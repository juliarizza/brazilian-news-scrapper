import requests
from bs4 import BeautifulSoup

class Homepage:
    def __init__(self, url):
        self.url = url
        self._html = None

    def get_html(self):
        try:
            response = requests.get(self.url)
            self._html = response.text
            return self._html
        except:
            return ''

    def get_soup(self):
        return BeautifulSoup(self.get_html(), 'html.parser')
    
    def get_version(self):
        if self._is_v1():
            return 'V1'
        elif self._is_v2():
            return 'V2'
        else:
            return None

    def _is_v1(self):
        return bool(self.get_soup().find(id='conteudo'))

    def _is_v2(self):
        pass

class HomepageV1(Homepage):
    def __init__(self, url):
        Homepage.__init__(self, url)
        self.links = []

    def _verify_conditions(self, link):
        cond_1 = link.parent.get('id') == 'topo-direita'
        cond_2 = link.parent.parent.get('id') == 'mod-horz-top'
        cond_3 = link.get('name') == 'tempo'
        cond_4 = '-chapeu' in link.get('name', '')
        cond_5 = '-canais' in link.get('name', '')

        return not (cond_1 or cond_2 or cond_3 or cond_4 or cond_5)

    def _find_links(self):
        links = []
        news = self.get_soup().find(id='conteudo')
        for link in news.find_all('a'):
            if self._verify_conditions(link):
                links.append(link.get('href'))
        self.links = links

    def get_links(self):
        self._find_links()
        return self.links


    