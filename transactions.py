import random
import hashlib
import string

from classes import Transaction, User

NUM_USERS = 1000
NUM_TRANSACTIONS = 10_000
RANDOM_SEED = 42
MIN_BALANCE = 100
MAX_BALANCE = 1_000_000
MIN_AMOUNT = 1
MAX_AMOUNT = 10_000

random.seed(RANDOM_SEED)


def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def random_name(length: int = 8) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def random_pubkey() -> str:
    raw = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
    return sha256_hex(raw)


def make_users(n: int):
    users = []
    for _ in range(n):
        name = random_name()
        pk = random_pubkey()
        balance = random.randint(MIN_BALANCE, MAX_BALANCE)
        users.append(User(name, pk, balance))
    return users


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
    print(f"Generating {NUM_USERS} users...")
    users = make_users(NUM_USERS)
    print(f"Generating {NUM_TRANSACTIONS} transactions...")
    txs = generate_transactions(users, NUM_TRANSACTIONS)
    print(f"Generated {len(txs)} transactions")
    print("Example 3 transactions:")
    for t in txs[:3]:
        print(f"{t.txid[:10]}... {t.amount} from {t.sender[:8]} -> {t.receiver[:8]}")


if __name__ == "__main__":
    main()
