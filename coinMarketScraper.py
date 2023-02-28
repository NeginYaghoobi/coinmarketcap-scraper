from requests import Request, Session
import json
import time
import webbrowser
import pprint
import datetime
import pyodbc
from dateutil import parser

def coinMarketScraper():

    cnxn = pyodbc.connect("Driver={SQL Server};"
                          "Server=127.0.0.1,1433"
                          "Database=MyDW;"
                          'UID = sa;'
                          'PWD = Aa123456;'
                          "Trusted_Connection=yes;")
    cursor = cnxn.cursor()

    to_date = datetime.datetime.today()
    from_date = to_date - datetime.timedelta(days=7)

    url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=2000&sortBy=market_cap&sortType=desc&convertId=2781&cryptoType=all&tagType=all&audited=false&pageSize=5000&page=1"
    session = Session()
    response = session.get(url, params={})
    info = json.loads(response.text)
    coin_ids = [coin['id'] for coin in info['data']['cryptoCurrencyList']]
    # print("Coin IDs:", coin_ids)

    for coin_id in coin_ids:

        url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id=" + str(coin_id) + "&convertId=2781&timeStart=" + str(round(from_date.timestamp())) + "&timeEnd=" + str(round(to_date.timestamp()))
        session = Session()
        response = session.get(url, params={})
        info = json.loads(response.text)

        quotes = info['data']['quotes']
        for quote in quotes:
            date_id = parser.parse(quote['timeClose']).strftime("%Y%m%d")
            open_price = quote['quote']['open']
            close_price = quote['quote']['close']
            high_price = quote['quote']['high']
            low_price = quote['quote']['low']
            volume = quote['quote']['volume']
            market_cap = quote['quote']['marketCap']
            cursor.execute("INSERT INTO [MyDW].[crypto].[FactPrice] ([CoinId],[DateId],[OpenPrice],[ClosePrice],[HighPrice],[LowPrice],[Volume],[MarketCap]) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           coin_id, date_id, open_price, close_price, high_price, low_price, volume, market_cap)

        cnxn.commit()

    cursor.close()
    cnxn.close()

coinMarketScraper()    