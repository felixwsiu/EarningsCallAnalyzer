from azure.cosmos import CosmosClient
import yfinance as yf
import articlescrape
from datetime import datetime
import calendar
import scorer
import os


#Used to graph the scatterplot
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np

url = os.environ['ACCOUNT_URI']
key = os.environ['ACCOUNT_KEY']
client = CosmosClient(url, credential=key)
database_name = "EarningsCallAnalyzer"
database = client.get_database_client(database_name)
container_name = "Model"
container = database.get_container_client(container_name)


# Takes in a list of tickers and creates a database of scores
# Run this function to initialize the model so the scatterplot can be plotted
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
				try:
					change = yf.download(ticker, start=date, end=futuredate)
					start = change["High"][0]
					end = change["High"][-1]
					difference = end - start
					pChange = difference/start * 100
					print("Added an entry for " + ticker)
					addEntry(ticker,score,pChange)
				except Exception as e:
					print("Could not download ticker, probably delisted") 
					break



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
	with open("NYSE_EDITED.txt") as file:
		lines = file.readlines()
		for line in lines:
			ticker = line.split(",")[0]
			tickerlist.append(ticker)
	return tickerlist

# Returns all score and price change data from the ticker model built in our database
def getDataForScattter():
	languagescores = []
	pricechanges = []
	for item in container.query_items(query='SELECT * FROM c', enable_cross_partition_query=True):
		languagescores.append(item["score"])
		pricechanges.append(item["change"])
	return languagescores, pricechanges

# Plots the scatterplot using the data from the model
def plotScatter():
	x,y = getDataForScattter()
	colors = (0,0,0)
	area = np.pi*3
	plt.scatter(x, y, s=area, c=colors, alpha=0.5)
	plt.title('Earnings Call Analysis with Natural Language Processing')
	plt.xlabel('Earnings Language Score')
	plt.ylabel('Price Change %')
	plt.show()

plotScatter()