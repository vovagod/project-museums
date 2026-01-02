import requests
import time
import random
from bs4 import BeautifulSoup

headers = {
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 YaBrowser/24.12.0.0 Safari/537.36',
'Accept-Language': 'ru,en;q=0.9',
'Referer': 'https://www.yandex.ru/'
}

#URL = "http://museum-nmsk.ru/about/"
#URL = "https://vladmuseum.ru/"
URL = "https://www.mgomz.ru/"

def parse_page(url):
    time.sleep(random.uniform(1, 3))
    
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Ошибка при доступе к странице: {response.status_code}")
        return

    # Создаем объект BeautifulSoup для парсинга
    soup = BeautifulSoup(response.text, 'html.parser')

    urls = []
    for link in soup.find_all('a'):
        print(link.get('href'))
    
    # Extract text using CSS selectors
    #texts = soup.select('div > p')  # Select all <p> tags inside <div class='content'>
    #for text in texts:
        #print(text.get_text())

    # Extract text from nested tags
    #divs = soup.find_all('div', class_='row')  # Find all <div> tags with class 'content'
    #for div in divs:
        #paragraphs = div.find_all('p')  # Find all <p> tags within each <div class='content'>
    #for p in paragraphs:
        #print(p.get_text())
    #print(S.prettify())

parse_page(URL)
