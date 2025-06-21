"""Модуль для тестирования данных полученных из CSV файла.
"""

import psycopg2
import csv
import datetime
from DB_CONFIG import DB_CONFIG


conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

def get_50_records() -> list:
    """
    Получаем 50 случаный данных из базы данных

    Returns:
        list[tupple]: Список строк из базы данных в формате кортежа
    """
    cursor.execute("SELECT * FROM card_transactions ORDER BY RANDOM() LIMIT 50")
    return cursor.fetchall()

def database_record_to_str(record):
    """
    Приводим данные, полученные из базы данных в валидный строковый вид
    для корректного сравнения с CSV-строками 

    Args:
        record (tuple): Строка из базы данных
    
    Returns:
        list[str]: Список данных в строковом виде 
    """
    return [str(record[0]), str(float(record[1])), str(record[2])]

def test_of_quality_data() -> None:
    """
    Тест качества данных.
    Проверка валидности даты и отсутствие некорректных значений

    Returns:
        None 

    """
    data = get_50_records()
    errors = []

    for transaction_id, amount, transaction_date, _ in data:
        if amount <= 50:
            errors.append(f"Сумма {amount} <= 50 (ID: {transaction_id})")
        if transaction_date > datetime.datetime.now() + datetime.timedelta(days=1):
            errors.append(f"Дата {transaction_date} в будущем (ID: {transaction_id})")
    
    assert not errors, "\n".join(["Ошибки в данных:"] + errors)
    
    print("Тест качества данных пройден!")

def test_of_equality_to_source_date() -> None:
    """
    Тест на корректность загруженных данных
    
    Returns:
        None
    """
    csv_data = {}
    with open("card_transactions.csv", mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            csv_data[int(row[0])] = row

    cursor.execute("SELECT * FROM card_transactions LIMIT 50")
    db_data = cursor.fetchall()

    errors = []
    for db_record in db_data:
        transaction_id = db_record[0]
        if transaction_id not in csv_data:
            errors.append(f"ID {transaction_id} нет в CSV")
            continue

        csv_record = csv_data[transaction_id]
        db_record_str = database_record_to_str(db_record)
        if csv_record != db_record_str:
            errors.append(f"Несовпадение для ID {transaction_id}:\nCSV: {csv_record}\nБД: {db_record_str}")

    assert not errors, "\n".join(["Ошибки соответствия CSV:"] + errors)
    
    print("Тест на соответствие CSV пройден!")

if __name__ == '__main__':
    try:
        test_of_equality_to_source_date()
        test_of_quality_data()
    finally:
        cursor.close()
        conn.close()