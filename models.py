from datetime import date

class Transaction:

    def __init__(self, t_type, amount, category, description=None, transaction_date=None):
        self.id = -1
        self.t_type = t_type
        self.amount = amount
        self.category = category
        self.description = description
        self.transaction_date = transaction_date if transaction_date else date.today()

    def to_dict(self):
        return {
            "id": self.id,
            "t_type": self.t_type,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "transaction_date": self.transaction_date.strftime("%d/%m/%y")
        }

    def __str__(self):
        return (f"[{self.id}] {self.t_type} - ${self.amount:,.2f} | {self.category} | "
                f"{self.description} | {self.transaction_date.strftime('%d/%m/%y')}")