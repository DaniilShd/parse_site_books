import schedule
import time
import logging
import datetime
import my_parser.pars as pars
import data_processing.data_processing as data_proc
from save_data import save_to_csv as save


# Настройка логирования
logging.basicConfig(level=logging.INFO)


# res = pars.parse_site(logging)
#
#
current_date = datetime.date.today().isoformat()
#
#
# save.dict_to_scv(res, current_date, logging)


filename = f"{current_date}.csv"

data_proc.processing_data(filename, logging)


def task():
    current_date = datetime.date.today().isoformat()
    data_dict = pars.parse_site(logging)
    save.dict_to_scv(data_dict, current_date, logging)


def start_schedule():
    schedule.every().day.at("19:00").do(task)

    while True:
        schedule.run_pending()
        time.sleep(1)


start_schedule()
