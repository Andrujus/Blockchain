from merkle import merkle_root
from classes import hash_string

# Dummy test
txids = [
    hash_string("Tx1"),
    hash_string("Tx2"),
    hash_string("Tx3"),
    hash_string("Tx4"),
]
print("Merkle Root =", merkle_root(txids))
