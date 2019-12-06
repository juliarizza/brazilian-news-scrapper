import scrapy
import datetime

from uol.utils import daterange, beautify

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
        urls = ["https://noticias.uol.com.br/arquivohome/20111004home_23.jhtm"]
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
        CATEGORY_LINK_SELECTOR = '.section-masthead h1::text'
        ARTICLE_SELECTOR = '#news'
        TITLE_SELECTOR = 'header h1::text'
        AUTHOR_SELECTOR = 'header .author::text'
        LOCATION_SELECTOR = ''
        DATETIME_SELECTOR = 'header time::attr("datetime")'
        COMMENT_COUNT_SELECTOR = '#article-comments header a.more::text'

        article = response.css(ARTICLE_SELECTOR)
        title = article.css(TITLE_SELECTOR).get()
        category = response.css(CATEGORY_SELECTOR).get() or response.css(CATEGORY_LINK_SELECTOR).get()
        
        return {
            "title": beautify(title),
            "author": beautify(article.css(AUTHOR_SELECTOR).get()),
            "category": beautify(category),
            "location": None,
            "datetime": article.css(DATETIME_SELECTOR).get(),
            "comment_count": article.css(COMMENT_COUNT_SELECTOR).get(),
            "url": response.url
        } if title else None

    def extract_uol(self, response):
        CATEGORY_SELECTOR = '.title-content .container h4.title-name::text'
        CATEGORY_LINK_SELECTOR = '.title-content .container h4.title-name a::text'
        ARTICLE_SELECTOR = 'article.article'
        TITLE_SELECTOR = 'header h1 .h-external::text'
        CUSTOM_TITLE_SELECTOR = 'header h1 .custom-title::text'
        AUTHOR_SELECTOR = '.author .p-author::text'
        LOCATION_SELECTOR = '.author .p-author-local::text'
        DATETIME_SELECTOR = '.author .p-author.time::attr("ia-date-publish")'
        COMMENT_COUNT_SELECTOR = '.comments-total h4 strong::text'

        article = response.css(ARTICLE_SELECTOR)
        title = article.css(TITLE_SELECTOR).get() or article.css(CUSTOM_TITLE_SELECTOR).get()
        category = response.css(CATEGORY_SELECTOR).get() or response.css(CATEGORY_LINK_SELECTOR).get()

        return {
            "title": beautify(title),
            "author": beautify(article.css(AUTHOR_SELECTOR).get()),
            "category": beautify(category),
            "location": beautify(article.css(LOCATION_SELECTOR).get()),
            "datetime": article.css(DATETIME_SELECTOR).get(),
            "comment_count": article.css(COMMENT_COUNT_SELECTOR).get(),
            "url": response.url
        } if title else None

    def extract_blogosfera(self, response):
        CATEGORY_SELECTOR = '.blog-header h1::text'
        CATEGORY_LINK_SELECTOR = '.blog-header h1 a::text'
        ARTICLE_SELECTOR = 'article.article'
        TITLE_SELECTOR = 'header h1 .h-external::text'
        CUSTOM_TITLE_SELECTOR = 'header h1 .custom-title::text'
        AUTHOR_SELECTOR = '.author .p-author::text'
        LOCATION_SELECTOR = '.author .p-author-local::text'
        DATETIME_SELECTOR = '.author .p-author.time::attr("ia-date-publish")'
        COMMENT_COUNT_SELECTOR = '.comments-total h4 strong::text'

        article = response.css(ARTICLE_SELECTOR)
        title = article.css(TITLE_SELECTOR).get() or article.css(CUSTOM_TITLE_SELECTOR).get()
        category = response.css(CATEGORY_SELECTOR).get() or response.css(CATEGORY_LINK_SELECTOR).get()

        return {
            "title": beautify(title),
            "author": beautify(article.css(AUTHOR_SELECTOR).get()),
            "category": beautify(category),
            "location": beautify(article.css(LOCATION_SELECTOR).get()),
            "datetime": article.css(DATETIME_SELECTOR).get(),
            "comment_count": article.css(COMMENT_COUNT_SELECTOR).get(),
            "url": response.url
        } if title else None
