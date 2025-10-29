import random
import json
from pathlib import Path

from classes import Transaction
from users import make_users, save_users

NUM_USERS = 1000
NUM_TRANSACTIONS = 10_000
RANDOM_SEED = 42
MIN_AMOUNT = 1
MAX_AMOUNT = 10_000
USERS_FILE = "users.json"
TX_FILE = "transactions.json"

random.seed(RANDOM_SEED)


def generate_transactions(users, count: int):
    txs = []
    user_keys = [u.public_key for u in users]
    for _ in range(count):
        sender = random.choice(user_keys)
        receiver = random.choice(user_keys)
        while receiver == sender:  # vengiam siųsti pats sau
            receiver = random.choice(user_keys)
        amount = random.randint(MIN_AMOUNT, MAX_AMOUNT)
        tx = Transaction(sender, receiver, amount)  # txid sugeneruoja klasė
        txs.append(tx)
    return txs


def save_transactions(txs, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    def tx_to_dict(t: Transaction):
        return {
            "sender": t.sender,
            "receiver": t.receiver,
            "amount": t.amount,
            "txid": t.txid,
        }

    with open(path, "w", encoding="utf-8") as f:
        json.dump([tx_to_dict(t) for t in txs], f, indent=2, ensure_ascii=False)


def main():
    print(f"Generating {NUM_USERS} users...")
    users = make_users(NUM_USERS)
    save_users(users, USERS_FILE)

    print(f"Generating {NUM_TRANSACTIONS} transactions...")
    txs = generate_transactions(users, NUM_TRANSACTIONS)
    save_transactions(txs, TX_FILE)
    print(f"Saved {len(txs)} transactions -> {TX_FILE}")

    print("Example 3 transactions:")
    for t in txs[:3]:
        print(f"{t.txid[:10]}... {t.amount} from {t.sender[:8]} -> {t.receiver[:8]}")


if __name__ == "__main__":
    main()
