# EarningsCallAnalyzer
![Page Image](https://github.com/felixwsiu/EarningsCallAnalyzer/blob/master/Scatterplot%20Screenshot.jpg)
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
A project that was built to find a correlation between the sentimental language found in a company's earnings call transcripts and the resulted change in stock price for a 1 month time period.

Important resources needed for this project:
<br>Exchange Ticker Symbols: http://www.eoddata.com/symbols.aspx
<br>Link Database to Earnings Call Transcripts: http://www.conferencecalltranscripts.org
<br>Positive Words Lexicon:https://github.com/jeffreybreen/twitter-sentiment-analysis-tutorial-201107/blob/master/data/opinion-lexicon-English/positive-words.txt
<br>Negative Words Lexicon:https://github.com/jeffreybreen/twitter-sentiment-analysis-tutorial-201107/blob/master/data/opinion-lexicon-English/negative-words.txt

The positive/negative opinion lexicons are used to filter out irrelevant words out of the transcripts to prevent cluttering of the sentiment score.

Since the scatterplot at the moment is not giving a strong enough correlation, a change in the modeling and weighing of sentiment words will need to be changed. A current work in progress!

## Technologies
Project is created with:
* Python version: 3.7.8

Scoring of each transcript was done using Amazon Comprehend (AWS Natural Language Processing) and the model was built on Amazon EC2 instances for virtual cloud hosting.
<br>Scatterplot and data science tools are from: https://matplotlib.org/

## Setup
Virtual environment for dependencies can be created by : python3 -m venv env

```
$ pip install awscli           (AWS Command Line Interface)
$ pip install boto3            (AWS SDK for Python)
$ pip3 install newspaper3k     (Used for article scraping and curation)
$ pip install beautifulsoup4   (Used for webpage scraping)
$ pip install requests         (Used with bs4 to send a get request to scrape results)
$ pip install yfinance         (Used to get historical data for companies)
$ pip install azure-cosmos     (Database storage for modeling)
$ pip install user_agent       (To prevent captchas on seekingalpha, a new browser agent was needed per request to prevent blocking)
```

Some environmental variables will be needed, please set these to run this project locally:
```
ACCOUNT_URI : This is the URI of your Azure Cosmos DB Account
ACCOUNT_KEY : This is the primary key of your Azure Cosmos DB Account
```
The model results were added to a Azure Cosmos DB container, you can save the results on disk instead if you like.
<br>Set up user in IAM (Identity and Access Management) for AWS instance management and connection.

 
