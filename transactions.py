import random
import string
import json

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


def save_users_to_json(users: list, filename: str = "users.json"):
    """Save users list to JSON file."""
    users_data = []
    for user in users:
        users_data.append({
            "name": user.name,
            "public_key": user.public_key,
            "balance": user.balance
        })
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(users)} users to {filename}")


def save_transactions_to_json(transactions: list, filename: str = "transactions.json"):
    """Save transactions list to JSON file."""
    tx_data = []
    for tx in transactions:
        tx_data.append({
            "txid": tx.txid,
            "sender": tx.sender,
            "receiver": tx.receiver,
            "amount": tx.amount
        })
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tx_data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(transactions)} transactions to {filename}")


def save_blocks_to_json(blocks: list, filename: str = "blocks.json"):
    """Save blocks list to JSON file."""
    blocks_data = []
    for block in blocks:
        # Convert transactions in block to dict format
        block_txs = []
        for tx in block.transactions:
            block_txs.append({
                "txid": tx.txid,
                "sender": tx.sender,
                "receiver": tx.receiver,
                "amount": tx.amount
            })
        
        blocks_data.append({
            "block_hash": block.block_hash,
            "header": {
                "prev_block_hash": block.header.prev_block_hash,
                "version": block.header.version,
                "transactions_hash": block.header.transactions_hash,
                "nonce": block.header.nonce
            },
            "transactions": block_txs
        })
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(blocks_data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(blocks)} blocks to {filename}")


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

    # Save all data to JSON files
    print("\nSaving data to JSON files...")
    save_users_to_json(users)
    save_transactions_to_json(txs)
    save_blocks_to_json([new_blk])  # Pass as list since function expects list


if __name__ == "__main__":
    main()
