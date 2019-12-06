import scrapy
import datetime

from scrapy.loader import ItemLoader

from uol.items import UolItem
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
        r'javascript', # page events
        r'tvuol', # videos
        r'/album', # photos
        r'/shopping' # ecommerce
    ]

    def start_requests(self):
        urls = ["https://noticias.uol.com.br/arquivohome/20090101home_23.jhtm"]
        # for date in daterange(self.min_date, self.max_date):
        #     date_url = URL.format(date=date.strftime('%Y%m%d'))
        #     urls.append(date_url)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
   
    def parse(self, response):
        MODULOS_SELECTOR = '#modulos a::attr("href")'
        MANCHETES_SELECTOR = '#novas-manchetes a::attr("href")'
        
        regex = r"^(?!{list_to_ignore}).*$".format(
            list_to_ignore='|'.join(self.ignore_containing)
        )
        
        for anchor in set(response.css(MODULOS_SELECTOR).re(regex)):
            yield response.follow(anchor, callback=self.extract)

        for anchor in set(response.css(MANCHETES_SELECTOR).re(regex)):
            yield response.follow(anchor, callback=self.extract)

    def extract(self, response):
        if 'folha' in response.url:
            return self.extract_fsp(response)
        elif 'blogosfera' in response.url:
            return self.extract_blogosfera(response)
        else:
            return self.extract_uol(response)
    
    def extract_fsp(self, response):
        CATEGORY_SELECTOR = '.section-masthead h1::text'
        TITLE_SELECTOR = '#news header h1::text'
        AUTHOR_SELECTOR = '#news header .author::text'
        LOCATION_SELECTOR = '#news header .author-location::text'
        DATETIME_SELECTOR = '#news header time::attr("datetime")'
        COMMENTS_COUNT_SELECTOR = '#article-comments header a.more::text'
        
        loader = ItemLoader(item=UolItem(), response=response)
        loader.add_css('title', TITLE_SELECTOR)
        loader.add_css('author', AUTHOR_SELECTOR)
        loader.add_css('category', CATEGORY_SELECTOR)
        loader.add_css('location', LOCATION_SELECTOR)
        loader.add_css('datetime', DATETIME_SELECTOR)
        loader.add_css('comments_count', COMMENTS_COUNT_SELECTOR)
        loader.add_value('url', response.url)
        return loader.load_item()

    def extract_uol(self, response):
        CATEGORY_SELECTOR = '.title-content .container h4.title-name::text'
        TITLE_SELECTOR = 'article header h1 .h-external::text, '\
                         'article header h1 .custom-title::text'
        AUTHOR_SELECTOR = 'article .author .p-author::text'
        LOCATION_SELECTOR = 'article .author .p-author-local::text'
        DATETIME_SELECTOR = 'article .author .p-author.time::attr("ia-date-publish")'
        COMMENTS_COUNT_SELECTOR = 'article .comments-total h4 strong::text'

        loader = ItemLoader(item=UolItem(), response=response)
        loader.add_css('title', TITLE_SELECTOR)
        loader.add_css('author', AUTHOR_SELECTOR)
        loader.add_css('category', CATEGORY_SELECTOR)
        loader.add_css('location', LOCATION_SELECTOR)
        loader.add_css('datetime', DATETIME_SELECTOR)
        loader.add_css('comments_count', COMMENTS_COUNT_SELECTOR)
        loader.add_value('url', response.url)
        return loader.load_item()

    def extract_blogosfera(self, response):
        CATEGORY_SELECTOR = '.blog-header h1::text'
        TITLE_SELECTOR = 'article header h1 .h-external::text, '\
                         'article header h1 .custom-title::text'
        AUTHOR_SELECTOR = 'article .author .p-author::text'
        LOCATION_SELECTOR = 'article .author .p-author-local::text'
        DATETIME_SELECTOR = 'article .author .p-author.time::attr("ia-date-publish")'
        COMMENTS_COUNT_SELECTOR = 'article .comments-total h4 strong::text'

        loader = ItemLoader(item=UolItem(), response=response)
        loader.add_css('title', TITLE_SELECTOR)
        loader.add_css('author', AUTHOR_SELECTOR)
        loader.add_css('category', CATEGORY_SELECTOR)
        loader.add_css('location', LOCATION_SELECTOR)
        loader.add_css('datetime', DATETIME_SELECTOR)
        loader.add_css('comments_count', COMMENTS_COUNT_SELECTOR)
        loader.add_value('url', response.url)
        return loader.load_item()
