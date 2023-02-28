from requests import Request, Session
import json
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
    from_date = to_date - datetime.timedelta(days=8)

    # number of coins
    limit_of_coins = 20
    url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit="+str(limit_of_coins)+"&sortBy=market_cap&sortType=desc&convertId=2781&cryptoType=all&tagType=all&audited=false&pageSize="+str(limit_of_coins)+"&page=1"
    session = Session()
    response = session.get(url, params={})
    info = json.loads(response.text)
    # coin_ids = [coin['id'] for coin in info['data']['cryptoCurrencyList']]
    # print("Coin IDs:", coin_ids)
    
    for coin in info['data']['cryptoCurrencyList']:
        print("Fetching ==>> ",coin["symbol"],"\n")
        
        cursor.execute("SELECT TOP 1 [ID] FROM  [MyDW].[crypto].[DimCoin] WHERE [CoinID] = ?",coin['id'])

        if cursor.rowcount == 0:
            cursor.execute("INSERT INTO [MyDW].[crypto].[DimCoin] ([CoinID],[Name],[Symbol]) VALUES (?, ?, ?)",
                           coin['id'], coin['name'], coin['symbol'])
            cnxn.commit()
            cursor.execute("SELECT @@IDENTITY AS ID;")
            coin_last_insert_ID = cursor.fetchone()[0]
        else :
            coin_last_insert_ID = cursor.fetchone()[0]    
        

        # inserted_id = cursor.inser

        url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id=" + str(coin['id']) + "&convertId=2781&timeStart=" + str(round(from_date.timestamp())) + "&timeEnd=" + str(round(to_date.timestamp()))
        session = Session()
        response = session.get(url, params={})
        info = json.loads(response.text)

        quotes = info['data']['quotes']

        for quote in quotes:
            timeClose = parser.parse(quote['timeClose'])

            print("     Date ==>> ",timeClose.strftime("%Y/%m/%d"))
            
            cursor.execute("SELECT TOP 1 [DateID] FROM  [MyDW].[crypto].[DimDate] WHERE [DateID] = ?",timeClose.strftime("%Y%m%d"))

            if cursor.rowcount == 0:
              month = int(timeClose.strftime("%m"))
              if month >= 1 and month <= 3 :
                  q = 1
              elif month >= 4 and month <= 6:
                  q = 2
              elif month >= 7 and month <= 9:  
                  q = 3
              else :
                  q = 4
                  
              cursor.execute("INSERT INTO [MyDW].[crypto].[DimDate] ([DateID],[Year],[Quarter],[Month],[Day]) VALUES (?, ?, ?, ?, ?)",
                           timeClose.strftime("%Y%m%d"), timeClose.strftime("%Y"), q, month, timeClose.strftime("%d"))
              cnxn.commit()
            
            date_id = timeClose.strftime("%Y%m%d")
            open_price = quote['quote']['open']
            close_price = quote['quote']['close']
            high_price = quote['quote']['high']
            low_price = quote['quote']['low']
            volume = quote['quote']['volume']
            market_cap = quote['quote']['marketCap']

            cursor.execute("SELECT TOP 1 [Date] FROM  [MyDW].[crypto].[FactPrice] WHERE [Date] = ? AND [CoinId] = ?",timeClose.strftime("%Y%m%d"),coin_last_insert_ID)

            if cursor.rowcount == 0 :
                cursor.execute("INSERT INTO [MyDW].[crypto].[FactPrice] ([CoinId],[Date],[OpenPrice],[ClosePrice],[HighPrice],[LowPrice],[Volume],[MarketCap]) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           coin_last_insert_ID, date_id, open_price, close_price, high_price, low_price, volume, market_cap)

        cnxn.commit()

    cursor.close()
    cnxn.close()

coinMarketScraper()    