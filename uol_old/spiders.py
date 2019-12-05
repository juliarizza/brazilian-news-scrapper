import logging
import scrapy
import datetime

# configure logging
logger = logging.getLogger('uol_spider')
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

# parameters definition
URL = "https://noticias.uol.com.br/arquivohome/20090101home_23.jhtm"


class UOL2009Spider(scrapy.Spider):
    """
        This spider crawls content from UOL's first version.
        This version lasts until 2011-10-04.
    """
    name = 'UOL 2009'
    min_date = datetime.date(2009, 1, 1)
    max_date = datetime.date(2011, 10, 4)
    start_urls = [URL]
   
    def parse(self, response):
        for link in response.css('a::attr("href")'):
            print(link)