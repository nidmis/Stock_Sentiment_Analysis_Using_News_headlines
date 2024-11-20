# backend/model/stock_model.py

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tf_keras.models import Sequential, load_model
from tf_keras.layers import LSTM, Dense, Dropout
import yfinance as yf
import os

class StockModel:
    def __init__(self):
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model_path = os.path.join(os.path.dirname(__file__), "../saved_model/stock_model.h5")
        self.model = self.load_or_build_model()

    def load_or_build_model(self):
        try:
            model = load_model(self.model_path)
            print("Loaded saved model.")
            return model
        except:
            print("No saved model found. Building and training a new model.")
            model = Sequential()
            model.add(LSTM(100, return_sequences=True, input_shape=(60, 3)))
            model.add(Dropout(0.2))
            model.add(LSTM(100, return_sequences=False))
            model.add(Dropout(0.2))
            model.add(Dense(50, activation='relu'))
            model.add(Dense(1))
            model.compile(optimizer='adam', loss='mean_squared_error')
            self.model = model
            # Train the model with default symbol (e.g., SPY)
            data = self.fetch_historical_data('SPY')
            self.train_model(data)
            model.save(self.model_path)
            return model

    def train_model(self, data):
        """
        Train the LSTM model using historical stock data.
        """
        features = ['Close', 'Change', 'Volatility']
        data = data[features]
        data.dropna(inplace=True)
        # Scale the data
        scaled_data = self.scaler.fit_transform(data)
        # Prepare training data
        X_train = []
        y_train = []
        for i in range(60, len(scaled_data)):
            X_train.append(scaled_data[i-60:i])
            y_train.append(scaled_data[i, 0])  # Predicting the 'Close' price

        X_train, y_train = np.array(X_train), np.array(y_train)
        # Train the model
        self.model.fit(X_train, y_train, epochs=5, batch_size=32)
        print("Model trained and saved.")

    def fetch_historical_data(self, symbol):
        """
        Fetch historical stock data.
        """
        stock = yf.Ticker(symbol)
        data = stock.history(period="2y")
        if data.empty or data.shape[0] < 61:
            raise ValueError(f"Not enough historical data for symbol {symbol}")
        data['Change'] = data['Close'].pct_change()
        data['Volatility'] = data['High'] - data['Low']
        data = data[['Close', 'Change', 'Volatility']]
        data.dropna(inplace=True)
        return data

    def fetch_chart_data(self, symbol):
        """
        Fetch data for the stock chart.
        """
        data = self.fetch_historical_data(symbol)
        data.reset_index(inplace=True)
        chart_data = {
            'dates': data['Date'].dt.strftime('%Y-%m-%d').tolist(),
            'prices': data['Close'].tolist()
        }
        return chart_data

    def predict_next_day(self, data, sentiment_score):
        """
        Predict the next day's stock price.
        """
        try:
            features = ['Close', 'Change', 'Volatility']
            data = data[features]
            data.dropna(inplace=True)
            if data.shape[0] < 60:
                raise ValueError(f"Not enough data to make prediction. Available data points: {data.shape[0]}. Need at least 60.")
            scaled_data = self.scaler.transform(data.tail(60))
            X = np.expand_dims(scaled_data, axis=0)
            predicted_price_scaled = self.model.predict(X)[0][0]
            # Reconstruct the predicted price
            inverse_scaled = self.scaler.inverse_transform([[predicted_price_scaled, 0, 0]])
            predicted_price = inverse_scaled[0][0]
            current_price = data['Close'].iloc[-1]
            return {
                "current_price": float(current_price),
                "predicted_price": float(predicted_price),
                "trend": "Up" if predicted_price > current_price else "Down",
                "confidence": float(sentiment_score * 100)
            }
        except Exception as e:
            print(f"Error in predict_next_day: {e}")
            import traceback
            traceback.print_exc()
            raise
