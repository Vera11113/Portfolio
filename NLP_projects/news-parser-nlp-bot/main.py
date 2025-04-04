import logging
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from dataclasses import dataclass
from datetime import datetime
import re
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')  # Отключение GPU для стабильности
options.add_argument('--window-size=1920,1080')  # Фиктивный размер окна

@dataclass
class Article:
    id: int = None
    url: str = None
    title: str = None
    subtitle: str = None
    summary: str = None
    content: str = None
    datetime: str = None

TOPICS = ['world', 'russia', 'business', 'sport', 'science']
SLEEP = 2
DEPTH = 166
BASE_URL = 'https://russian.rt.com/'

logging.basicConfig(
    filename = 'parser.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

browser = webdriver.Chrome(options=options)

def get_pages():


    items, topics_order = [], []
    for topic in TOPICS:
        URL = BASE_URL+topic
        print(URL)
        browser.get(URL)

        for i in tqdm(range(DEPTH)):
            try:
                button = WebDriverWait(browser, 30).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.button__item.button__item_listing'))
                )

                # Прокручиваем к элементу
                browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)

                # Кликаем через ActionChains (имитация реального взаимодействия)
                ActionChains(browser).move_to_element(button).click().perform()

            except TimeoutException:
                logging.exception('TimeoutException')
                break

        links = browser.find_elements(By.CLASS_NAME, 'listing__card.listing__card_sections ')
        for link in links:
            url_link = link.find_element(By.CSS_SELECTOR, '.card__heading').find_element(By.CSS_SELECTOR, '.link').get_attribute('href')
            items.append(url_link)

        topics_order.extend([topic] * len(links))
        print(f"Тема '{topic}': найдено {len(links)} статей")

    print(f"Итого собрано: {len(items)} статей")
    return items, topics_order

def parse_page(page):

        article = Article()
        article.url = page
        match = re.search('\d+', str(article.url))
        article.id = int(match.group())

        browser.get(page)

        try:
            article.title = browser.find_element(By.CSS_SELECTOR, '.article__heading').text
        except Exception as err:
            logging.exception('Title error')
            article.title = ''

        try:
            subtitle_elems = WebDriverWait(browser, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.article__subtitle'))
            )
            article.subtitle = subtitle_elems[0].text if subtitle_elems else ''
        except Exception as err:
            logging.error('Subtitle not found', exc_info=True)
            article.subtitle = ''

        try:
            date_string = browser.find_element(By.CLASS_NAME, 'date').get_attribute('datetime')
            article.datetime = datetime.strptime(date_string, '%Y-%m-%d %H:%M')
        except Exception as err:
            logging.exception('Datetime error')
            article.datetime = ''
        try:
            article.summary = browser.find_element(By.CSS_SELECTOR, '.article__summary').text
        except Exception as err:
            logging.exception('Summary error')
            article.summary = ''
        try:
            article.content = browser.find_element(By.CSS_SELECTOR, '.article__text').text
        except Exception as err:
            logging.exception('Content error')
            article.content = ''

        return article




items, topics_order = get_pages()
data, topics_order_fixed = [], []

for num, item in enumerate(tqdm(items)):

    res = parse_page(item)
    data.append(res)
    topics_order_fixed.append(topics_order[num])

browser.quit()

df = pd.DataFrame(data = data)
df['topic'] = topics_order_fixed
print(df.head())

df.to_csv('articles.csv', index=False, encoding='utf-8')
