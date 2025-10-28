import random
import time
import hashlib
import json
from pathlib import Path

USERS_FILE = "users.json"
OUTPUT_FILE = "transactions.json"
NUM_TRANSACTIONS = 10_000
RANDOM_SEED = 42
MIN_AMOUNT = 1
MAX_AMOUNT = 10_000

random.seed(RANDOM_SEED)

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def load_users(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_transactions(users, count: int):
    txs = []
    user_keys = [u["public_key"] for u in users]
    for _ in range(count):
        sender = random.choice(user_keys)
        receiver = random.choice(user_keys)
        # vengiam, kad siųstų pats sau
        while receiver == sender:
            receiver = random.choice(user_keys)
        amount = random.randint(MIN_AMOUNT, MAX_AMOUNT)
        timestamp = time.time()
        raw = f"{sender}|{receiver}|{amount}|{timestamp}"
        txid = sha256_hex(raw)
        txs.append({
            "txid": txid,
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "timestamp": timestamp
        })
    return txs

def save_transactions(txs, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(txs, f, indent=2, ensure_ascii=False)

def main():
    print(f"Loading users from {USERS_FILE}...")
    users = load_users(USERS_FILE)
    print(f"Generating {NUM_TRANSACTIONS} transactions...")
    txs = generate_transactions(users, NUM_TRANSACTIONS)
    save_transactions(txs, OUTPUT_FILE)
    print(f"Saved {len(txs)} transactions to {OUTPUT_FILE}")
    print("Example 3 transactions:")
    for t in txs[:3]:
        print(f"  {t['txid'][:10]}... {t['amount']} from {t['sender'][:8]} -> {t['receiver'][:8]}")

if __name__ == "__main__":
    main()
