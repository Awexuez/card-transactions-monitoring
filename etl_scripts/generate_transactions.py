from datetime import datetime
import random
from faker import Faker


fake = Faker('ru_RU')


def generate_transactions():
    """Генерация транзакций"""
    roll = random.randint(1, 6)

    if roll == 1:
        amount = round(random.uniform(3500.00, 100000.00), 2)
    elif roll in (3, 4):
         amount = round(random.uniform(10.21, 3500.00), 2)
    else:
        amount = round(random.uniform(10.21, 5000.00 ), 2)
    operation_date = fake.date_time_between(start_date=datetime(2025, 1, 1), end_date=datetime(2025, 6, 1))
    return amount, operation_date


if __name__ == '__main__':

    print(generate_transactions())