import asyncio
import requests
import json
import time
import random
import logging
from bs4 import BeautifulSoup
from typing import Optional

from museums.config import BASE_DIR

logger = logging.getLogger(__name__)

LINK = BASE_DIR + "/data/train_expositions.json"

HEADERS = {
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 YaBrowser/24.12.0.0 Safari/537.36',
'Accept-Language': 'ru,en;q=0.9',
'Referer': 'https://www.yandex.ru/'
}


class ReadSourceData:
    ''' Класс чтения json-файла '''

    def __init__(self, link: str = LINK):
        self.link = LINK

    def read_json_file(self): # -> Optional[dict[], dict[str, list[dict[str, str]]]]:
        data = {}
        try:
            with open(self.link, "r", encoding="utf-8") as file:
                data.update(json.load(file))
        except Exception as exc:
            logger.error(f"Ошибка чтения файла: {exc}")
            raise ValueError
        return data

class ParseWebPages:
    ''' Класс извлечения информации из веб-страниц '''

    def __init__(self, urls_list: dict) -> None:
        self.urls_list = urls_list

    def get_web_pages(self) -> list[str]:
        web_pages = [page for val in self.urls_list.values() for page in val]
        #print(f"WEB_PAGES: {web_pages}")
        #return ["http://museum-nmsk.ru/about/", "https://www.mgomz.ru/ru/excursion/zimnyaya-skazka-v-kolomenskom"]
        return web_pages

    def fetch(self, pack: dict) -> Optional[str]:
        ''' Выполнение запроса к странице '''
        
        *_, url, _, class_name = pack.values()
        logger.info(f"Выполняем запрос к странице: {url}...")
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            logger.error(f"Ошибка доступа к странице: {response.status_code}")
            return
        # Подключаем html.parser
        soup = BeautifulSoup(response.text, 'html.parser')
        content = ""
        # Находим все <div> теги с именем класса <class_name>
        divs = soup.find_all('div', class_=class_name)
        for div in divs:
            # Находим все <p> теги в выбранном классе
            paragraphs = div.find_all('p') if div.find_all('p') else div
            #print(f"PARAGRAPHS: {paragraphs}")
            for p in paragraphs:
                # Извлекаем текст
                chunk = p.get_text().strip() + " "
                #chunk = chunk.replace("\xa0", "").replace("\t", "").replace("\n", "").replace("\r", "") 
                chunk = chunk.replace("Скрыть", "").replace("Подробнее...", "") # development
                #print(f"P: {chunk}")
                content += "".join(chunk)

        # Extract text using CSS selectors
        #texts = soup.select('div > p')  # Select all <p> tags inside <div class='content'>
        #content = ""
        #for text in texts:
            #print(text.get_text())
            #content += "".join(text.get_text())
            #info.append(text.get_text())
        #print(f"blocking_io complete at {time.strftime('%X')}")
        logger.info(f"Содержание страницы: {url} получено...")
        return content

    async def fetch_all(self):
        ''' Ассинхронный движок запросов '''
        logger.info(f"Запуск движка запросов страниц...")
        result = [
            await asyncio.gather(
                asyncio.to_thread(self.fetch, pack),
                return_exceptions = True
                ) for pack in self.get_web_pages()
            ]
        logger.info(f"Остановка движка запросов страниц...")
        print(f"RESULT: {result}")
        return result


async def run_process():

    # Чтение файла в ReadSourceData
    try:
        data = ReadSourceData().read_json_file()
        #data = data.read_json_file()
        print(f"DATA: {data}")
    except ValueError:
        return

    # Инициализация ParseWebPages
    init = ParseWebPages(data) 

    # Получение списка url-ов страниц
    init.get_web_pages()

    # Выполнение запросов
    parsed_data = await init.fetch_all()

    # Запись текста в файл
    with open(BASE_DIR + "/data/train_result.txt", "w", encoding="utf-8") as f:
        f.write(parsed_data[1][0])


if __name__ == "__main__":
    asyncio.run(run_process())
            