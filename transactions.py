"""
Transactions ir blokų formavimas + kasimas
==========================================
Failas: transactions.py
"""
import random
import json
from pathlib import Path
import time

from classes import Transaction, User, Block, Header, hash_string
from users import make_users, save_users

NUM_USERS = 1000
NUM_TRANSACTIONS = 10_000
RANDOM_SEED = 42
MIN_AMOUNT = 1
MAX_AMOUNT = 10_000
TX_FILE = "transactions.json"
BLOCK_FILE = "blocks.json"
USERS_FILE = "users.json"

random.seed(RANDOM_SEED)


def generate_transactions(users, count: int):
    txs = []
    user_keys = [u.public_key for u in users]
    for _ in range(count):
        sender = random.choice(user_keys)
        receiver = random.choice(user_keys)
        while receiver == sender:
            receiver = random.choice(user_keys)
        amount = random.randint(MIN_AMOUNT, MAX_AMOUNT)
        tx = Transaction(sender, receiver, amount)
        txs.append(tx)
    return txs


def save_transactions(txs, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([t.__dict__ for t in txs], f, indent=2, ensure_ascii=False)


def pick_random_transactions(txs: list, k: int = 100) -> list:
    if k > len(txs):
        raise ValueError(f"Requested {k} transactions, but only {len(txs)} available")
    return random.sample(txs, k)


def mine_block(prev_hash: str, txs: list, k: int = 100, difficulty: str = "000") -> Block:
    """
    Formuoja ir kasa naują bloką (Proof-of-Work).
    """
    selected = pick_random_transactions(txs, k)
    all_txids = "".join(tx.txid for tx in selected)
    transactions_hash = hash_string(all_txids)

    nonce = 0
    while True:
        # Difficulty saugomas tik header'e kaip info, bet nenaudojamas hash'e
        header = Header(
            prev_block_hash=prev_hash,
            version="v0.1",
            transactions_hash=transactions_hash,
            nonce=nonce,
            difficulty=difficulty
        )
        # Hashuojam tik serialize (be difficulty)
        block_hash = hash_string(header.serialize())
        if block_hash.startswith(difficulty):
            # Radom tinkamą hash
            return Block(header, selected, block_hash)
        nonce += 1


def save_blocks(blocks: list, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    def block_to_dict(b: Block):
        return {
            "header": b.header.__dict__,
            "transactions": [t.__dict__ for t in b.transactions],
            "block_hash": b.block_hash
        }

    with open(path, "w", encoding="utf-8") as f:
        json.dump([block_to_dict(b) for b in blocks], f, indent=2, ensure_ascii=False)


def main():
    print(f"Generating {NUM_USERS} users...")
    users = make_users(NUM_USERS)
    save_users(users, USERS_FILE)

    print(f"Generating {NUM_TRANSACTIONS} transactions...")
    txs = generate_transactions(users, NUM_TRANSACTIONS)
    save_transactions(txs, TX_FILE)
    print(f"Saved {len(txs)} transactions -> {TX_FILE}")

    print("Mining new block with 100 random transactions...")
    start = time.time()
    new_blk = mine_block("0"*64, txs, 100, difficulty="000")
    end = time.time()
    save_blocks([new_blk], BLOCK_FILE)
    print(f"Block mined! Hash={new_blk.block_hash[:12]}... in {end-start:.2f} sec")
    print(f"Saved block -> {BLOCK_FILE}")

    print("First 3 transactions in block:")
    for t in new_blk.transactions[:3]:
        print(f"{t.txid[:10]}... {t.amount} from {t.sender[:8]} -> {t.receiver[:8]}")


if __name__ == "__main__":
    main()
