import csv
from generate_transactions import generate_transactions


def csv_card_transactions(num_actions):

    with open("card_transactions.csv", mode="w", encoding="utf-8-sig", newline="") as file:
        
        header = ['transaction_id', 'amount',  'date']
        writer = csv.writer(file)
        writer.writerow(header) 
        
        for i in range(1, num_actions + 1):
            action_data = generate_transactions()
            writer.writerow((i,) + action_data)
    
    print("Файл card_transactons.csv успешно создан!")

if __name__ == '__main__':
    
    csv_card_transactions(2000)
