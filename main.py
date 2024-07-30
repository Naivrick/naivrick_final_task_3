import csv
from datetime import datetime as dt
from decimal import Decimal
import matplotlib.pyplot as plt


def read_sales_data(file_path: str) -> list[dict]:
    '''Функция принимает путь к CSV файлу и возвращает список словарей
    со следующими ключами (название, количество, цена, дата)'''
    # --- Открытие CSV с дальнешим считыванием ---
    with open(file_path, mode='r', encoding='UTF-8') as file_data:
        headers = ('product_name', 'quantity', 'price', 'date')
        dictReader = csv.DictReader(
            file_data, fieldnames=headers, delimiter=',')

        # --- Перевод 'сырых' данных в удобные типы данных --
        products = list()
        for item in dictReader:
            values = (
                item['product_name'].strip(),  # название
                int(item['quantity'].strip()),  # количество
                Decimal(item['price'].strip()),  # цена
                dt.fromisoformat(item['date'].strip())  # дата
            )

            product = dict(zip(headers, values))
            products.append(product)

        # --- Возврат обработанных данных ---
        return products


def total_sales_per_product(sales_data: list[dict]) -> dict:
    '''Функция принимает список продаж и возвращает словарь,
    где ключ - название продукта, а значение - общая сумма продаж этого продукта.'''
    result = dict()
    for product in sales_data:
        name_product = product['product_name']
        price_product = product['price']

        result.setdefault(name_product, 0)
        result[name_product] += price_product
    return result


def sales_over_time(sales_data: list[dict]) -> dict:
    '''Функция принимает список продаж и возвращает словарь,
    где ключ - дата, а значение общая сумма продаж за эту дату.'''
    result = dict()
    for product in sales_data:
        date = product['date']
        price_product = product['price']
        result.setdefault(date, 0)
        result[date] += price_product
    return result


def draw_all_sum_products(sales_data: dict) -> None:
    '''График общей суммы продаж по каждому продукту.'''
    fig, ax = plt.subplots()
    plt.style.use('seaborn-v0_8-white')
    data = zip(*sorted(sales_data.items(), key=lambda x: x[1]))
    bar = ax.bar(*data, width=0.8, edgecolor="white")

    ax.set(xlabel='Продукты', ylabel='Прибыль',
           title='График общей суммы продаж по каждому продукту')
    ax.bar_label(bar, fmt=lambda x: F"{x}₽")
    plt.show()


def draw_all_sum_date(sales_data: dict) -> None:
    '''Построить график общей суммы продаж по дням'''
    fig, ax = plt.subplots()
    data = zip(*sorted(sales_data.items(), key=lambda x: x[0]))
    bar = plt.bar(*data)
    ax.set(xlabel='Дата', ylabel='Прибыль',
           title='Общая сумма продаж по дням')
    ax.bar_label(bar, fmt=lambda x: F"{x}₽")
    fig.set_size_inches(w=1000, h=600)
    plt.show()


products = read_sales_data('data/data_10.csv')
# print(*products, sep='\n')
print('График общей суммы продаж по каждому продукту.')
draw_all_sum_products(total_sales_per_product(products))
# print(*total_sales_per_product(products).items(), sep='\n')
print('График общей суммы продаж по дням')
# print(*sales_over_time(products).items(), sep='\n')
draw_all_sum_date(sales_over_time(products))
print('ВСЁ')
