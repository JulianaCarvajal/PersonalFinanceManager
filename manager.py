import json

from datetime import date, datetime
from os.path import exists
from typing import Any

from models import Transaction

class FinanceManager:
    def __init__(self, filename: str = "transactions.json") -> None:
        self.filename: str = filename
        self.transactions: list[Transaction] = []
        self.next_id: int = 1
        self.balance: float = 0.0
        self.load_from_file()

    def load_from_file(self) -> None:
        if not exists(self.filename):
            return

        with open(self.filename, "r", encoding="utf-8") as json_file:
            data: list[dict[str, Any]] = json.load(json_file)

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

    def save_to_file(self) -> None:
        transaction_data = [t.to_dict() for t in self.transactions]
        with open(self.filename, 'w', encoding="utf-8") as json_file:
            json.dump(transaction_data, json_file, ensure_ascii=False, indent=4)

    def add_transaction(self, transaction: Transaction, show_message: bool = True) -> None:
        self.transactions.append(transaction)
        transaction.id = self.next_id
        self.next_id += 1

        if transaction.t_type == "Gasto":
            self.balance -= transaction.amount
        elif transaction.t_type == "Ingreso":
            self.balance += transaction.amount

        if show_message:
            print(f"Transacción agregada exitosamente.")

    def find_transaction_by_id(self, transaction_id: int) -> Transaction | None:
        for transaction in self.transactions:
            if transaction_id == transaction.id:
                return transaction
        return None

    def edit_transaction(self, transaction_id: int) -> Transaction | None:
        transaction = self.find_transaction_by_id(transaction_id)
        if transaction:
            print(f"Editando transacción: {transaction}")

            print(f"El monto actual es ${transaction.amount:,.2f}")
            while True:
                try:
                    new_amount_input = input(f"Ingrese el nuevo monto (dejar vacío para no cambiar): $")
                    if new_amount_input != "":
                        new_amount = float(new_amount_input)
                        amount_difference = new_amount - transaction.amount
                        if transaction.t_type == "Gasto":
                            self.balance -= amount_difference
                        elif transaction.t_type == "Ingreso":
                            self.balance += amount_difference

                        transaction.amount = new_amount
                    break
                except ValueError:
                    print("Debe ingresar un número.")

            print(f"La categoría actual es '{transaction.category.capitalize()}'")
            new_category = input("Ingrese la nueva categoría (dejar vacío para no cambiar): ")
            if new_category != "":
                transaction.category = new_category

            if transaction.description:
                print(f"La descripción actual es {transaction.description.capitalize()}")
            else:
                print("Actualmente la transacción no tiene descripción")
            new_description = input("Ingrese la nueva descripción (dejar vacío para no cambiar): ")
            if new_description != "":
                transaction.description = new_description

            print(f"La fecha actual es {transaction.transaction_date.strftime('%d/%m/%y')}")
            while True:
                try:
                    new_date_input = input("Ingrese la nueva fecha (dd/mm/yy) (dejar vacío para no cambiar): ")
                    if new_date_input:
                        new_date = datetime.strptime(new_date_input, "%d/%m/%y").date()
                        transaction.transaction_date = new_date
                    break
                except ValueError:
                    print("Por favor ingrese el formato solicitado.")

            print(f"Transacción editada exitosamente.")
            return transaction

        else:
            print("Esta transacción no existe. Ingrese un ID válido.")
            return None

    def delete_transaction(self, transaction_id: int) -> Transaction | None:
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

    def display_balance(self) -> None:
        print(f"Actualmente tiene ${self.balance:.2f}")

    def filter_transactions(self, category: str | None = None, t_type: str | None = None, date_from: date | None = None,
                            date_to: date | None = None) -> list[Transaction]:
        filtered = self.transactions

        if category:
            filtered = [t for t in filtered if t.category == category.lower()]

        if t_type:
            filtered = [t for t in filtered if t.t_type.lower() == t_type.lower()]

        if date_from:
            filtered = [t for t in filtered if t.transaction_date >= date_from]

        if date_to:
            filtered = [t for t in filtered if t.transaction_date <= date_to]

        return filtered

    def display_transactions(self) -> None:
        if self.transactions:
            # Show available options to the user
            categories = sorted(set(t.category.capitalize() for t in self.transactions))
            types = sorted(set(t.t_type for t in self.transactions))

            print("\nCategorías disponibles:", ", ".join(categories))
            category = input("Filtrar por categoría (dejar vacío para ignorar): ").strip()

            print("Tipos disponibles:", ", ".join(types))
            t_type = input("Filtrar por tipo (Gasto / Ingreso, dejar vacío para ignorar): ").strip()

            try:
                date_from_input = input("Filtrar desde (dd/mm/yy, dejar vacío para ignorar): ").strip()
                date_from = datetime.strptime(date_from_input, "%d/%m/%y").date() if date_from_input else None

                date_to_input = input("Filtrar hasta (dd/mm/yy, dejar vacío para ignorar): ").strip()
                date_to = datetime.strptime(date_to_input, "%d/%m/%y").date() if date_to_input else None
            except ValueError:
                print("Formato de fecha inválido. Se ignorarán los filtros por fecha.")
                date_from, date_to = None, None

            results = self.filter_transactions(
                category=category or None,
                t_type=t_type or None,
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

