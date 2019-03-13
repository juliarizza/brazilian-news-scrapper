import argparse
import requests
import logging
import time
import csv

from bs4 import BeautifulSoup
from datetime import date

from homepage import *
from news import *

# get arguments
parser = argparse.ArgumentParser(description='Scrap UOL news.')
parser.add_argument('--date-since', required=False,
                    help='date to start the scrapping in the format YYYY-MM-DD')
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
csvfile = open('data.csv', 'w')
news_writer = csv.writer(csvfile)
news_writer.writerow(['Title', 'Category', 'Author', 'Date', 'Location', 'URL', 'Source'])

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


date = date(YEAR, MONTH, DAY)

logger.info("Getting homepage for {date}".format(date=date.isoformat()))
# getting the page's content
datestr = date.strftime('%Y%m%d')
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
                news_writer.writerow(news.to_array())
                logger.info("Recording news data.")
            except:
                logger.warning("Could not find metadata. It may be that the format of this content is not correct.")
        else:
            logger.warning("News format not supported.")

# close csv
csvfile.close()