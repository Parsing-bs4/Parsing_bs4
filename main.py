import csv
import requests
from bs4 import BeautifulSoup


URL = 'https://www.olx.ua/nedvizhimost/kvartiry/kiev/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
HOST = 'https://www.olx.ua'
FILE = 'offers.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='block br3 brc8 large tdnone lheight24')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='offer-wrapper')
    offer = []
    for item in items:
        """uah_price = item.find('p', class_='price')
        if uah_price:
            uah_price = uah_price.get_text()
        else:
            uah_price = 'No price'"""
        offer.append({'title': item.find('strong').get_text(strip=True),
                      'link': item.find('a').get('href'),
                      'price': item.find('p', class_='price').get_text().replace('\n1' and '\n', ''),
                      #'price_uah': uah_price,
                      })
    return offer


def save_file(items, path):
    with open(path, 'w', newline='', errors='ignore') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Назва оголошення', 'Посилання', 'Ціна'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['price']])


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        offer = []
        pages_count = get_pages(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсінг сторінки {page} із {pages_count}')
            html = get_html(URL, params={'page': page})
            offer.extend(get_content(html.text))
        save_file(offer, FILE)
        print(f'Получено оголошень', (len(offer)))
    else:
        print('err')


parse()