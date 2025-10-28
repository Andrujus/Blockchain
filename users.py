import random
import string
import hashlib

from classes import User

NUM_USERS = 1000
MIN_BALANCE = 100
MAX_BALANCE = 1_000_000
RANDOM_SEED = 42

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
        users.append(User(name, pk, balance))
    return users

def main():
    print(f"Generating {NUM_USERS} users...")
    users = generate_users(NUM_USERS)
    print("Example 3 users:")
    for u in users[:3]:
        print(" ", u)
        print("    Name: ", u.name)
        print("    Public Key: ", u.public_key)
        print("    Balance: ", u.balance)

if __name__ == "__main__":
    main()