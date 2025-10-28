import random
import time
import hashlib
import json
from pathlib import Path

from classes import Transaction, User

USERS_FILE = "users.json"
NUM_TRANSACTIONS = 10_000
RANDOM_SEED = 42
MIN_AMOUNT = 1
MAX_AMOUNT = 10_000

random.seed(RANDOM_SEED)


def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def load_users(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [User(u["name"], u["public_key"], u["balance"]) for u in data]


def generate_transactions(users, count: int):
    txs = []
    user_keys = [u.public_key for u in users]
    for _ in range(count):
        sender = random.choice(user_keys)
        receiver = random.choice(user_keys)
        while receiver == sender:
            receiver = random.choice(user_keys)
        amount = random.randint(MIN_AMOUNT, MAX_AMOUNT)
        raw = f"{sender}|{receiver}|{amount}"
        txid = sha256_hex(raw)
        tx = Transaction(sender, receiver, amount, txid)
        txs.append(tx)
    return txs


def main():
    print(f"Loading users from {USERS_FILE}...")
    users = load_users(USERS_FILE)
    print(f"Generating {NUM_TRANSACTIONS} transactions...")
    txs = generate_transactions(users, NUM_TRANSACTIONS)
    print(f"Generated {len(txs)} transactions")
    print("Example 3 transactions:")
    for t in txs[:3]:
        print(f"{t.txid[:10]}... {t.amount} from {t.sender} -> {t.receiver}")


if __name__ == "__main__":
    main()
