"""
Blokų formavimas + kasimas + blockchain kūrimas
==============================================
Failas: transactions.py
"""
import json
import random
import time
from pathlib import Path

from classes import Transaction, Block, Header, hash_string

TX_FILE = "transactions.json"
BLOCK_FILE = "blocks.json"
BLOCKCHAIN_FILE = "blockchain.json"
RANDOM_SEED = 42

random.seed(RANDOM_SEED)


# ================== Pagalbinės funkcijos ==================
def load_transactions(path: str):
    """Užkrauna transakcijas iš JSON failo į Transaction objektus"""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Transaction(t["sender"], t["receiver"], t["amount"]) for t in data]


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


def save_blockchain(blocks: list, path: str):
    """Išsaugo pilną blockchain (blokų grandinę) į JSON"""
    save_blocks(blocks, path)


def build_blockchain(txs, n_blocks: int = 3, k: int = 100, difficulty: str = "000"):
    """Iškasa kelis blokus ir suformuoja grandinę"""
    blockchain = []
    prev_hash = "0" * 64

    for i in range(n_blocks):
        print(f"Mining block {i+1}/{n_blocks}...")
        start = time.time()
        blk = mine_block(prev_hash, txs, k=k, difficulty=difficulty)
        end = time.time()
        blockchain.append(blk)
        prev_hash = blk.block_hash
        print(f" Block {i+1} mined in {end-start:.2f} sec. Hash={blk.block_hash[:12]}...")
    
    return blockchain

def main():
    print(f"Loading transactions from {TX_FILE}...")
    txs = load_transactions(TX_FILE)
    print(f"Loaded {len(txs)} transactions")

    blockchain = build_blockchain(txs, n_blocks=3, k=100, difficulty="000")
    save_blockchain(blockchain, BLOCKCHAIN_FILE)
    print(f"Blockchain saved -> {BLOCKCHAIN_FILE}")


if __name__ == "__main__":
    main()
