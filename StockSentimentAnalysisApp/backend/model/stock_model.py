# backend/model/stock_model.py

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tf_keras.models import Sequential
from tf_keras.layers import LSTM, Dense, Dropout
import yfinance as yf

class StockModel:
    def __init__(self):
        pass  # Removed self.scaler initialization

    def fetch_historical_data(self, symbol):
        """
        Fetch historical stock data and prepare features.
        """
        stock = yf.Ticker(symbol)
        data = stock.history(period="2y")
        if data.empty or data.shape[0] < 120:
            raise ValueError(f"Not enough historical data for symbol {symbol}")
        data['Change'] = data['Close'].pct_change()
        data['Volatility'] = data['High'] - data['Low']
        data['Volume'] = data['Volume'].pct_change()
        data['MA7'] = data['Close'].rolling(window=7).mean()
        data['MA14'] = data['Close'].rolling(window=14).mean()
        data['MA30'] = data['Close'].rolling(window=30).mean()
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

    def predict_next_day(self, symbol, sentiment_score):
        """
        Predict the next day's stock price.
        """
        try:
            data = self.fetch_historical_data(symbol)
            # Include sentiment score in features
            data['Sentiment'] = sentiment_score
            features = ['Close', 'Change', 'Volatility', 'Volume', 'MA7', 'MA14', 'MA30', 'Sentiment']
            data = data[features]
            data.dropna(inplace=True)
            num_features = len(features)
            if data.shape[0] < 120:
                raise ValueError(f"Not enough data to make prediction for {symbol}. Need at least 120 data points.")
            
            # Split data into training and prediction sets
            train_data = data[:-1]
            test_data = data[-61:]  # Last 61 data points for prediction

            # Check for NaN or infinite values
            if train_data.isnull().values.any():
                raise ValueError("train_data contains NaN values after dropping missing data.")

            if not np.isfinite(train_data.values).all():
                raise ValueError("train_data contains infinite values.")

            # Scale the data
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(train_data)

            # Prepare training data
            X_train = []
            y_train = []
            for i in range(60, len(scaled_data)):
                X_train.append(scaled_data[i - 60:i])
                y_train.append(scaled_data[i, 0])  # Predicting 'Close' price

            X_train, y_train = np.array(X_train), np.array(y_train)

            # Build and train the model
            model = Sequential()
            model.add(LSTM(100, return_sequences=True, input_shape=(60, num_features)))
            model.add(Dropout(0.2))
            model.add(LSTM(100, return_sequences=False))
            model.add(Dropout(0.2))
            model.add(Dense(50, activation='relu'))
            model.add(Dense(1))
            model.compile(optimizer='adam', loss='mean_squared_error')
            model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=0)

            # Prepare input for prediction
            last_60_data = test_data.tail(60)
            last_60_data['Sentiment'] = sentiment_score  # Ensure sentiment is up-to-date

            # Ensure columns are in the same order
            last_60_data = last_60_data[features]

            scaled_last_60_data = scaler.transform(last_60_data)
            X_predict = np.expand_dims(scaled_last_60_data, axis=0)

            # Make prediction
            predicted_price_scaled = model.predict(X_predict)[0][0]
            # Reconstruct the predicted price
            inverse_scaled = scaler.inverse_transform([[predicted_price_scaled] + [0]*(num_features-1)])
            predicted_price = inverse_scaled[0][0]
            current_price = data['Close'].iloc[-1]

            return {
                "current_price": float(current_price),
                "predicted_price": float(predicted_price),
                "trend": "Up" if predicted_price > current_price else "Down",
                "confidence": float(sentiment_score * 100)
            }
        except Exception as e:
            print(f"Error in predict_next_day for {symbol}: {e}")
            import traceback
            traceback.print_exc()
            raise
