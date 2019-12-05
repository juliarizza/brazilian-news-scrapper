import scrapy
import datetime

from uol.utils import daterange

# parameters definition
URL = "https://noticias.uol.com.br/arquivohome/{date}home_23.jhtm"


class UOL2009Spider(scrapy.Spider):
    """
        This spider crawls content from UOL's first version.
        This version lasts until 2011-10-04.
    """
    name = 'uol_2009'
    min_date = datetime.date(2009, 1, 1)
    max_date = datetime.date(2011, 10, 4)
    ignore_containing = [
        'javascript', # page events
        'tvuol', # videos
        '/album' # photos
    ]

    def start_requests(self):
        urls = []
        for date in daterange(self.min_date, self.max_date):
            date_url = URL.format(date=date.strftime('%Y%m%d'))
            urls.append(date_url)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
   
    def parse(self, response):
        MODULOS_SELECTOR = '#modulos a::attr("href")'
        MANCHETES_SELECTOR = '#novas-manchetes a::attr("href")'
        
        regex = r"^(?!{list_to_ignore}).*$".format(
            list_to_ignore='|'.join(self.ignore_containing)
        )
        
        for anchor in set(response.css(MODULOS_SELECTOR).re(regex)):
            yield scrapy.Request(url=anchor, callback=self.extract)

        for anchor in set(response.css(MANCHETES_SELECTOR).re(regex)):
            yield scrapy.Request(url=anchor, callback=self.extract)
    
    def extract(self, response):
        pass