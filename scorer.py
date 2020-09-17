import articlescrape
import sentiment


# Will return the given score based off of scores.txt of the given map of words with frequencies
# @returns {integer} score : the score of the earnings call based off of sentiment scores

def getScoreOfWords(wordmap):
	scorereference = {}
	totalscore = 0
	scores = open("scores.txt","r")
	lines = scores.readlines()
	for line in lines:
		words = line.split()
		scorereference[words[0]] = [words[1],words[2]]

	for word in wordmap:
		totalscore += (word[1] * float(scorereference[word[0]][0])) + (word[1] * float(scorereference[word[0]][1]))

	return(totalscore)


# Returns the predicted score of an earnings call based off of word sentiment
# @params {url} url : url of an earnings call
# @returns {float} score: sentiment score of the earnings call
def getScoreOfCall(url):
	text = articlescrape.getTranscriptText(url)
	if text:
		wordmap = sentiment.getWordFrequencyMap(text)
		callscore = getScoreOfWords(wordmap)
		return callscore
	else:
		return False