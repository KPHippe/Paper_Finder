from Email import Email
from Scraper import ArXiv

def main():
    ArXiv_Scraper = ArXiv() #arxiv scraper, scrapes upon initialization
    Emailer = Email() #emailing class


    arxiv_articles = ArXiv_Scraper.get_selections()
    Emailer.send_articles(arxiv_articles)


if __name__ == '__main__':
    main()
