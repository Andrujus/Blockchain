# simplehash.py
import struct
import sys

# --- 1) Rotacija ---
def rotl32(x, r):
    return ((x << r) & 0xFFFFFFFF) | (x >> (32 - r))

# --- 2) 4 baitų paėmimas ---
def u32_le(b, i):
    chunk = b[i:i+4]
    if len(chunk) < 4:
        chunk = chunk + b'\x00' * (4 - len(chunk))
    return struct.unpack('<I', chunk)[0]

# --- 3) Padding ---
def pad(data: bytes) -> bytes:
    bit_len = (len(data) * 8) & 0xFFFFFFFF
    padded = data + b'\x80'
    while len(padded) % 4 != 0:
        padded += b'\x00'
    padded += struct.pack('<I', bit_len)
    return padded

# --- 4) Mix funkcija ---
def mix_once(st):
    for i in range(8):
        a = st[i]
        b = st[(i+1) % 8]
        c = ((a ^ rotl32(b, (i+1) % 31)) * 0x85ebca6b) & 0xFFFFFFFF
        st[i] = ((st[i] + c) ^ rotl32(st[(i+3) % 8], (i*7) % 31)) & 0xFFFFFFFF
    # permutacija
    st[0], st[2], st[4], st[6] = st[2], st[4], st[6], st[0]

# --- 5) Pagrindinė hash funkcija ---
def simplehash_bytes(data: bytes, rounds_per_block=3, final_rounds=16):
    # pradinė būsena (8 žodžiai po 32 bitus)
    primes = [2, 3, 5, 7, 11, 13, 17, 19]
    state = [((p * 0x9e3779b1) ^ (p << (i+3))) & 0xFFFFFFFF 
             for i, p in enumerate(primes)]

    padded = pad(data)

    # apdorojam kiekvieną 4 baitų žodį
    for i in range(0, len(padded), 4):
        w = u32_le(padded, i)
        idx = (i // 4) % 8
        state[idx] = (state[idx] ^ ((w + 0x9e3779b1) & 0xFFFFFFFF)) & 0xFFFFFFFF
        for _ in range(rounds_per_block):
            mix_once(state)

    # finalizacija
    bit_len = (len(data) * 8) & 0xFFFFFFFF
    state[0] ^= bit_len
    for r in range(final_rounds):
        state[(r*3) % 8] = (state[(r*3) % 8] + 0x6a09e667) & 0xFFFFFFFF
        mix_once(state)

    # išvestis: 64 hex simboliai
    return ''.join(f'{w:08x}' for w in state)

def simplehash_string(s: str, **kwargs):
    return simplehash_bytes(s.encode('utf-8'), **kwargs)

# --- Paleidimas ---
if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            print(simplehash_bytes(data))
        except FileNotFoundError:
            print(f"Failas '{file_path}' nerastas.")
            sys.exit(1)
        except Exception as e:
            print(f"Klaida skaitant failą: {e}")
            sys.exit(1)
    else:
        zinute = input("Įveskite žinutę hash'inimui: ")
        print(simplehash_string(zinute))