import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import csv
import time
import pickle

class AvitoParse():
    def __init__(self, url: str, items: list, count: int = 100):
        self.url = url
        self.count = count
        self.items = items
        self.data = []
        self.driver = None

    def __set_up(self):
        self.options = uc.ChromeOptions()
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")
        self.driver = uc.Chrome(options=self.options)

    def __get_url(self):

        self.driver.get("https://www.avito.ru")
        time.sleep(3)
        with open("avito_cookies.pkl", "rb") as file:
            cookies = pickle.load(file)

        for cookie in cookies:
            self.driver.add_cookie(cookie)

        self.driver.get("https://www.avito.ru")
        time.sleep(3)

        self.driver.get(self.url)
        time.sleep(5)

    def __paginator(self):
        while self.count > 0:
            self.__parse_page()  # Парсим текущую страницу

            try:
                next_page_button = self.driver.find_element(By.CSS_SELECTOR,
                                                            "[data-marker='pagination-button/nextPage']")
                next_page_url = next_page_button.get_attribute("href")  # Берем ссылку на след. страницу

                if next_page_url:
                    self.driver.get(next_page_url)  # Переходим на следующую страницу
                    time.sleep(5)  # Ждем загрузки
                    self.count -= 1
                    self.url = next_page_url
                else:
                    break  # Если нет ссылки — выходим из цикла

            except Exception as e:
                print(f"Ошибка при переходе на следующую страницу: {e}")
                break  # Если кнопки "Следующая" нет, останавливаем парсинг

    def __parse_page(self):
        product_links = []  # Храним список URL

        # Сбор списка товаров
        titles = self.driver.find_elements(By.CSS_SELECTOR, "[data-marker='item']")
        for title in titles:
            try:
                item = title.find_element(By.CSS_SELECTOR, '[data-marker="item-title"]')
                name = item.text
                url = item.get_attribute('href')
                price = title.find_element(By.CSS_SELECTOR, '[itemprop="price"]').get_attribute('content')

                if any([keyword.lower() in name.lower() for keyword in self.items]):
                    product_links.append((name, url, price)) # Сохраняем в список
                    print(name, url, price)

            except Exception as e:
                print(f"Ошибка при получении ссылки: {e}")

        # Теперь переходим на каждую страницу товара
        for name, url, price in product_links:
            try:
                print(url)
                self.driver.get(url)
                # Ждем загрузки
                time.sleep(3)

                # Парсим данные
                views_cnt = \
                self.driver.find_element(By.CSS_SELECTOR, '[data-marker="item-view/total-views"]').text.split()[
                    0].strip()
                city = self.driver.find_element(By.CSS_SELECTOR, '[class*="style-item-address__string"]').text.strip()
                seller = self.driver.find_element(By.CSS_SELECTOR,
                                                  '[data-marker="item-view/seller-info"]').find_element(By.CSS_SELECTOR,
                                                                                                        'span').text.strip()

                try:
                    seller_rating = driver.find_element(By.CSS_SELECTOR,
                                                        '[class="style-seller-info-value-vOioL"]').find_element(
                        By.CSS_SELECTOR, '[class="styles-module-size_m-n6S6Y"]').text.strip()
                    seller_rating = float(seller_rating.replace(',', '.'))
                except:
                    seller_rating = None

                try:
                    comments_cnt = \
                    self.driver.find_element(By.CSS_SELECTOR, '[data-marker="rating-caption/rating"]').text.split()[0]
                except:
                    comments_cnt = 0

                # Добавляем в список
                self.data.append({
                    'name': name,
                    'price': float(price.replace(',', '.')),
                    'url': url,
                    'views_cnt': int(views_cnt),
                    'city': city,
                    'seller': seller,
                    'seller_rating': seller_rating,
                    'comments_cnt': int(comments_cnt)
                })



            except Exception as e:
                print(f"Ошибка при парсинге {name}: {e}")

        # Сохраняем данные в файл
        self.__save_data()
        self.driver.get(self.url)

    def __save_data(self):
        # Открываем файл для записи
        with open("ethno_jewelery.csv", 'a', newline='', encoding='utf-8-sig') as file:
            # Создаем объект writer
            writer = csv.DictWriter(file, fieldnames=['name', 'price', 'url', 'views_cnt', 'city', 'seller', 'seller_rating', 'comments_cnt'])

            # Записываем заголовки
            if file.tell() == 0:
                writer.writeheader()

            # Записываем данные
            writer.writerows(self.data)
        self.data = []

    def parse(self):
        self.__set_up()
        self.__get_url()
        self.__paginator()
        self.driver.quit()

if __name__ == '__main__':
    AvitoParse(
        url = 'https://www.avito.ru/moskva/lichnye_veschi?q=%D1%8D%D1%82%D0%BD%D0%BE+%D1%83%D0%BA%D1%80%D0%B0%D1%88%D0%B5%D0%BD%D0%B8%D1%8F',
        items = ['кольц', 'этно', 'украшен', 'серг', 'сережк', 'этническ'],
        count = 10
    ).parse()