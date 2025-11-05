def rotl64(x, r):
    return ((x << r) & ((1 << 64) - 1))


def hash_string(user_input):
    MASK64 = (1 << 64) - 1
    h1 = 0x1234567890abcdef
    h2 = 0xfedcba0987654321
    h3 = 0xabcdef1234567890
    h4 = 0x0987654321fedcba

    if isinstance(user_input, str):
        user_input = user_input.encode('utf-8')

    for b in user_input:
        h1 ^= b
        h1 = (rotl64(h1, 13) * 31 + (b ^ (b >> 3))) & MASK64

        h2 ^= rotl64(b, 7)
        h2 = (h2 * 27 + (b ^ (b >> 5))) & MASK64

        h3 ^= rotl64(b, 10)
        h3 = (h3 * 29 + (b ^ (b >> 7))) & MASK64

        h4 ^= rotl64(b, 17)
        h4 = (h4 * 37 + (b ^ (b >> 11))) & MASK64

    mix = (h1 ^ h2 ^ h3 ^ h4) & MASK64
    h1 = (h1 ^ rotl64(mix, 5)) & MASK64
    h2 = (h2 ^ rotl64(mix, 11)) & MASK64
    h3 = (h3 ^ rotl64(mix, 23)) & MASK64
    h4 = (h4 ^ rotl64(mix, 37)) & MASK64

    rez1 = f"{h1:016x}"
    rez2 = f"{h2:016x}"
    rez3 = f"{h3:016x}"
    rez4 = f"{h4:016x}"
    return f"{rez1}{rez2}{rez3}{rez4}"



class User:
    def __init__(self, name: str, public_key: str, balance: int):
        self.name = name
        self.public_key = public_key
        self.balance = balance


class Transaction:
    def __init__(self, sender: str, receiver: str, amount: int, txid: str | None = None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

        raw = f"{sender}|{receiver}|{amount}"
        self.computed_txid = hash_string(raw)
        self.txid = txid if txid is not None else self.computed_txid

    def is_txid_valid(self) -> bool:
        return self.txid == self.computed_txid


class Header:
    def __init__(self, prev_block_hash: str, version: str, transactions_hash: str, nonce: int, difficulty: str):
        import time
        self.prev_block_hash = prev_block_hash
        self.version = version
        self.transactions_hash = transactions_hash
        self.nonce = nonce
        self.difficulty = difficulty 
        self.timestamp = int(time.time())

    def serialize(self) -> str:
        return f"{self.prev_block_hash}|{self.version}|{self.transactions_hash}|{self.nonce}|{self.timestamp}"


class Block:
    def __init__(self, header: Header, transactions: list, block_hash: str):
        self.header = header
        self.transactions = transactions
        self.block_hash = block_hash
