'''Скрипт генерирует тестовые данные о покупке
с последующем сохранение в файл csv'''
from csv import DictWriter
from datetime import timedelta, date
from random import randint, choice, randrange


# Настройка генерации
# ------------------------------------------------------------------------------
FILE_NAME = 'data/data_100'  # Название файла
COUNT_ROW = 1000  # Кол-во сгенерированных строк

PRODUCTS = {'яблоко': 15, 'груша': 11, 'слива': 15,
            'печенье': 23, 'конфета': 22}  # список продуктов {Название: Цена}
COUNTS_PRODUCT_RANGE = (1, 20)  # Диапазон кол-ва (от, до)
PRICE_PRODUCT_RANGE = (10, 25)  # Диапазон цены (от, до)
DATE_RANGE = (date(2024, 6, 1), date(2024, 6, 30))  # Диапазон дат (от, до)
# ------------------------------------------------------------------------------


def random_date(start_date: date, end_date: date) -> date:
    '''Функция возращает рандомноую дату из 2-ух дат'''
    delta = end_date - start_date
    int_delta = (delta.days * 24 * 60 * 60)
    random_second = randrange(int_delta)
    return start_date + timedelta(seconds=random_second)


def get_product() -> dict:
    '''Функция возвращает информацию о покупке в виде словаря
    со следующими ключами (название, количество, цена, дата)'''
    product_name = choice(tuple(PRODUCTS))
    return {
        'product_name': product_name,
        'quantity': randint(*COUNTS_PRODUCT_RANGE),
        'price': PRODUCTS[product_name],
        'date': random_date(*DATE_RANGE)
    }


def generate_file(file_name: str = 'data', count_row: int = 1) -> None:
    '''Функция создаёт файл и заполняет рандомными данными'''
    with open(f"{file_name}.csv", mode='w', encoding='UTF-8') as file_csv:
        headers = ('product_name', 'quantity', 'price', 'date')
        writer = DictWriter(file_csv, fieldnames=headers)
        # writer.writeheader() # запись названий заголовков
        for _ in range(count_row):
            writer.writerow(get_product())
# ------------------------------------------------------------------------------


# start programm
generate_file(FILE_NAME, COUNT_ROW)
