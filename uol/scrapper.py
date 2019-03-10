import argparse
import requests
import logging
import time
import csv

from bs4 import BeautifulSoup
from datetime import date

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

# version identifiers
def is_v1(soup):
    return soup.find(id='corpo')

def is_v2(soup):
    pass

def is_v3(soup):
    pass

# provider identifiers
def is_uol_noticias(url):
    return 'noticias.uol.com.br' in url

def is_folha_sao_paulo(url):
    return 'folha.uol.com.br' in url

logger.info("Getting homepage for {date}".format(date=date.isoformat()))
# getting the page's content
datestr = date.strftime('%Y%m%d')
response = requests.get(URL.format(date=datestr))
if not response.status_code == 200:
    logger.error("Could not acquire homepage")
    # continue

# parsing the content
soup = BeautifulSoup(response.text, 'html.parser')

links = []
if is_v1(soup):
    logger.info("Homepage version: V1")
    news = soup.find(id='conteudo')
    # filter news links
    for link in news.find_all('a'):
        # links to be ignored
        q1 = link.parent.get('id') == 'topo-direita'
        q2 = link.parent.parent.get('id') == 'mod-horz-top'
        q3 = link.get('name') == 'tempo'
        q4 = '-chapeu' in link.get('name', '')
        q5 = '-canais' in link.get('name', '')
        # add links to list
        if not (q1 or q2 or q3 or q4 or q5):
            links.append(link.get('href'))
    logger.info("Links acquired")

    for link in set(links):
        logger.info(f"Requesting news: {link}")
        # avoid being classified as spammer
        time.sleep(1)

        # get the page's content
        try:
            content = requests.get(link)

            if not content.status_code == 200:
                logger.error("News no longer available")
                continue
        except:
            logger.error("News no longer available")
            continue

        # identify the provider
        if is_uol_noticias(link):
            source = 'UOL Notícias'

            try:
                news_soup = BeautifulSoup(content.text, 'html.parser')
                category_info = news_soup.find(id='barra-estacao')
                category = category_info.find(class_='canal').string

                top_info = news_soup.find(id='titulo').find(class_='conteudo')
                title = top_info.h1.string
                date_time = top_info.h2.string

                author = None
                location = None

                meta = news_soup.find(id='credito-texto')
                if meta:
                    meta = meta.split('<br>')
                    for data in meta:
                        if 'em' in data.lower():
                            location = data
                        elif 'especial' in data.lower():
                            pass
                        else:
                            author = data

                logger.info("Recording data")
                news_writer.writerow([title, category, author, 
                    date_time, location, link, source])
            except:
                logger.warning("Could not find metadata. It may be that the format of this content is not correct.")

        elif is_folha_sao_paulo(link):
            pass

elif is_v2(soup):
    pass
elif is_v3(soup):
    pass
else:
    logger.error("Could not find homepage version")

# close csv
csvfile.close()