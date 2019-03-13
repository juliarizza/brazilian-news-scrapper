import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString

class News:
    def __init__(self, url):
        self.title = None
        self.category = None
        self.author = None
        self.date = None
        self.location = None
        self.source = None
        self.url = url

        self._html = ''
        self._soup = self.get_soup()

    def get_html(self):
        try:
            response = requests.get(self.url)
            self._html = response.text
            return self._html
        except:
            raise Exception('Not available')

    def get_soup(self):
        self._soup = BeautifulSoup(self.get_html(), 'html.parser')
        return self._soup

    def get_version(self):
        if self._is_uol_noticias():
            return 'UOL NOTICIAS'
        elif self._is_folha_sao_paulo():
            return 'FOLHA SAO PAULO'
        else:
            return None

    def _is_uol_noticias(self):
        return 'noticias.uol.com.br' in self.url

    def _is_folha_sao_paulo(self):
        return 'folha.uol.com.br' in self.url

class UolNoticiasV1(News):
    def __init__(self, url):
        News.__init__(self, url)
        self.source = 'UOL Notícias'
        self._set_metadata()

    def _set_metadata(self):
        try:
            category_info = self._soup.find(id='barra-estacao')
            self.category = category_info.find(class_='canal').string

            top_info = self._soup.find(id='titulo').find(class_='conteudo')
            self.title = top_info.h1.string
            self.date = top_info.h2.string

            meta = self._soup.find(id='credito-texto')
            if meta:
                news_credits = filter(lambda c: type(c) == NavigableString, meta.contents)
                for data in news_credits:
                    if 'em ' in str(data).lower():
                        self.location = data
                    elif 'no ' in str(data).lower():
                        self.location = data
                    elif 'especial ' in str(data).lower():
                        pass
                    elif 'do ' in str(data).lower():
                        pass
                    else:
                        self.author = data
        except:
            raise Exception('Invalid news format')

    def to_array(self):
        return [self.title, self.category, self.author, self.date,
                self.location, self.url, self.source]

    def to_dict(self):
        return {
            'Title': self.title,
            'Category': self.category,
            'Author': self.author,
            'Date': self.date,
            'Location': self.location,
            'URL': self.url,
            'Source': self.source
        }

