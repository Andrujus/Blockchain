# reverse_hash_demo_limited.py
import itertools
import string
import time
import os
from hash_su_ai import simplehash_bytes  # naudosim bytes API

# ---------- Konfigai (keisk, jei reikia) ----------
FIXED_SALT = b"\xa1\xb2"  # 16 bytes example

CHARSET = string.ascii_lowercase + string.digits  # 'a-z0-9'
MAX_LEN = 3  # max brute-force message length
SALT_CHARSET = string.ascii_lowercase  # salt brute-force charset
SALT_MAX_LEN = 2  # max salt length when unknown

MAX_ATTEMPTS = 100000000  # STOP after this many attempts per search
SHOW_PROGRESS_EVERY = 50000  # how often to print progress (0 - disabled)

# ---------- Helper funkcijos ----------
def hash_bytes(data_bytes: bytes) -> str:
    return simplehash_bytes(data_bytes)

def hash_with_salt_bytes(data_bytes: bytes, salt: bytes = None) -> str:
    if salt is None:
        return hash_bytes(data_bytes)
    return hash_bytes(salt + data_bytes)

def prepare_bytes(data):
    if isinstance(data, str):
        return data.encode('utf-8')
    return data

# ---------- Bruteforce funkcijos (su attempt limit) ----------
def brute_force_no_salt(target_hash: str, charset=CHARSET, max_len=MAX_LEN, max_attempts=MAX_ATTEMPTS):
    attempts = 0
    t0 = time.time()
    for length in range(1, max_len + 1):
        for cand in itertools.product(charset, repeat=length):
            attempts += 1
            if attempts > max_attempts:
                return None, attempts, time.time() - t0, True
            s = ''.join(cand)
            if hash_with_salt_bytes(prepare_bytes(s), salt=None) == target_hash:
                return s, attempts, time.time() - t0, False
            if SHOW_PROGRESS_EVERY and attempts % SHOW_PROGRESS_EVERY == 0:
                print(f"[no-salt] Tried {attempts} candidates...")
    return None, attempts, time.time() - t0, False

def brute_force_known_salt(target_hash: str, salt: bytes, charset=CHARSET, max_len=MAX_LEN, max_attempts=MAX_ATTEMPTS):
    attempts = 0
    t0 = time.time()
    for length in range(1, max_len + 1):
        for cand in itertools.product(charset, repeat=length):
            attempts += 1
            if attempts > max_attempts:
                return None, attempts, time.time() - t0, True
            s = ''.join(cand)
            if hash_with_salt_bytes(prepare_bytes(s), salt=salt) == target_hash:
                return s, attempts, time.time() - t0, False
            if SHOW_PROGRESS_EVERY and attempts % SHOW_PROGRESS_EVERY == 0:
                print(f"[known-salt] Tried {attempts} candidates...")
    return None, attempts, time.time() - t0, False

def brute_force_unknown_salt(target_hash: str,
                             charset=CHARSET,
                             max_len=MAX_LEN,
                             salt_charset=SALT_CHARSET,
                             salt_max_len=SALT_MAX_LEN,
                             max_attempts=MAX_ATTEMPTS):
    attempts = 0
    t0 = time.time()
    for sl in range(1, salt_max_len + 1):
        for salt_cand in itertools.product(salt_charset, repeat=sl):
            salt_str = ''.join(salt_cand)
            salt_bytes = salt_str.encode('latin1')
            for length in range(1, max_len + 1):
                for cand in itertools.product(charset, repeat=length):
                    attempts += 1
                    if attempts > max_attempts:
                        return None, None, attempts, time.time() - t0, True
                    s = ''.join(cand)
                    if hash_with_salt_bytes(prepare_bytes(s), salt=salt_bytes) == target_hash:
                        return salt_str, s, attempts, time.time() - t0, False
                    if SHOW_PROGRESS_EVERY and attempts % SHOW_PROGRESS_EVERY == 0:
                        print(f"[unknown-salt] Tried {attempts} total combos...")
    return None, None, attempts, time.time() - t0, False

# ---------- Demo / UI ----------
def run_demo():
    print("=== Reverse puzzle (with attempt limit) ===")
    original = input("Įveskite originalų tekstą (patartina trumpas, pvz. 'ab1'): ").strip()
    if not original:
        print("Neįvestas tekstas. Išeinu.")
        return

    data_bytes = prepare_bytes(original)

    target_no_salt = hash_with_salt_bytes(data_bytes, salt=None)
    target_known_salt = hash_with_salt_bytes(data_bytes, salt=FIXED_SALT)
    unknown_salt = b"ac"  # random short salt for demo
    target_unknown_salt = hash_with_salt_bytes(data_bytes, salt=unknown_salt)

    print("\nTarget hashes:")
    print(" - No salt       :", target_no_salt)
    print(" - Known salt    :", target_known_salt)
    print(" - Unknown salt  :", target_unknown_salt, "(salt not shown)")

    print("\n--- Brute-force: no salt ---")
    found, attempts, elapsed, stopped = brute_force_no_salt(target_no_salt)
    if found:
        print(f"FOUND (no salt): '{found}' after {attempts} attempts in {elapsed:.2f}s")
    elif stopped:
        print(f"STOPPED (no salt) after reaching attempt limit ({attempts}) in {elapsed:.2f}s")
    else:
        print(f"NOT FOUND (no salt) after {attempts} attempts in {elapsed:.2f}s")

    print("\n--- Brute-force: known salt ---")
    found, attempts, elapsed, stopped = brute_force_known_salt(target_known_salt, FIXED_SALT)
    if found:
        print(f"FOUND (known salt): '{found}' after {attempts} attempts in {elapsed:.2f}s")
    elif stopped:
        print(f"STOPPED (known salt) after reaching attempt limit ({attempts}) in {elapsed:.2f}s")
    else:
        print(f"NOT FOUND (known salt) after {attempts} attempts in {elapsed:.2f}s")

    print("\n--- Brute-force: unknown salt (trying small salt space) ---")
    salt_found, msg_found, attempts, elapsed, stopped = brute_force_unknown_salt(target_unknown_salt)
    if msg_found:
        print(f"FOUND (unknown salt): salt='{salt_found}', message='{msg_found}' after {attempts} attempts in {elapsed:.2f}s")
        print(f"Actual unknown salt (for verification): {unknown_salt!r}")
    elif stopped:
        print(f"STOPPED (unknown salt) after reaching attempt limit ({attempts}) in {elapsed:.2f}s")
        print(f"Actual unknown salt (hidden during search): {unknown_salt!r}")
    else:
        print(f"NOT FOUND (unknown salt) after {attempts} attempts in {elapsed:.2f}s")
        print(f"Actual unknown salt (hidden during search): {unknown_salt!r}")

    print("\n--- DONE ---")
    print(f"Attempt limit per search was: {MAX_ATTEMPTS}")

if __name__ == "__main__":
    run_demo()
