import schedule
import time
import logging
import datetime
import my_parser.pars as pars
import data_processing.data_processing as data_proc
from save_data import save_to_csv as save


# Настройка логирования
logging.basicConfig(level=logging.INFO)


def task():
    """Функция для парсинга сайта и обработки скаченных данных"""
    #Определяется сегодняшняя дата для формирования названия файла
    filename_date = datetime.date.today().isoformat()
    # Функция парсинга целевого сайта
    data_dict = pars.parse_site(logging)
    # Сохранение скаченных данных в папке new_data
    save.dict_to_scv(data_dict, filename_date, logging)
    # Функция обработки данных
    data_df = data_proc.processing_data(filename_date, logging)
    #Сохранение обработанных данных в папке data_processing
    save.df_to_scv(data_df, filename_date, logging)

def start_schedule():
    """Функция для автоматического запуска парсинга в 19:00"""
    schedule.every().day.at("19:00").do(task)

    #Запуск бесконечного цикла с периодичностью 1 секунда
    while True:
        schedule.run_pending()
        time.sleep(1)


# Запуск планировщика задач
start_schedule()
