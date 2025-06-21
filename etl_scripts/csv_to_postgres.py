"""Модуль для загрузки данных из CSV-файлов в базу данных PostgreSQL.
"""

import csv
import psycopg2

from DB_CONFIG import DB_CONFIG
from psycopg2 import sql


conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

def write_csv_to_postgres(file_path: str, query: sql.SQL) -> None:
    """
    Записывает данные из CSV-файла в таблицу базы данных PostgreSQL.
    
    Функция читает CSV-файл, извлекает данные и выполняет SQL-запрос
    для вставки данных в соответствующую таблицу.

    Args:
        file_path (str): Путь к CSV-файлу c данными для загрузки
        query (sql.SQL): SQL-запрос для вставки данных, должен быть
                         подготовлен c использованием psycopg2.sql.SQL

    Returns:
        None
    """
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)                  # Пропускаем заголовок

        for card_transaction_data in reader:
            _, amount, _ = card_transaction_data
            
            if float(amount) > 50:
                cursor.execute(query, card_transaction_data[1:])

    conn.commit()

if __name__ == '__main__':
    try:
        query = sql.SQL(
            """
                INSERT INTO card_transactions (amount, transaction_date) 
                VALUES (%s, %s)
            """)
        write_csv_to_postgres("card_transactions.csv", query)
        
    except Exception as e:
        print(f"Программа завершена c ошибкой: {e}")
    finally:    
        if conn:
            conn.close()

