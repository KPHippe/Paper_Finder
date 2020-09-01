import re
import json

import requests
from bs4 import BeautifulSoup

class ArXiv:
    '''
    This class scrapes the new CS articles from ArXiv
    '''
    url = 'https://arxiv.org/list/cs/new'
    config_path = './.config/scraper_config.json'
    def __init__(self):
        '''
        Upon initialization, we load the search words and also scrape
        ArXiv.
        '''
        self.all_articles = {}
        self.selected_articles = {}
        self.key_terms = json.load(open(self.config_path))['ArXiv']

        self.selected_articles['keywords'] = self.key_terms

        self._scrape()
        self._find_relevant_articles()


    def _scrape(self):
        '''
        This method is responsible for scraping ArXiv and loading the relevant
        articles into the dictionary field.

        Parameters:
        ----------
        None: This method only needs its instance variables

        Returns:
        ---------
        None: This method just sets values to a field variable

        '''
        arxiv_page = requests.get(self.url)
        arxiv_page.encoding = 'ISO-885901'
        soup = BeautifulSoup(arxiv_page.text, 'html.parser')

        dl_data = soup.find_all('dl')
        for dlitem in dl_data:
            for dt_item, dd_item in zip(dlitem.find_all('dt'), dlitem.find_all('dd')):
                #^\[.+\]$ matches any string with a "[" at the beginning, one or more characters, and a "]" at the end
                hash_num = int(json.loads((dt_item.find('a', text=re.compile("^\[.+\]$")).text))[0])
                title = (dd_item.find('div', class_='list-title mathjax').text.split('Title: ')[1]).strip().replace("  ", ' ')
                try:
                    #some articles do not have a PDF link, we explude these articles
                    url = 'https://arxiv.org' + (dt_item.find('a', title="Download PDF", href=True)['href'])
                except TypeError:
                    print(f"Title: '{title}' has no PDF download...")
                self.all_articles[hash_num] = {'title': title, 'url': url}


    def _find_relevant_articles(self):
        '''
        This method searches the relevant articles for keywords that come from the
        JSON config

        There are no parameters or returns, it sets field variables


        TODO: use REGEX or a more powerful pattern matcher to find patterns
        '''
        for article_hash, data_dictionary in self.all_articles.items():
            title = data_dictionary['title']
            url = data_dictionary['url']
            for key_term in self.key_terms:
                #we are looking for this pattern anywhere in this string
                #TODO: update to regex
                if key_term.lower() in title.lower():
                    if article_hash not in self.selected_articles.keys():
                        self.selected_articles[article_hash] = {'title': title, 'url': url}
                        continue

    def get_selections(self):
        '''
        Getter to see the selected articles
        '''
        return self.selected_articles

if __name__ == '__main__':
    scraper = ArXiv()

    print(len(scraper.get_selections()))
    print(scraper.get_selections())
