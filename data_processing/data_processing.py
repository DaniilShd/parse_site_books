import pandas as pd

def read_file(filename):
    path = '../new_data/' + filename
    print(path)
    df = pd.read_csv(path)
    return df

def processing_data(filename, logging):
    # Чтение файла csv
    logging.info("Чтение файла csv")
    df = read_file(filename + '.csv')
    # Перед началом манипуляций над файлом делаю копию dataframe
    df_copy = df.copy()
    # Проверка на дубликаты и подсчет их количества
    count_duplicate = df_copy.duplicated().sum()
    logging.info(f"Количество дубликатов - {count_duplicate}")
    # Удаление дубликатов
    df_copy.drop_duplicates(inplace=True)
    # Проверка на пропущенные значения, определение их количества
    pass_data = df_copy.isna().sum()
    logging.info(f"Количество пропусков - {pass_data}")
    # Замена пропусков на соседние значения
    df_copy.bfill(inplace=True)
    pass_data = df_copy.isna().sum()
    logging.info(f"Количество пропусков после обработки - {pass_data}")
    # Подсчет общего количества книг и вывод на экран
    books_sum = df_copy.shape[0]
    logging.info(f"Количество записей после обработки - {books_sum}")
    print(f"Количество книг - {books_sum}")
    # Вывод статистики на экран
    print(df_copy.describe())
    # Возвращаю обработанные данные
    return df_copy

