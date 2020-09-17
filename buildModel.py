from azure.cosmos import CosmosClient
import yfinance as yf
import articlescrape
from datetime import datetime
import calendar
import scorer
import os

url = os.environ['ACCOUNT_URI']
key = os.environ['ACCOUNT_KEY']
client = CosmosClient(url, credential=key)
database_name = "EarningsCallAnalyzer"
database = client.get_database_client(database_name)
container_name = "Model"
container = database.get_container_client(container_name)


# Takes in a list of tickers and creates a database of scores
def buildModel(listOfTickers):
	for ticker in listOfTickers:
		urls = articlescrape.getAllTranscriptsForTicker(ticker)
		for url in urls:
			date = articlescrape.getTranscriptPublishDate(url)
			score = scorer.getScoreOfCall(url)

			if date == False or score == False:
				continue

			futuredate = add_months(date,1)

			#Only valid dates that exist will be parsed
			if futuredate <  datetime.today():
				change = yf.download(ticker, start=date, end=futuredate)
				start = change["High"][0]
				end = change["High"][-1]
				difference = end - start
				pChange = difference/start * 100
				print("Added an entry for " + ticker)
				addEntry(ticker,score,pChange)



def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime(year, month, day)


# Adds an earnings call entry to the model
# @params {string} ticker: ticker symbol of stock
# @params {float} score: sentiment score of the earnings call
# @params {float} change: change that occured after earnings call
def addEntry(ticker, score, change):
	container.upsert_item(
        {
            "ticker": ticker,
    		"score": score,
    		"change": change,
    	}
    )


def getListOfTickers():
	tickerlist=[]
	with open("NYSE_20200916.txt") as file:
		lines = file.readlines()
		for line in lines:
			ticker = line.split(",")[0]
			tickerlist.append(ticker)
	return tickerlist


buildModel(getListOfTickers())

