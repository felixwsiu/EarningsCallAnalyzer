from azure.cosmos import CosmosClient
import articlescrape
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
			print(url)
			score = scorer.getScoreOfCall(url)
			print(score)




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

buildModel(["TSLA"])