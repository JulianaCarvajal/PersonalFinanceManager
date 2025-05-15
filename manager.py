import json

from datetime import datetime
from os.path import exists

from models import Transaction

class FinanceManager:
    def __init__(self, filename="transactions.json"):
        self.filename = filename
        self.transactions = []
        self.next_id = 1
        self.balance = 0
        self.load_from_file()

    def load_from_file(self):
        if not exists(self.filename):
            return

        with open(self.filename, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        for transaction_data in data:
            transaction = Transaction(
                transaction_data["t_type"],
                transaction_data["amount"],
                transaction_data["category"],
                transaction_data.get("description"),
                datetime.strptime(transaction_data["transaction_date"], "%d/%m/%y").date()
            )
            self.add_transaction(transaction, show_message=False)

        # Ensure next ID is not repeated
        if self.transactions:
            self.next_id = max(t.id for t in self.transactions) + 1

    def save_to_file(self):
        transaction_data = [t.to_dict() for t in self.transactions]
        with open(self.filename, 'w', encoding="utf-8") as json_file:
            json.dump(transaction_data, json_file, ensure_ascii=False, indent=4)

    def add_transaction(self, transaction, show_message=True):
        self.transactions.append(transaction)
        transaction.id = self.next_id
        self.next_id += 1
        if transaction.t_type == "Gasto":
            self.balance -= transaction.amount
        elif transaction.t_type == "Ingreso":
            self.balance += transaction.amount
        if show_message:
            print(f"Transacción agregada exitosamente.")

    def find_transaction_by_id(self, transaction_id):
        for transaction in self.transactions:
            if transaction_id == transaction.id:
                return transaction
        return None

    def edit_transaction(self, transaction_id):
        transaction = self.find_transaction_by_id(transaction_id)
        if transaction:
            print(f"Editando transacción: {transaction}")

            print(f"El monto actual es ${transaction.amount:,.2f}")
            while True:
                try:
                    new_amount = input(f"Ingrese el nuevo monto (dejar vacío para no cambiar): $")
                    if new_amount != "":
                        new_amount = float(new_amount)
                        amount_difference = new_amount - transaction.amount
                        if transaction.t_type == "Gasto":
                            self.balance -= amount_difference
                        elif transaction.t_type == "Ingreso":
                            self.balance += amount_difference

                        transaction.amount = new_amount
                    break
                except ValueError:
                    print("Debe ingresar un número.")

            print(f"La categoría actual es '{transaction.category}'")
            new_category = input("Ingrese la nueva categoría (dejar vacío para no cambiar): ")
            if new_category != "":
                transaction.category = new_category

            if transaction.description:
                print(f"La descripción actual es {transaction.description}")
            else:
                print("Actualmente la transacción no tiene descripción")
            new_description = input("Ingrese la nueva descripción (dejar vacío para no cambiar): ")
            if new_description != "":
                transaction.description = new_description

            print(f"La fecha actual es {transaction.transaction_date.strftime('%d/%m/%y')}")
            while True:
                try:
                    new_date = input("Ingrese la nueva fecha (dd/mm/yy) (dejar vacío para no cambiar): ")
                    if new_date:
                        new_date = datetime.strptime(new_date, "%d/%m/%y").date()
                        transaction.transaction_date = new_date
                    break
                except ValueError:
                    print("Por favor ingrese el formato solicitado.")

            print(f"Transacción editada exitosamente.")
            return transaction

        else:
            print("Esta transacción no existe. Ingrese un ID válido.")
            return None

    def delete_transaction(self, transaction_id):
        transaction = self.find_transaction_by_id(transaction_id)

        if transaction:
            confirm = input(f"¿Seguro que desea eliminar la transacción {transaction.id}? (s/n): ").lower()
            if confirm in ("s", "sí", "si"):
                if transaction.t_type == "Gasto":
                    self.balance += transaction.amount
                elif transaction.t_type == "Ingreso":
                    self.balance -= transaction.amount
                print(f"Transacción eliminada exitosamente.")
                self.transactions.remove(transaction)
                return transaction

            print("Operación cancelada")
            return None

        print("Esta transacción no existe. Ingrese un ID válido.")
        return None

    def display_balance(self):
        print(f"Actualmente tiene ${self.balance:.2f}")

    def filter_transactions(self, category=None, t_type=None, date_from=None, date_to=None):
        filtered = self.transactions

        if category:
            filtered = [t for t in filtered if t.category.lower() == category.lower()]

        if t_type:
            filtered = [t for t in filtered if t.t_type.lower() == t_type.lower()]

        if date_from:
            filtered = [t for t in filtered if t.transaction_date >= date_from]

        if date_to:
            filtered = [t for t in filtered if t.transaction_date <= date_to]

        return filtered

    def display_transactions(self):
        if self.transactions:
            # Mostrar opciones disponibles al usuario
            categories = sorted(set(t.category.lower() for t in self.transactions))
            types = sorted(set(t.t_type for t in self.transactions))

            print("\nCategorías disponibles:", ", ".join(categories))
            category = input("Filtrar por categoría (dejar vacío para ignorar): ").strip()

            print("Tipos disponibles:", ", ".join(types))
            t_type = input("Filtrar por tipo (Gasto / Ingreso, dejar vacío para ignorar): ").strip()

            try:
                date_from = input("Filtrar desde (dd/mm/yy, dejar vacío para ignorar): ").strip()
                date_from = datetime.strptime(date_from, "%d/%m/%y").date() if date_from else None

                date_to = input("Filtrar hasta (dd/mm/yy, dejar vacío para ignorar): ").strip()
                date_to = datetime.strptime(date_to, "%d/%m/%y").date() if date_to else None
            except ValueError:
                print("Formato de fecha inválido. Se ignorarán los filtros por fecha.")
                date_from, date_to = None, None

            results = self.filter_transactions(
                category=category if category else None,
                t_type=t_type if t_type else None,
                date_from=date_from,
                date_to=date_to
            )

            print("***** TRANSACCIONES *****")
            if results:
                print(*results, sep="\n")
            else:
                print("No se encontraron transacciones con esos criterios.")
        else:
            print("Actualmente no hay transacciones.")