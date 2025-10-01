from hash_su_ai import simplehash_string as org_hash_string

FIXED_SALT = bytes.fromhex("a1b2c3d4e5f60718293a4b5c6d7e8f90")

def hash_with_salt(data):
    if isinstance(data, str):
        data_bytes = data.encode('utf-8')
    else:
        data_bytes = data
    return org_hash_string(FIXED_SALT + data_bytes) 

def demonstrate_irreversibility():
    original = "SlaptasTekstas"
    modified = "SlaptasTekstaa"

    hash_orig = hash_with_salt(original)
    hash_mod  = hash_with_salt(modified)

    print("Original string:", original)
    print("Hash with fixed salt:", hash_orig)
    print("\nModified string:", modified)
    print("Hash with fixed salt:", hash_mod)

if __name__ == "__main__":
    demonstrate_irreversibility()
