# backend/model/sentiment_model.py

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import requests
import os

class SentimentModel:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
        self.model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")
        self.NEWS_API_KEY = os.getenv('NEWS_API_KEY')

    def fetch_news(self, query):
        """
        Fetch news headlines using NewsAPI.
        """
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={self.NEWS_API_KEY}&language=en&sortBy=publishedAt&pageSize=10"
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            return [article["title"] for article in articles[:10]]
        else:
            print(f"Error fetching news: {response.status_code} - {response.text}")
            return []

    def analyze_sentiment(self, headlines):
        """
        Analyze sentiment of the news headlines using FinBERT.
        """
        if not headlines:
            return {"positive": 0, "neutral": 0, "negative": 0}

        inputs = self.tokenizer(headlines, truncation=True, padding=True, return_tensors="pt")
        outputs = self.model(**inputs)
        logits = outputs.logits
        predictions = torch.nn.functional.softmax(logits, dim=-1).detach().cpu().numpy()

        # Label mapping for 'yiyanghkust/finbert-tone':
        # 0: Positive, 1: Negative, 2: Neutral
        positive = predictions[:, 0].mean()
        negative = predictions[:, 1].mean()
        neutral = predictions[:, 2].mean()

        return {
            "positive": float(positive),
            "neutral": float(neutral),
            "negative": float(negative)
        }
