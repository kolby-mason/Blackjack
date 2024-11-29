import csv

def load_money():
    try:
        with open("money.txt", mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
            return float(data[0][0]) if data else 100
    except FileNotFoundError:
        return 100

def save_money(money):
    with open("money.txt", mode='w') as file:
        writer = csv.writer(file)
        writer.writerow([money])
