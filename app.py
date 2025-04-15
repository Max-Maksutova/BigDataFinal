from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

ALPHA_VANTAGE_KEY = os.getenv('ALPHA_VANTAGE_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/fetch-data", methods=["POST"])
def fetch_data():
    data = request.json
    symbol = data.get("symbol")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    stock_data = fetch_stock_data(symbol)
    news_data = fetch_tariff_news()

    return jsonify({"stock": stock_data, "news": news_data})

from datetime import datetime

def fetch_stock_data(symbol):
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": ALPHA_VANTAGE_KEY
    }
    response = requests.get(url, params=params)
    raw_data = response.json()

    if "Time Series (Daily)" not in raw_data:
        return []

    time_series = raw_data["Time Series (Daily)"]
    parsed_data = [
        {
            "date": date,
            "price": float(info["5. adjusted close"])
        }
        for date, info in sorted(time_series.items())
    ]
    return parsed_data

def fetch_tariff_news():
    query = "tariff OR trade war"
    url = f"https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 50,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(url, params=params)
    articles = response.json().get("articles", [])

    news_data = []
    for idx, article in enumerate(articles):
        news_data.append({
            "id": idx,
            "title": article["title"],
            "publishedAt": article["publishedAt"][:10],
            "source": article["source"]["name"],
            "url": article["url"]
        })

    return news_data

if __name__ == "__main__":
    app.run(debug=True)
