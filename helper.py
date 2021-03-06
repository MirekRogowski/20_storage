import sys
import pathlib
import datetime


class Manager:
    def __init__(self):
        self.balance = 0
        self.warehouse = {}
        self.logs = []
        self.data = []
        self.error = []
        self.actions = {}
        self.action_param = {}
        self.read_data_from_file(sys.argv[1])

    def assign(self, action, action_qty=0):
        def decorate(callback):
            self.actions[action] = callback
            self.action_param[action] = action_qty
        return decorate

    def execute(self, action, *args):
        if action in self.actions:
            self.actions[action](*args)
        else:
            return "Akcja niedostpena"

    def read_data_from_file(self, filepath):
        with open(filepath) as f:
            for line in f:
                self.data.append(line.strip())

    def write_data_to_file(self, filename):
        with open(filename, "w") as f:
            for line in self.logs:
                f.write(f"{line[0]}\n")
                for item in line[1]:
                    f.write(f"{item}\n")

    def check_warehouse(self, product, quantity):
        if product in self.warehouse:
            self.warehouse[product] += quantity  # add quantity to warehouse
        else:
            self.warehouse[product] = quantity  # add item and quantity to warehouse

    def transform_data(self):
        index = 0
        while index < len(self.data):
            if self.data[index] in self.action_param:
                qty_param = self.action_param[self.data[index]]
                action = self.data[index]
                if action == "saldo":
                    self.execute(action, int(self.data[index + 1]), self.data[index + qty_param])
                elif action == "zakup":
                    self.execute(action, self.data[index + 1], int(self.data[index + 2]), int(self.data[index + qty_param]))
                elif action == "sprzedaz":
                    self.execute(action, self.data[index + 1], int(self.data[index + 2]), int(self.data[index + qty_param]))
                else:
                    print(f"Nie jest obslugiwana akcja {action}")    
                index += qty_param + 1
            else:
                break
        return


manager = Manager()

@manager.assign("saldo", 2)
def balance_update_data(balance, comment):
    if manager.balance + int(balance) >= 0:
        manager.balance += int(balance)
        manager.logs.append(["saldo", [balance, comment]])
    else:
        manager.error.append(["saldo", [balance, comment]])
        print(f"\nZa ma??e saldo du wykonania operacji:"
              f"\nbrakuje {int(balance) + manager.balance}, dostepne saldo: {manager.balance}")

@manager.assign("zakup", 3)
def buy_update_data(product, price, quantity):
    if manager.balance <= 0:
        print(f"Saldo wynosi: {manager.balance}. Nie mo??na kupi?? towaru")
    if price * quantity > manager.balance:
        print(f"Nie mozna zakupi?? {product}: {quantity} sztuk. Za ma??e saldo: {manager.balance}")
    if price * quantity <= manager.balance:
        manager.balance -= price * quantity
        manager.check_warehouse(product, quantity)
        return manager.logs.append(["zakup", [product, price, quantity]])

@manager.assign("sprzedaz", 3)
def sale_update_data(product, price, quantity):
    if not manager.warehouse:
        print(f"Magazyn jest pusty prosz?? zakupic towar.")
    if product in manager.warehouse:
        if manager.warehouse[product] - quantity < 0:
            print(f"Chcesz sprzedac {product}: {quantity} sztuk. "
                  f"W magazynie jest: {manager.warehouse[product]} ")
        else:
            manager.balance += price * quantity
            manager.warehouse[product] -= quantity
            return manager.logs.append(["sprzedaz", [product, price, quantity]])
    else:
        print(f"Nie ma w magazynie: {product} ")

@manager.assign("magazyn")
def status_warehouse(item_store):
    print("Stan magazynu:")
    for item in item_store:
        if item in manager.warehouse:
            print(f"  - {item} : {manager.warehouse[item]} sztuk")
        else:
            print(f"  - {item} : brak poyzcji w magazynie")
    return

@manager.assign("konto")
def check_balance():
    print(f"\nStan konta wynosi: {manager.balance} ")
    return

@manager.assign("przeglad")
def display_log(log_first, log_last):
    first, last = log_first, log_last
    try:
        while first <= last:
            print(f"Akcja nr {first} - {manager.logs[first - 1]}")
            first += 1
    except IndexError:
        print("Koniec")
    return
