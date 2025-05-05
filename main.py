from datetime import date, datetime

class Transaction:

    def __init__(self, type, amount, category, description=None, transaction_date=None):
        self.id = -1
        self.type = type
        self.amount = amount
        self.category = category
        self.description = description
        self.transaction_date = transaction_date if transaction_date else date.today()

    def __str__(self):
        return (f"[{self.id}] {self.type} - ${self.amount:,.2f} | {self.category} | "
                f"{self.description} | {self.transaction_date.strftime('%d/%m/%y')}")

class FinanceManager:
    def __init__(self):
        self.transactions = []
        self.next_id = 1
        self.balance = 0

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        transaction.id = self.next_id
        self.next_id += 1
        if transaction.type == "Gasto":
            self.balance -= transaction.amount
        elif transaction.type == "Ingreso":
            self.balance += transaction.amount
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
                        if transaction.type == "Gasto":
                            self.balance -= amount_difference
                        elif transaction.type == "Ingreso":
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
                if transaction.type == "Gasto":
                    self.balance += transaction.amount
                elif transaction.type == "Ingreso":
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
            filtered = [t for t in filtered if t.type.lower() == t_type.lower()]

        if date_from:
            filtered = [t for t in filtered if t.transaction_date >= date_from]

        if date_to:
            filtered = [t for t in filtered if t.transaction_date <= date_to]

        return filtered

    def display_transactions(self):
        if self.transactions:
            # Mostrar opciones disponibles al usuario
            categories = sorted(set(t.category.lower() for t in self.transactions))
            types = sorted(set(t.type for t in self.transactions))

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

def display_menu():
    print("")
    print("***** MENÚ *****")
    print("1. Agregar gasto")
    print("2. Agregar ingreso")
    print("3. Ver balance")
    print("4. Ver transacciones")
    print("5. Editar transacción")
    print("6. Eliminar transacción")
    print("7. Salir")
    print("")

def main():
    # Create FinanceManager instance
    manager = FinanceManager()

    while True:
        display_menu()

        try:
            choice = int(input("Seleccione una opción: "))
        except ValueError:
            print("Debe ingresar un número.")
            continue

        match choice:
            # Add income/expense
            case 1|2:
                type = "Gasto" if choice == 1 else "Ingreso"

                while True:
                    try:
                        amount = float(input(f"Ingrese el monto del {type.lower()}: $"))
                        if amount <= 0:
                            print("Debe ingresar un número positivo.")
                            continue
                        break
                    except ValueError:
                        print("Debe ingresar un número.")

                while True:
                    category = input("Ingrese la categoría: ")
                    if category:
                        break
                    print("Debe ingresar la categoría.")

                description = input("Ingrese la descripción (opcional): ")

                while True:
                    try:
                        transaction_date = input("Fecha (dd/mm/yy) o dejar en blanco para hoy: ")
                        if transaction_date:
                            transaction_date = datetime.strptime(transaction_date, "%d/%m/%y").date()
                        break
                    except ValueError:
                        print("Por favor ingrese el formato solicitado.")

                transaction = Transaction(type, amount, category, description, transaction_date)
                manager.add_transaction(transaction)

            case 3:
                manager.display_balance()

            case 4:
                manager.display_transactions()

            # Edit/delete transaction
            case 5|6:
                if not manager.transactions:
                    print("Actualmente no hay transacciones.")
                    continue

                action = manager.edit_transaction if choice == 5 else manager.delete_transaction
                while True:
                    try:
                        transaction_id = int(input("Ingrese el ID de la transacción: "))
                        transaction = action(transaction_id)
                        if transaction:
                            break
                    except ValueError:
                        print("Debe ingresar un número.")

            # Quit
            case 7:
                print("Hasta la próxima!")
                break

            # Anything else
            case _:
                print("Opción inválida")

if __name__ == "__main__":
    main()

