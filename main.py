import requests
from datetime import *
from twilio.rest import Client
import os
from twilio.http.http_client import TwilioHttpClient

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY = "elo"
account_sid = "elo"
auth_token = "my auth tocken"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

url = 'https://www.alphavantage.co/query'
alpha_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": "demo",
}
r = requests.get(url, params=alpha_parameters)
data = r.json()
data_list = list(data["Time Series (Daily)"].items())

previous_day_closing_price = float(data_list[1][1]["4. close"])
day_before_yesterday_closing_price = float(data_list[2][1]["4. close"])

positive_difference_between_prices = abs(day_before_yesterday_closing_price - previous_day_closing_price)
percentage_difference = (positive_difference_between_prices / previous_day_closing_price) * 100

# if percentage_difference > 5:
#     print("Get News")

news_url = 'https://newsapi.org/v2/everything'
news_parameters = {
    "apiKey": API_KEY,
    "qInTitle": COMPANY_NAME,
    "from": datetime.date()
}
news_request = requests.get(news_url, params=news_parameters)
news_data = news_request.json()
news_articles = news_data["articles"]

articles_list = news_articles[1:3]

new_article_list = [f"Headline: {article['headline']} \nBrief:{article['description']}" for article in articles_list]

proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {'https': os.environ['https_proxy']}
client = Client(account_sid, auth_token, http_client=proxy_client)
for article_idx in new_article_list:
    message = client.messages \
                .create(
                body= article_idx,
                from = '12456789',
                to = '25125',
            )


