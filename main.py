import csv
import logging
from sys import getsizeof
from decimal import Decimal
from datetime import datetime as dt

import matplotlib.pyplot as plt

logging.basicConfig(
    format='%(levelname)s: %(message)s',
    level=logging.INFO)


def read_sales_data(file_path: str) -> list[dict]:
    '''Функция принимает путь к CSV файлу и возвращает список словарей
    со следующими ключами (название, количество, цена, дата)'''
    # --- Открытие CSV с дальнешим считыванием ---
    with open(file_path, mode='r', encoding='UTF-8') as file_data:
        logging.info(F"Открыт файл: {file_path.split('/')[1]}")
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

        logging.debug(F"Вес объекта: {getsizeof(products)} байт")

        # --- Возврат обработанных данных ---
        return products


def total_sales_per_product(sales_data: list[dict]) -> dict:
    '''Функция принимает список продаж и возвращает словарь,
    где ключ - название продукта, а значение -
      общая сумма продаж этого продукта.'''
    logging.debug(F"Запуск функции total_sales_per_product")
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
    logging.debug(F"Запуск функции sales_over_time")
    result = dict()
    for product in sales_data:
        date = product['date']
        price_product = product['price']
        result.setdefault(date, 0)
        result[date] += price_product
    return result


def draw_result(max_price_product, max_price_day):
    fig = plt.figure()

    fig.text(0.5, 0.6,
             f"Наибольшую выручка: {max_price_product[0]} {
                 max_price_product[1]}₽",
             horizontalalignment='center',
             verticalalignment='center')

    date_sale = f"{max_price_day[0].day}.{
        max_price_day[0].month}.{max_price_day[0].year}"
    fig.text(0.5, 0.4,
             f"""Наибольшая сумма продаж была: {date_sale}
Сумма: {max_price_day[1]}₽""",
        horizontalalignment='center',
        verticalalignment='center')

    # fig.text(10, 10, 'продукт принес наибольшую выручку. ')
    # день когда была наибольшая сумма продаж

    plt.show()


def draw_all_sum_products(sales_data: dict) -> None:
    '''График общей суммы продаж по каждому продукту.'''
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    plt.style.use('seaborn-v0_8-white')
    data = zip(*sorted(sales_data.items(), key=lambda x: x[1]))
    bar = ax.bar(*data, width=0.8, edgecolor="white")

    ax.set(xlabel='Продукты', ylabel='Прибыль',
           title='График общей суммы продаж по каждому продукту')
    ax.bar_label(bar, fmt=lambda x: F"{x}₽")
    plt.show()


def draw_all_sum_date(sales_data: dict) -> None:
    '''Построить график общей суммы продаж по дням'''
    fig, ax = plt.subplots(layout="constrained")
    data = zip(*sorted(sales_data.items(), key=lambda x: x[0]))
    bar = plt.bar(*data)
    ax.set(xlabel='Дата', ylabel='Прибыль',
           title='Общая сумма продаж по дням')

    ax.bar_label(bar, fmt=lambda x: F"{x}₽")
    ax.tick_params(labelrotation=90)
    fig.set_figwidth(10)
    plt.show()


def main() -> None:
    '''Точка входа'''
    products = read_sales_data('data/data_10.csv')
    logging.info('Получили список покупок')
    total_sales_products = total_sales_per_product(products)
    logging.info('Получили общую сумму продаж этого продукта')

    sales_all_time = sales_over_time(products)
    logging.info('Получили общую сумму продаж по датам')

    # Определить, какой продукт принес наибольшую выручку.
    max_price_product = max(total_sales_products.items(), key=lambda x: x[1])

    # Определить, в какой день была наибольшая сумма продаж.
    max_price_day = max(sales_all_time.items(), key=lambda x: x[1])

    draw_result(max_price_product, max_price_day)

    logging.info('Отрисовка графиков:')
    draw_all_sum_products(total_sales_products)  # Отрисовка графиков
    draw_all_sum_date(sales_all_time)


if __name__ == '__main__':
    main()
    logging.info('The End')
