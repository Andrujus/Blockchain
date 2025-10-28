import random
import string
import hashlib
import json
from pathlib import Path

NUM_USERS = 1000
MIN_BALANCE = 100
MAX_BALANCE = 1_000_000
RANDOM_SEED = 42
OUTPUT_FILE = "users.json"

random.seed(RANDOM_SEED)

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def random_name(length: int = 8) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def random_pubkey() -> str:
    raw = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
    return sha256_hex(raw)

def generate_users(n: int):
    users = []
    for _ in range(n):
        name = random_name()
        pk = random_pubkey()
        balance = random.randint(MIN_BALANCE, MAX_BALANCE)
        users.append({
            "name": name,
            "public_key": pk,
            "balance": balance
        })
    return users

def save_users(users, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def main():
    print(f"Generating {NUM_USERS} users...")
    users = generate_users(NUM_USERS)
    save_users(users, OUTPUT_FILE)
    print(f"Saved to {OUTPUT_FILE}")
    print("Example 3 users:")
    for u in users[:3]:
        print(f"  {u['name']} {u['public_key'][:10]}... balance={u['balance']}")

if __name__ == "__main__":
    main()
