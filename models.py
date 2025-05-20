from datetime import date
from typing import Any


class Transaction:

    def __init__(self, t_type: str, amount: float, category: str, description: str | None = None, transaction_date: date | None = None) -> None:
        self.id: int = -1
        self.t_type: str = t_type
        self.amount: float = amount
        self.category: str = category.lower()
        self.description: str | None = description.lower() if description else None
        self.transaction_date = transaction_date or date.today()

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "t_type": self.t_type,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "transaction_date": self.transaction_date.strftime("%d/%m/%y")
        }

    def __str__(self) -> str:
        return (f"[{self.id}] {self.t_type:<8} | ${self.amount:<14,.2f} | {self.category.capitalize():<13} | "
                f"{self.description.capitalize():<10} | {self.transaction_date.strftime('%d/%m/%y')}")