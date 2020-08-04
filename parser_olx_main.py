from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import requests
from selenium.webdriver.firefox.options import Options
import time
from random import randint


class OlxParser:
    def __init__(self, urls):
        self.urls = urls
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

    @staticmethod
    def write_csv(data):
        with open('olx.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow((data['name'], data['price'], data['address'], data['phone']))

    @staticmethod
    def comma_deleter(text_data):
        if ',' in text_data:
            text_data = ' '.join(text_data.split(','))
            return text_data
        return text_data

    def parse(self):
        first_time_check = True
        count = 230
        for url in self.urls:
            if first_time_check:
                html = self.get_html(url, cookie_click=True)
                if html:
                    data = self.extract_data(html)
                    self.write_csv(data)
                    count += 1
                    first_time_check = False
                continue
            else:
                html = self.get_html(url)
                if html:
                    data = self.extract_data(html)
                    self.write_csv(data)
                    count += 1
                continue
        self.driver.quit()

    def get_html(self, url, cookie_click=False):
        time.sleep(randint(1, 5))
        self.driver.get(url)
        if cookie_click:
            cookie_button = self.driver.find_element_by_xpath('//button[@class="cookie-close abs cookiesBarClose"]')
            cookie_button.click()
        try:
            phone_button = self.driver.find_element_by_xpath('//strong[@class="xx-large"]')
            html = ''
            count = 0
            while not html:
                if count == 10:
                    return False
                try:
                    count += 1
                    phone_button.click()
                    phone_button.click()
                    phone_button.click()
                    time.sleep(5)
                    html = self.driver.page_source
                    return html
                except:
                    continue
        except:
            return False

    def extract_data(self, html):
        soup = BeautifulSoup(html, 'lxml')

        phone = soup.find('strong', class_="xx-large").text.strip()
        phone = self.comma_deleter(phone)

        address = soup.find('address').find('p').text.strip()
        address = self.comma_deleter(address)

        price = soup.find('div', class_="pricelabel").find('strong').text.strip()
        price = self.comma_deleter(price)

        name = soup.find('div', class_="offer-titlebox").find('h1').text.strip()
        name = self.comma_deleter(name)

        data = {'name': name, 'price': price,
                'address': address, 'phone': phone}

        return data


links = list()

for i in range(1, 11):
    url = f'https://www.olx.ua/list/q-iphone-11/?search%5Bfilter_float_price%3Afrom%5D=10000&page={i}'
    time.sleep(randint(1, 5))
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'lxml')

    a_tags = soup.find_all('a', class_="marginright5 link linkWithHash detailsLink")

    for a_tag in a_tags:
        url = a_tag.get('href')
        links.append(url)


olx_parser = OlxParser(links)
olx_parser.parse()
