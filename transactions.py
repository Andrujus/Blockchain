import random
import string

from classes import Transaction, User, Block, Header, hash_string

NUM_USERS = 1000
NUM_TRANSACTIONS = 10_000
RANDOM_SEED = 42
MIN_BALANCE = 100
MAX_BALANCE = 1_000_000
MIN_AMOUNT = 1
MAX_AMOUNT = 10_000

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


def generate_transactions(users, count: int):
    txs = []
    user_keys = [u.public_key for u in users]
    for _ in range(count):
        sender = random.choice(user_keys)
        receiver = random.choice(user_keys)
        while receiver == sender:
            receiver = random.choice(user_keys)
        amount = random.randint(MIN_AMOUNT, MAX_AMOUNT)
        tx = Transaction(sender, receiver, amount)  # Transaction pats sugeneruos txid
        txs.append(tx)
    return txs


def pick_random_transactions(txs: list, k: int = 100) -> list:
    if k > len(txs):
        raise ValueError(f"Requested {k} transactions, but only {len(txs)} available")
    return random.sample(txs, k)


def form_new_block(prev_hash: str, txs: list, k: int = 100) -> Block:
    selected = pick_random_transactions(txs, k)
    all_txids = "".join(tx.txid for tx in selected)
    transactions_hash = hash_string(all_txids)

    header = Header(
        prev_block_hash=prev_hash,
        version="v0.1",
        transactions_hash=transactions_hash,
        nonce=0,
    )
    block_hash = hash_string(header.serialize())
    return Block(header, selected, block_hash)


def main():
    print(f"Generating {NUM_USERS} users...")
    users = make_users(NUM_USERS)
    print(f"Generating {NUM_TRANSACTIONS} transactions...")
    txs = generate_transactions(users, NUM_TRANSACTIONS)
    print(f"Generated {len(txs)} transactions")
    print("Example 3 transactions:")
    for t in txs[:3]:
        print(f"{t.txid[:10]}... {t.amount} from {t.sender[:8]} -> {t.receiver[:8]}")

    print("Selecting 100 random transactions for a new block...")
    new_blk = form_new_block("0"*64, txs, 100)
    print(f"New block prepared with {len(new_blk.transactions)} transactions")
    print("First 5 tx in the block:")
    for t in new_blk.transactions[:5]:
        print(f"{t.txid[:10]}... {t.amount} from {t.sender[:8]} -> {t.receiver[:8]}")


if __name__ == "__main__":
    main()
