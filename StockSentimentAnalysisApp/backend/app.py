# backend/app.py

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
from model.sentiment_model import SentimentModel
from model.stock_model import StockModel
import yfinance as yf

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Load environment variables
load_dotenv('.env')

# API Key Configuration
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

# Initialize models
sentiment_model = SentimentModel()
stock_model = StockModel()

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/stock.html')
def serve_stock():
    return send_from_directory(app.static_folder, 'stock.html')

@app.route('/news.html')
def serve_news():
    return send_from_directory(app.static_folder, 'news.html')

def get_market_trends():
    """
    Fetch current trends for Dow Jones, NASDAQ, and S&P 500.
    """
    try:
        indices = {
            '^DJI': 'Dow Jones Industrial Average',
            '^IXIC': 'NASDAQ Composite',
            '^GSPC': 'S&P 500'
        }
        trends = []
        for symbol, name in indices.items():
            data = yf.Ticker(symbol)
            hist = data.history(period='1d')
            current_price = hist['Close'].iloc[-1]
            previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else hist['Open'].iloc[0]
            change = ((current_price - previous_close) / previous_close) * 100
            trends.append({
                'symbol': symbol,
                'name': name,
                'current_price': round(float(current_price), 2),
                'change_percent': round(float(change), 2)
            })
        return trends
    except Exception as e:
        print(f"Error fetching market trends: {e}")
        return []

@app.route('/api/market-trends', methods=['GET'])
def get_market_trends_api():
    """
    API endpoint to get current market trends.
    """
    try:
        trends = get_market_trends()
        return jsonify({"trends": trends})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/news/<string:symbol>', methods=['GET'])
def get_news(symbol):
    """
    Fetch recent news for a specific stock symbol.
    """
    try:
        news = sentiment_model.fetch_news(symbol)
        return jsonify({"symbol": symbol.upper(), "news": news})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/news/top-news', methods=['GET'])
def get_top_news():
    """
    Fetch top news headlines.
    """
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({"error": "Failed to fetch news."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stock-chart/<string:symbol>', methods=['GET'])
def get_stock_chart(symbol):
    """
    Fetch stock chart data for a specific symbol.
    """
    try:
        chart_data = stock_model.fetch_chart_data(symbol)
        return jsonify(chart_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/predict/<string:symbol>', methods=['GET'])
def predict_stock(symbol):
    """
    Predict stock price trends and confidence levels.
    """
    try:
        historical_data = stock_model.fetch_historical_data(symbol)
        news = sentiment_model.fetch_news(symbol)
        sentiment = sentiment_model.analyze_sentiment(news)
        prediction = stock_model.predict_next_day(symbol, sentiment["positive"])

        return jsonify({
            "symbol": symbol,
            "predicted_price": prediction["predicted_price"],
            "current_price": prediction["current_price"],
            "trend": prediction["trend"],
            "confidence": prediction["confidence"],
            "news": news,
            "sentiment": sentiment
        })
    except Exception as e:
        print(f"Error in predict_stock for symbol {symbol}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
