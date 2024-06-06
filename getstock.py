import requests
from bs4 import BeautifulSoup
import json
import datetime
import yfinance as yf

stocks = ['NVDA','LULU', 'AAPL', 'TSLA', 'AMZN', 'GOOGL', 'MSFT', 'META', 'NFLX']
stock_data = []
monthly_data = {symbol: [] for symbol in stocks}

def getData(symbol):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

    url = f'https://finance.yahoo.com/quote/{symbol}/'

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    price_tag = soup.find('fin-streamer', {'data-symbol': symbol, 'data-field': 'regularMarketPrice'})
    change_tag = soup.find('fin-streamer', {'data-symbol': symbol, 'data-field': 'regularMarketChange'})
    
    stock = {
        'symbol': symbol,
        'price': price_tag.text if price_tag else 'N/A',
        'change': change_tag.text if change_tag else 'N/A'
    }

    return stock

def getPastData(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1mo")
    for date, row in hist.iterrows():
        monthly_data[symbol].append({
            'date': date.strftime('%Y-%m-%d'),
            'price': row['Close'],
            'change': row['Close'] - row['Open']
        })

for item in stocks:
    stock_data.append(getData(item))
    getPastData(item)
    print("receiving: ", item)

with open('stock_data_today.json', 'w') as f:
    json.dump(stock_data, f, indent=4)

with open('stock_data_month.json', 'w') as f:
    json.dump(monthly_data, f, indent=4)

print("done")





