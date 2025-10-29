import random
import string
import json
from pathlib import Path

from classes import User, hash_string

NUM_USERS = 1000
MIN_BALANCE = 100
MAX_BALANCE = 1_000_000
RANDOM_SEED = 42
OUTPUT_FILE = "users.json"

random.seed(RANDOM_SEED)


def random_name(length: int = 8) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def random_pubkey() -> str:
    raw = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
    return hash_string(raw)


def make_users(n: int):
    users = []
    for _ in range(n):
        name = random_name()
        pk = random_pubkey()
        balance = random.randint(MIN_BALANCE, MAX_BALANCE)
        users.append(User(name, pk, balance))
    return users


def save_users(users, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([u.__dict__ for u in users], f, indent=2, ensure_ascii=False)


def main():
    users = make_users(NUM_USERS)
    save_users(users, OUTPUT_FILE)
    print(f"Generated {len(users)} users -> saved to {OUTPUT_FILE}")
    for u in users[:5]:
        print(f"{u.name} {u.public_key[:10]}... balance={u.balance}")


if __name__ == "__main__":
    main()
