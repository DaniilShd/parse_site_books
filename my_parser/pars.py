

import requests
from bs4 import BeautifulSoup
import re
import time

def parse_site(logging):
    count_page = 49
    # Создаю список куда будет записана вся скаченная информация (список)
    result_info_books = []
    # Запускаю бесконечный цикл для прохода по всем страницам сайта
    while True:
        # Увеличиваю номер страницы на 1
        count_page += 1
        logging.info(f"Запуск функции парсинга сайта - итерация {count_page}")
        url = f"https://books.toscrape.com/catalogue/page-{count_page}.html"
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response.encoding = 'utf-8'
            if response.status_code == 404:
                logging.info(f"Дошли до страницы, "
                             f"которой не существует - итерация {count_page}")
                return result_info_books
                break
            page = BeautifulSoup(response.text, 'html.parser')
            title_books = page.find("section").find_all('h3')
            logging.info("Запуск цикла по страничкам книг")
            for title_book in title_books:
                # Запуск функции парсинга странички книги
                book_info = parse_book_page(title_book, logging)
                # Запись результата парсинга в список
                result_info_books.append(book_info)
            logging.info(f"Парсинг страницы {count_page} закончен")
        except Exception as err:
            print(err)
            break


def parse_book_page(title_book, logging):
    # Создаю словарь для данных по каждой книге
    book_info = dict()
    # Формирование url для каждой странички книги
    url_page_book = ('https://books.toscrape.com/catalogue/'
                     + title_book.find('a', href=True).get('href'))
    # Отправка get запроса по заданному url и заданным параметрам head.
    # Выполняется через try
    try:
        response = requests.get(url_page_book,
                                headers={'User-Agent': 'Mozilla/5.0'})
    except requests.ConnectionError as e:
        logging.info(f"Возникла ошибка - {e}")
        return
    # Прочтение ответа библиотекой BeautifulSoup
    page = BeautifulSoup(response.text, 'html.parser')
    # Название книги, выполняется через проверку.
    # Если названия книги нет записывается пустая строка
    if page.find("h1"):
        name_book = page.find("h1").text
        book_info['Name book'] = name_book
    else:
        book_info['Name book'] = None
    # Цена книги, выполняется через проверку.
    # Если цены нет записывается None
    if page.find('p', attrs="price_color"):
        price = page.find('p', attrs="price_color").text
        book_info['Price'] = float(price[2:])
    else:
        book_info['Price'] = None
    # Рейтинг книги, выполняется через проверку.
    # Если рейтинга нет записывается None
    if page.find('p', attrs="star-rating"):
        rating_stars = page.find('p', attrs="star-rating").attrs['class'][1]
    else:
        book_info['Rating'] = None
    if rating_stars == "One":
        book_info['Rating'] = 1
    elif rating_stars == "Two":
        book_info['Rating'] = 2
    elif rating_stars == "Three":
        book_info['Rating'] = 3
    elif rating_stars == "Four":
        book_info['Rating'] = 4
    elif rating_stars == "Five":
        book_info['Rating'] = 5
    # Определение количества книг на складе.
    # Если нет значения записывается None
    if page.find('p', attrs="instock availability"):
        count_text = page.find('p', attrs="instock availability").text
        count = int(re.findall('(\d+)', count_text)[0])
        book_info['Count'] = count
    else:
        book_info['Count'] = None
    # Скачивание текста описания книги.
    # Если нет описания записывается пустая строка
    if page.find(id='product_description'):
        description = (page.find(id='product_description')
                       .find_next('p').text)
    else:
        description = None
    book_info['Product description'] = description
    # Скачивание таблицы с данными о книге
    tr = page.find('table', attrs='table table-striped')
    # Строка UPC
    if tr.select('td')[0]:
        book_info['UPC'] = tr.select('td')[0].text
    else:
        book_info['UPC'] = None
    # Строка Product Type
    if tr.select('td')[1]:
        book_info['Product Type'] = tr.select('td')[1].text
    else:
        book_info['Product Type'] = None
    # Строка Price (excl. tax)
    if tr.select('td')[2]:
        book_info['Price (excl. tax)'] = float(tr.select('td')[2].text[2:])
    else:
        book_info['Price (excl. tax)'] = None
    # Строка Price (incl. tax)
    if tr.select('td')[3]:
        book_info['Price (incl. tax)'] = float(tr.select('td')[3].text[2:])
    else:
        book_info['Price (incl. tax)'] = None
    # Строка Tax
    if tr.select('td')[4]:
        book_info['Tax'] = float(tr.select('td')[4].text[2:])
    else:
        book_info['Tax'] = None
    # Строка Availability
    if tr.select('td')[5]:
        count_text = tr.select('td')[5].text
        count = int(re.findall('(\d+)', count_text)[0])
        book_info['Availability'] = count
    else:
        book_info['Availability'] = None
    # Строка Number of reviews
    if tr.select('td')[6]:
        book_info['Number of reviews'] = int(tr.select('td')[6].text)
    else:
        book_info['Number of reviews'] = None
    # Задержка в выполнении запросов к сайту
    time.sleep(0)
    # Возвращается словарь с данными о книге
    return book_info
