from typing import List
from classes import hash_string

def merkle_root(txids: List[str]) -> str:
    if not txids:
        return hash_string("")

    level = [bytes.fromhex(txid) for txid in txids]
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])

        new_level = []
        for i in range(0, len(level), 2):
            combined = level[i] + level[i+1]
            new_hash_hex = hash_string(combined.hex())
            new_level.append(bytes.fromhex(new_hash_hex))

        level = new_level

    return level[0].hex()
