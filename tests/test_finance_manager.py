import pytest

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
