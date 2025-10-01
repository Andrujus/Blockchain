from hash_be_ai import hash_string

FIXED_SALT = bytes.fromhex("a1b2c3d4e5f60718293a4b5c6d7e8f90")
MASK64 = (1 << 64) - 1

def rotl64(x, r):
    return ((x << r) | (x >> (64 - r))) & MASK64


def demonstrate_irreversibility():
    original = "SlaptasTekstas"
    modified = "SlaptasTekstas!"  

    hash_orig = hash_string(original)
    hash_mod = hash_string(modified)

    print("Original string:", original)
    print("Hash:", hash_orig)
    print("\nModified string:", modified)
    print("Hash:", hash_mod)


demonstrate_irreversibility()
