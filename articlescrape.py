from newspaper import Article, Config
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from datetime import datetime
from user_agent import generate_user_agent, generate_navigator


url = "http://www.conferencecalltranscripts.org/?co=tsla"
urlt = "https://seekingalpha.com/article/4360072-tesla-inc-tsla-ceo-elon-musk-on-q2-2020-results-earnings-call-transcript"
#Seeking alpha forces a capcha when trying to scrape their list of transcripts, therefore conferencecalltranscripts.org is used instead
#Browser user_agents must be randomly generated to prevent 

config = Config()
config.browser_user_agent = generate_user_agent()
config.fetch_images = False




#Returns the full text of the given earnings call transcript 
#@params {urL} url of the earnings call transcript
def getTranscriptText(url):
	article = prepareArticle(url)
	return article.text

#Returns the date of the earnings call was published
#@params {urL} url of the earnings call transcript
def getTranscriptPublishDate(url):
	article = prepareArticle(url)
	return article.publish_date


#Consumes a webpage URL and prepares it in the form of an Article
#@params {urL} url of a webpage
#@returns {article} article of the webpage
def prepareArticle(url):
	article = Article(url,config=config)
	article.download()
	article.parse()
	return article


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
