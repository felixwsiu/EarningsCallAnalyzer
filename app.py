import sentiment
import articlescrape
import scorer 

# Analyzes an earnings call and  provides a score and the predicted change in stock performance
# @params {url} url : url of an earnings call
def analyzeEarningsCall(url):
	score = scorer.getScoreOfCall(url)
	print("Sentiment Score of Earnings : " + str(score))
	change = getStockPerformanceChange(score)
	print("Predicted Stock Performance Change : " + str(change))



# Returns the predicted change in stock performance
def getStockPerformanceChange(score):
	return 5

analyzeEarningsCall("https://seekingalpha.com/article/4360072-tesla-inc-tsla-ceo-elon-musk-on-q2-2020-results-earnings-call-transcript")