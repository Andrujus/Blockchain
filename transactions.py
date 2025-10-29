"""
Blokų formavimas + kasimas + blockchain kūrimas + balansų atnaujinimas
======================================================================
Failas: transactions.py
"""
import json
import random
import time
from pathlib import Path

from classes import Transaction, Block, Header, hash_string, User

TX_FILE = "transactions.json"
BLOCKCHAIN_FILE = "blockchain.json"
USERS_FILE = "users.json"
RANDOM_SEED = 42

random.seed(RANDOM_SEED)


# ================== Pagalbinės funkcijos ==================
def load_transactions(path: str):
    """Užkrauna transakcijas iš JSON failo į Transaction objektus"""
    if not Path(path).exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Transaction(t["sender"], t["receiver"], t["amount"]) for t in data]


def save_transactions(txs, path: str):
    """Išsaugo transakcijas į JSON failą"""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([t.__dict__ for t in txs], f, indent=2, ensure_ascii=False)


def load_users(path: str):
    """Užkrauna vartotojus iš JSON failo į User objektus"""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [User(u["name"], u["public_key"], u["balance"]) for u in data]


def save_users(users, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([u.__dict__ for u in users], f, indent=2, ensure_ascii=False)


def pick_random_transactions(txs: list, k: int = 100) -> list:
    if k > len(txs):
        raise ValueError(f"Requested {k} transactions, but only {len(txs)} available")
    return random.sample(txs, k)


def mine_block(prev_hash: str, txs: list, k: int = 100, difficulty: str = "000") -> Block:
    """Formuoja ir kasa naują bloką (Proof-of-Work)."""
    selected = pick_random_transactions(txs, k)
    all_txids = "".join(tx.txid for tx in selected)
    transactions_hash = hash_string(all_txids)

    nonce = 0
    while True:
        header = Header(
            prev_block_hash=prev_hash,
            version="v0.1",
            transactions_hash=transactions_hash,
            nonce=nonce,
            difficulty=difficulty
        )
        block_hash = hash_string(header.serialize())
        if block_hash.startswith(difficulty):
            return Block(header, selected, block_hash)
        nonce += 1


def confirm_block(block: Block, txs: list, users: list):
    """Pašalina transakcijas iš sąrašo ir atnaujina balansus."""
    # Pašalinam įvykdytas transakcijas
    remaining = [t for t in txs if t.txid not in {x.txid for x in block.transactions}]

    # Vartotojų lookup
    user_map = {u.public_key: u for u in users}

    # Balansų atnaujinimas
    for tx in block.transactions:
        if tx.sender in user_map and tx.receiver in user_map:
            sender = user_map[tx.sender]
            receiver = user_map[tx.receiver]
            if sender.balance >= tx.amount:
                sender.balance -= tx.amount
                receiver.balance += tx.amount

    return remaining, list(user_map.values())


def save_blockchain(blocks: list, path: str):
    """Išsaugo pilną blockchain (blokų grandinę) į JSON"""
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    def block_to_dict(b: Block):
        return {
            "header": b.header.__dict__,
            "transactions": [t.__dict__ for t in b.transactions],
            "block_hash": b.block_hash
        }

    with open(path, "w", encoding="utf-8") as f:
        json.dump([block_to_dict(b) for b in blocks], f, indent=2, ensure_ascii=False)


# ================== Vykdymas ==================
def main():
    print(f"Loading users from {USERS_FILE}...")
    users = load_users(USERS_FILE)

    print(f"Loading transactions from {TX_FILE}...")
    txs = load_transactions(TX_FILE)
    print(f"Loaded {len(txs)} transactions")

    blockchain = []
    prev_hash = "0" * 64

    # Iškasame 3 blokus
    for i in range(78):
        if len(txs) < 100:
            print("Not enough transactions to form a block.")
            break

        print(f"\nMining block {i+1}/3...")
        start = time.time()
        blk = mine_block(prev_hash, txs, k=100, difficulty="000")
        end = time.time()
        print(f" Block {i+1} mined in {end-start:.2f} sec. Hash={blk.block_hash[:12]}...")

        # Patvirtiname bloką: pašalinam tx, atnaujinam balansus
        txs, users = confirm_block(blk, txs, users)

        blockchain.append(blk)
        prev_hash = blk.block_hash

        # === ČIA SVARBU ===
        # Išsaugom atnaujintus duomenis
        save_transactions(txs, TX_FILE)   # likusios transakcijos
        save_users(users, USERS_FILE)     # atnaujinti vartotojai

    # Išsaugome grandinę
    save_blockchain(blockchain, BLOCKCHAIN_FILE)

    print(f"\nBlockchain saved -> {BLOCKCHAIN_FILE}")
    print(f"Remaining transactions saved -> {TX_FILE}")
    print(f"Users updated -> {USERS_FILE}")


if __name__ == "__main__":
    main()
