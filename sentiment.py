import articlescrape
import boto3
import json

comprehend = boto3.client(service_name="comprehend", region_name="us-east-2")

#Gets the positive and negative words from text
wordlist=[]
with open("words.txt") as file:
	lines = file.readlines()
	for line in lines:
		wordlist.append(line.strip())


# By using AWS Comprehend, key words/phrases will be analyzed for their sentiment
# Depending if the word is "positive" or "negative", the corresponding confidence value will be used as the weight for that word
# The end score of a transcript will be determined by the (weight * occurence of positive words) - (weight * occurence of negative words)
# The score will then be related to the change in stock price after earnings to attempt to relate the data
# This model will be used to predict future price changes from earning calls



# Returns the word sentiment value 
def getSentiment(text):
	return json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4)


# Returns the word frequency of a given text
# @returns { dict {string,number} } dictionary object of word frequency
def getWordFrequencyMap(text):
	dict = {}
	listofwords = text.split()
	for word in listofwords:
		print(word)
		if word in wordlist:
			if word in dict:
				dict[word] = dict[word] + 1
			else:
				dict[word] = 1
	return sorted(dict.items(), key=lambda x:x[1], reverse=True)


