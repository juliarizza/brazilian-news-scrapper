import argparse
import requests
import logging
import time
import csv

from bs4 import BeautifulSoup
from datetime import date, timedelta

from homepage import *
from news import *

# get arguments
parser = argparse.ArgumentParser(description='Scrap UOL news.')
parser.add_argument('--date-since', required=False,
                    help='date to start the scrapping in the format YYYY-MM-DD')
parser.add_argument('--end-date', required=False,
                    help='date to end the scrapping in the format YYYY-MM-DD')
args = parser.parse_args()

# configure logging
logger = logging.getLogger('uol_scrapper')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('scrapper.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

# configuring csv
csvfile = open('data.csv', 'a')
fieldnames = ['Title', 'Category', 'Author', 'Date', 'Location', 'URL', 'Source']
news_writer = csv.DictWriter(csvfile, fieldnames)

# parameters definition
URL = "https://noticias.uol.com.br/arquivohome/{date}home_23.jhtm"

if args.date_since:
    date_since = args.date_since.split('-')
    YEAR = int(date_since[0])
    MONTH = int(date_since[1])
    DAY = int(date_since[2])
else:
    YEAR = 2009
    MONTH = 1
    DAY = 1

date_from = date(YEAR, MONTH, DAY)

if args.end_date:
    end_date = args.end_date.split('-')
    END_YEAR = int(end_date[0])
    END_MONTH = int(date_since[1])
    END_DAY = int(date_since[2])
    date_to = date(END_YEAR, END_MONTH, END_DAY)
else:
    date_to = date.today()

while date_from != date_to:
    logger.info("Getting homepage for {date}".format(date=date_from.isoformat()))
    # getting the page's content
    datestr = date_from.strftime('%Y%m%d')
    hp = Homepage(URL.format(date=datestr))

    if not bool(hp.get_html()):
        logger.error("Could not acquire homepage")

    version = hp.get_version()
    if version == 'V1':
        logger.info("Homepage version: V1")
        hp = HomepageV1(hp.url)
        links = hp.get_links()

        for link in set(links):
            logger.info(f"Requesting news: {link}")
            # avoid being classified as spammer
            time.sleep(1)

            try:
                news = News(link)
            except:
                logger.error("News no longer available")
                continue

            if news.get_version() == 'UOL NOTICIAS':
                try:
                    news = UolNoticiasV1(news.url)
                    news_writer.writerow(news.to_dict())
                    logger.info("Recording news data.")
                except:
                    logger.warning("Could not find metadata. It may be that the format of this content is not correct.")
            else:
                logger.warning("News format not supported.")
    
    date_from = date_from + timedelta(days=1)

# close csv
csvfile.close()