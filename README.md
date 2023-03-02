# Coin Market Cap Scraper and BI Dashboard
The purpose of this repo is to build a bi dashboard for cryptocurrency market
# How To Start ?
* Install Microsoft Sql Server
* Run SqlDump.sql to setup database and tables structure
* Install Python
* In coinMarketScraper.py define database connection inside pyodbc.connect method
* Run scraper with python (to fetch and save coin market cap data)
* Open CoinMarketCapDashboard.pbix to explore the dashboard (The Data is already imported Based on My own Dw , Please change the connection Source if you want to work with the updated Data from your database)