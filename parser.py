import requests
from bs4 import BeautifulSoup
import csv

HOST = 'https://app.memrise.com'
URL = 'https://app.memrise.com/course/861896/umnyi-slovar-1000-slov/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r
def get_page_links(html):
    adr = []
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        adr.append(HOST + link.get('href'))
    return adr[26:60]
html = get_html(URL)#мы получили список ссылок adr. Теперь нужно по одной обработать каждую ссылку и достать из них нужную информацию.
adr = get_page_links(html.text)

def parse_words(html):
    bsoup = BeautifulSoup(html, 'html.parser')
    things = bsoup.find_all('div', class_='thing text-text')
    keys = []
    items = []
    for thing in things:
        key = thing.find('div', class_='col_a col text')
        keys.append(key.text)
    for thing in things:
        item = thing.find('div', class_='col_b col text')
        items.append(item.text)
    my_dict = dict(zip(keys, items))
    return my_dict

final_dict = {}
for i in range(len(adr)):
    html1 = get_html(adr[i])
    dict_ = parse_words(html1.text)
    final_dict.update(dict_)

with open('output.csv', 'w', encoding='utf-8') as output:
    writer = csv.writer(output)
    for key, value in final_dict.items():
        writer.writerow([key, value])