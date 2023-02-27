from requests import Request, Session
import json
import time
import webbrowser
import pprint
import datetime
import pyodbc 
from dateutil import parser



def main ():
    
    # cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
    #                   "Server=127.0.0.1;"
    #                   "Database=MyDW;"
    #                   "Trusted_Connection=yes;")

    # cursor = cnxn.cursor()

    to_date = datetime.datetime.today()
    from_date = to_date - datetime.timedelta(days=7)
    CoinID = [1027,1]
    for id in CoinID:
        print("id",id)
        url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id="+str(id)+"&convertId=2781&timeStart="+str(round(from_date.timestamp()))+"&timeEnd="+str(round(to_date.timestamp()))
        session = Session()
        response = session.get(url, params={})
        info = json.loads(response.text)


        quotes=info['data']['quotes']

        for quote in quotes:
            pprint.pprint(quote['quote']['low'])


        

        #cursor.execute("INSERT INTO crypto.FactPrice (CoinId,[DateId],[OpenPrice],[ClosePrice],[HighPrice],[LowPrice],[Volume],[MarketCap])\
        #                SELECT '{id}', '{currency_name}', {exchange_rate}")
        

        # pprint.pprint(info)
        
main()