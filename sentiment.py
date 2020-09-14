import articlescrape
import boto3
import json

comprehend = boto3.client(service_name='comprehend', region_name='region')

# Returns the word frequency of a given text
# @returns { dict {string,number} } dictionary object of word frequency
def getWordFrequencyMap(text):
	dict = {}
	listofwords = text.split()
	for word in listofwords:
		if word in dict:
			dict[word] = dict[word] + 1
		else:
			dict[word] = 1
	return dict


