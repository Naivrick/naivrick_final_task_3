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
    plt.bar(*zip(*sorted(sales_data.items(), key=lambda x: x[1])))
    plt.xlabel('Продукты')
    plt.ylabel('Прибыль')
    plt.title('Общая сумма продаж по каждому продукту')
    # plt.figure(figsize=(20,5))
    plt.show()


def draw_all_sum_date(sales_data: dict) -> None:
    '''Построить график общей суммы продаж по дням'''
    fig, ax = plt.subplots()
    plt.bar(*zip(*sorted(sales_data.items(), key=lambda x: x[0])))
    fig.set_size_inches(15, 5)

    plt.xlabel('Дата')
    plt.ylabel('Прибыль')
    plt.title('Общая сумма продаж по дням')

    plt.show()


products = read_sales_data('input_data.csv')
# print(*products, sep='\n')
draw_all_sum_products(total_sales_per_product(products))
# print(*total_sales_per_product(products).items(), sep='\n')

# print(*sales_over_time(products).items(), sep='\n')
draw_all_sum_date(sales_over_time(products))
