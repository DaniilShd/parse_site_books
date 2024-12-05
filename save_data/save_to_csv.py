import csv
import pandas as pd

# Функция записи данных в файл csv из словаря
def dict_to_scv(list_result, filename, logging):
    """Функция сохранения словаря в файл csv"""
    # Наименование столбцов для будущей таблицы csv
    list_heads = ['Name book', 'Price', 'Rating', 'Count',
                  'Product description', 'UPC', 'Product Type',
                  'Price (excl. tax)', 'Price (incl. tax)', 'Tax',
                  'Availability', 'Number of reviews']

    # Запись в файл выполняется через блок try
    try:
        # Попытка сохранения данных в файл csv
        logging.info("Попытка сохранения данных в файл csv")
        with open('../new_data/' + filename + '.csv', 'w', newline='', encoding="utf-8") as result:
            writer = csv.writer(result)
            writer.writerow(list_heads)
            for item in list_result:
                list_res = []
                for value in item.values():
                    list_res.append(value)
                writer.writerow(list_res)
        logging.info("Файл успешно записан и сохранен в формате csv")
    except Exception as err:
        print(err)


# Функция записи данных в файл csv из dataframe
def df_to_scv(data_df, filename, logging):
    # Запись файла DataFrame в csv
    try:
        data_df.to_csv('../processed_data/' + filename + '.csv')
    except Exception as err:
        logging.error(f"Ошибка записи фаула df - {err}")
    logging.info("Файл успешно записан и сохранен в формате csv")
