import requests
import sqlite3
from time import sleep
from bs4 import BeautifulSoup


class BaseParser:
    def __init__(self, url):
        self.url = url
        self.raw_html = None
        self.bulk_data = list()
        self.is_active = False
        

    def work(self):
        self.is_active = True
        while self.is_active:
            if self.get_html():
                self.parse_html()
            if len(self.bulk_data) > 0:
                self.save_data()

            sleep(10)

    def get_html(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                self.raw_html = response.text
                return True
            else:
                print(f'Failed to get HTML, code {response.status_code}:\n{response.text}')
                return False
        except Exception as e:
            print(f'Failed to get HTML, code {e}')

    def parse_html(self):
        raise NotImplementedError('Use parse_html method from child')

    def save_data(self):
        with sqlite3.connect('news.db') as conn:
            cursor = conn.cursor()
            for item in self.bulk_data:
                try:
                    headline = item['headline']
                    tag = item['tag']
                    date = item['date']
                except KeyError:
                    continue
                else:
                    cursor.execute(f'INSERT INTO news VALUES (\'{headline}\', \'{tag}\', \'{date}\')')
            conn.commit()
        self.bulk_data.clear()
        print('Data saved to db')


class NVParser(BaseParser):
    def __int__(self, url):
        super().__init__(url=url)

    def parse_html(self):
        soup = BeautifulSoup(self.raw_html, 'lxml')
        one_results = soup.find_all('div', attrs={'class': 'one_result'})

        for result in one_results:
            record = dict()
            raw_headline = result.find('span', attrs={'class': 'search__article_title'})
            record['headline'] = raw_headline.get_text()

            raw_tag = result.find('span', attrs={'class': 'atom__additional_category'})
            record['tag'] = raw_tag.get_text()

            raw_date = result.find('div', attrs={'class': 'atom__additional_pubDate'})
            record['date'] = raw_date.get_text()
            print(record)
            self.bulk_data.append(record)


def create_db():
    try:
        conn = sqlite3.connect('news.db')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE news (headline, tag, date)')
        conn.commit()
        conn.close()
    except Exception as e:
        print('DB is already there')


nv_url = 'https://nv.ua/allnews.html'
nv_parser = NVParser(nv_url)
nv_parser.work()