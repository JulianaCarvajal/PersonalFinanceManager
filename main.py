from collections.abc import Callable
from datetime import datetime

from manager import FinanceManager
from models import Transaction

def display_menu() -> None:
    print("")
    print(f"{' MENÚ ':*^30}")
    print("1. Agregar gasto")
    print("2. Agregar ingreso")
    print("3. Ver balance")
    print("4. Ver transacciones")
    print("5. Editar transacción")
    print("6. Eliminar transacción")
    print("7. Ver gastos mensuales por categoría ")
    print("8. Salir")
    print("")

def main() -> None:
    # Create FinanceManager instance
    filename = input("Nombre del archivo de transacciones (por defecto: transactions.json): ").strip()
    manager = FinanceManager(filename or "transactions.json")

    try:
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
                    t_type = "Gasto" if choice == 1 else "Ingreso"

                    while True:
                        try:
                            amount = float(input(f"Ingrese el monto del {t_type.lower()}: $"))
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
                            transaction_date_input = input("Fecha (dd/mm/yy) o dejar en blanco para hoy: ")
                            transaction_date = datetime.strptime(transaction_date_input,
                                                                 "%d/%m/%y").date() if transaction_date_input else None
                            break
                        except ValueError:
                            print("Por favor ingrese el formato solicitado.")

                    transaction = Transaction(t_type, amount, category, description, transaction_date)
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

                    action: Callable[[
                        int], Transaction | None] = manager.edit_transaction if choice == 5 else manager.delete_transaction
                    while True:
                        try:
                            transaction_id = int(input("Ingrese el ID de la transacción: "))
                            transaction = action(transaction_id)
                            if transaction:
                                break
                        except ValueError:
                            print("Debe ingresar un número.")

                case 7:
                    while True:
                        try:
                            month = int(input("Mes (1-12): "))
                            if month < 1 or month > 12:
                                print("El mes debe ser un número entre 1 y 12")
                                continue
                            year = int(input("Año: "))
                            if year <= 0:
                                print("El año debe ser un número positivo")
                                continue
                            break
                        except ValueError:
                            print("Por favor ingrese solo números enteros")
                    manager.print_monthly_summary(month, year)

                # Quit
                case 8:
                    manager.save_to_file()
                    print("Hasta la próxima!")
                    break

                # Anything else
                case _:
                    print("Opción inválida")
    finally:
        manager.save_to_file()

if __name__ == "__main__":
    main()

