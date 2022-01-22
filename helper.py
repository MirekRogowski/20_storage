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
        self.write_error_to_file()

    def write_error_to_file(self):
        with open("error.txt", "a") as e:
            for line in self.error:
                e.write(f"\n{datetime.datetime.now().strftime('%Y-%m-%d - %H:%M:%S')} - {line}")

    def check_warehouse(self, product, quantity):
        if product in self.warehouse:
            self.warehouse[product] += quantity  # add quantity to warehouse
        else:
            self.warehouse[product] = quantity  # add item and quantity to warehouse

    # def status_warehouse(self, item_store):
    #     if item_store in self.warehouse:
    #         return f"{item_store} : {self.warehouse[item_store]} sztuk"
    #     else:
    #         return f"{item_store} : brak poyzcji w magazynie"

    def transform_data(self):
        index = 0
        while index < len(self.data):
            if self.data[index] in self.action_param:
                qty_param = self.action_param[self.data[index]]
                action = self.data[index]
                # print(index, action, self.data[index], self.data[index + 1], self.data[index + 2], self.data[index + qty_param])
                if action == "saldo":
                    # self.balance += int(self.data[index + 1])
                    # self.logs.append([action, [int(self.data[index + 1]), self.data[index + qty_param]]])
                    self.execute(action, int(self.data[index + 1]), self.data[index + qty_param])
                elif action == "zakup":
                    # self.balance -= int(self.data[index + 2]) + int(self.data[index + qty_param])
                    # self.logs.append([action, [self.data[index + 1], int(self.data[index + 2]), int(self.data[index + qty_param])]])
                    self.execute(action, self.data[index + 1], int(self.data[index + 2]), int(self.data[index + qty_param]))
                elif action == "sprzedaz":
                    # self.balance += int(self.data[index + 2]) + int(self.data[index + qty_param])
                    # self.logs.append([action, [self.data[index + 1], int(self.data[index + 2]), int(self.data[index + qty_param])]])
                    self.execute(action, self.data[index + 1], int(self.data[index + 2]), int(self.data[index + qty_param]))
                index += qty_param + 1
                # print(index, action, self.data[index], self.data[index + 1], self.data[index + 2], self.data[index + qty_param])
            else:
                return f"Nie jest obslugiwana akcja {action}"
        return

    def print_info(self, action):
        print(f"{action} - balance: ", self.balance)
        print(f"{action} - warehouse: ", self.warehouse)
        print(f"{action} - logs: ", self.logs)
        print(f"{action} - data: ", self.data , type(self.data))
        print(f"{action} - error: ", self.error)
        print(f"{action} - actions: ", self.actions)
        print(f"{action} - action_param: ", self.action_param )


manager = Manager()


@manager.assign("saldo", 2)
def balance_update_data(balance, comment):
    if manager.balance + int(balance) >= 0:
        manager.balance += int(balance)
        manager.logs.append(["saldo", [balance, comment]])
    else:
        manager.error.append(["saldo", [balance, comment]])
        print(f"Za małe saldo du wykonania operacji:"
              f"\npotrzebujesz {int(balance) + manager.balance} jest {manager.balance}")


manager.execute("saldo", -1000, "zus")