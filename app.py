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
