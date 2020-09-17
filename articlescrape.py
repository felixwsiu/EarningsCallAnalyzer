from newspaper import Article, Config
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from datetime import datetime
from user_agent import generate_user_agent, generate_navigator


url = "http://www.conferencecalltranscripts.org/?co=tsla"
urlt = "https://seekingalpha.com/article/4360072-tesla-inc-tsla-ceo-elon-musk-on-q2-2020-results-earnings-call-transcript"
#Seeking alpha forces a capcha when trying to scrape their list of transcripts, therefore conferencecalltranscripts.org is used instead



#Browser user_agents must be randomly generated to prevent capcha/ anti-scraping mechanisms
#Setups browser by preparing a random user agent for scraping
#@return {config} config object from newspaper3k
def setupAgent():
	config = Config()
	config.browser_user_agent = generate_user_agent()
	config.fetch_images = False
	return config



#Returns the full text of the given earnings call transcript 
#@params {urL} url of the earnings call transcript
def getTranscriptText(url):
	article = prepareArticle(url)
	if article != False and (len(article.text) > 1000):
		return article.text
	else:
		return False

#Returns the date of the earnings call was published
#@params {urL} url of the earnings call transcript
def getTranscriptPublishDate(url):
	article = prepareArticle(url)
	if article == False:
		return False
	return article.publish_date


#Consumes a webpage URL and prepares it in the form of an Article
#@params {urL} url of a webpage
#@returns {article} article of the webpage
def prepareArticle(url):
	config = setupAgent()
	article = Article(url,config=config)
	try:
		article.download()
		article.parse()
		return article
	except Exception as e:
		print("Article could not be downloaded")
		return False
	


#Returns all possible transcript links for a ticker
#@params {string} ticker : ticker symbol for the stock
def getAllTranscriptsForTicker(ticker):
	urls = []
	url = "http://www.conferencecalltranscripts.org/?co=" + ticker
	soup = BeautifulSoup(requests.get(url).content, "html.parser")
	for link in soup.find_all('a'):
		if ("/include?location=" in str(link.get('href'))) and ("fool" in str(link.get('href')) or "seekingalpha" in str(link.get('href'))):
			urls.append(str(link.get("href"))[18:])
	return urls

