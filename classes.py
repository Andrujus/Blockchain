class User:
    def __init__(self, name: str, public_key: str, balance: int):
        self.name = name
        self.public_key = public_key
        self.balance = balance

class Transaction:
    def __init__(self, sender: User, receiver: User, amount: int, txid: str):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.txid = txid


class block:
    def __init__(self, transactions: list):
        self.transactions = transactions