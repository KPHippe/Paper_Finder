import os
import json
import smtplib
from datetime import date
from email.message import EmailMessage


class Email:
    #configuration variables
    config_path  = './.config/email_config.json'

    def __init__(self):
        config_data = json.load(open(self.config_path))
        self.SENDER_ADDR = config_data['sender_email']
        self.SENDER_PASS = config_data['sender_password']
        self.RECIPIENTS = config_data['recipients']

    def send_articles(self, article_data):
        msg = EmailMessage()
        current_date = date.today().strftime("%b-%d-%Y")
        msg['Subject'] = f'ArXiv {current_date}'
        msg['From'] = self.SENDER_ADDR
        msg['To'] = self.RECIPIENTS
        msg.set_content(self._format_article_data(article_data))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.SENDER_ADDR, self.SENDER_PASS)

            # smtp.sendmail(SENDER, RECEIVER, msg)
            smtp.send_message( msg)



    def _format_article_data(self, article_data):
        ret_list = []

        ret_list.append('Keywords: ' + str(article_data['keywords']) + '\n\n')
        del article_data['keywords']
        for article_hash, article_data in article_data.items():
            article_title = article_data['title']
            article_url = article_data['url']
            ret_list.append(f'{article_title}: {article_url}')

        return "\n".join(ret_list)


if __name__ == '__main__':
    arxiv_emailer = Email()
    data = {
    1: {'title': 'Neural Networks and Quantum Field Theory', 'url': 'https://arxiv.org/pdf/2008.08601'},
    20: {'title': 'Asymptotics of Wide Convolutional Neural Networks', 'url': 'https://arxiv.org/pdf/2008.08675'}
    }
    arxiv_emailer.send_articles(data)
