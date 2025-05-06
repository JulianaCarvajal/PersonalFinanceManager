import pytest

from datetime import date
from main import Transaction, FinanceManager

class TestFinanceManager:
    def test_add_transaction(self):
        manager = FinanceManager()
        t1 = Transaction("Gasto", 5000, "Comida")
        manager.add_transaction(t1)

        assert len(manager.transactions) == 1
        assert t1.id == 1
        assert manager.next_id == 2
        assert manager.balance == -5000

        t2 = Transaction("Ingreso", 10000, "Salario")
        manager.add_transaction(t2)

        assert len(manager.transactions) == 2
        assert t2.id == 2
        assert manager.next_id == 3
        assert manager.balance == 5000

    def test_find_transaction_by_id(self):
        manager = FinanceManager()
        t = Transaction("Gasto", 5000, "Comida")
        manager.add_transaction(t)
        t_found = manager.find_transaction_by_id(1)

        assert t_found == t
        assert t_found.amount == 5000
        assert manager.find_transaction_by_id(999) is None

    def test_filter_by_category(self):
        manager = FinanceManager()
        t1 = Transaction("Gasto", 5000, "Comida")
        t2 = Transaction("Ingreso", 10000, "Salario")
        t3 = Transaction("Gasto", 1000, "comida")
        manager.add_transaction(t1)
        manager.add_transaction(t2)
        manager.add_transaction(t3)

        result = manager.filter_transactions(category="comida")
        assert result == [t1, t3]

    def test_filter_by_type(self):
        manager = FinanceManager()
        t1 = Transaction("Gasto", 5000, "Comida")
        t2 = Transaction("Ingreso", 10000, "Salario")
        t3 = Transaction("Gasto", 1000, "comida")
        manager.add_transaction(t1)
        manager.add_transaction(t2)
        manager.add_transaction(t3)

        result = manager.filter_transactions(t_type="Ingreso")
        assert result == [t2]

    def test_filter_by_date(self):
        manager = FinanceManager()
        t1 = Transaction("Gasto", 5000, "Comida", transaction_date=date(2001, 1, 1))
        t2 = Transaction("Ingreso", 10000, "Salario", transaction_date=date(2001, 6, 15))
        t3 = Transaction("Gasto", 1000, "comida", transaction_date=date(2001, 12, 30))
        manager.add_transaction(t1)
        manager.add_transaction(t2)
        manager.add_transaction(t3)

        result1 = manager.filter_transactions(date_from=date(2001, 6, 16))
        result2 = manager.filter_transactions(date_from=date(2001, 1, 1), date_to=date(2001, 6, 15))
        assert result1 == [t3]
        assert result2 == [t1, t2]

    def test_filter_by_category_and_type(self):
        manager = FinanceManager()
        t1 = Transaction("Gasto", 5000, "Comida")
        t2 = Transaction("Ingreso", 10000, "Salario")
        t3 = Transaction("Ingreso", 1000, "comida")
        manager.add_transaction(t1)
        manager.add_transaction(t2)
        manager.add_transaction(t3)

        result = manager.filter_transactions(category="Comida", t_type="Gasto")
        assert result == [t1]

    def test_save_and_load_file(self, tmp_path):
        # Temporary file
        test_file = tmp_path / "test_transactions.json"

        manager = FinanceManager()
        manager.filename = str(test_file)
        t1 = Transaction("Gasto", 5000, "Comida", transaction_date=date(2001, 1, 1))
        t2 = Transaction("Ingreso", 10000, "Salario", transaction_date=date(2001, 6, 15))
        t3 = Transaction("Gasto", 1000, "comida", transaction_date=date(2001, 12, 30))
        manager.add_transaction(t1)
        manager.add_transaction(t2)
        manager.add_transaction(t3)

        # Save to JSON file
        manager.save_to_file()

        # Create new manager
        new_manager = FinanceManager()
        new_manager.filename = str(test_file)
        new_manager.load_from_file()

        assert len(new_manager.transactions) == 3
        assert new_manager.transactions[0].category == "Comida"
        assert new_manager.transactions[1].amount == 10000
        assert new_manager.balance == 4000
