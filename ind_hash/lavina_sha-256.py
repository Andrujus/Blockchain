# lavina_test_existing_files.py
import hashlib

def bit_difference(h1, h2):
    return bin(int(h1, 16) ^ int(h2, 16)).count('1')

def hex_difference(h1, h2):
    return sum(c1 != c2 for c1, c2 in zip(h1, h2))

def run_avalanche_test(file_path):
    bit_diffs = []
    hex_diffs = []
    identical_pairs = []  # saugome identiškas poras

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            s1, s2 = line.strip().split(maxsplit=1)
            h1 = hashlib.sha256(s1.encode('utf-8')).hexdigest()
            h2 = hashlib.sha256(s2.encode('utf-8')).hexdigest()
            
            bit_diff = bit_difference(h1, h2)
            hex_diff = hex_difference(h1, h2)
            bit_diffs.append(bit_diff)
            hex_diffs.append(hex_diff)

            # patikrinam, ar hash'ai visiškai identiški
            if bit_diff == 0:
                identical_pairs.append((s1, s2, h1))

    print(f"[{file_path}]")
    print(f"Bits -> min: {min(bit_diffs)}, max: {max(bit_diffs)}, avg: {sum(bit_diffs)/len(bit_diffs):.2f}")
    print(f"Hex  -> min: {min(hex_diffs)}, max: {max(hex_diffs)}, avg: {sum(hex_diffs)/len(hex_diffs):.2f}")

    if identical_pairs:
        print("\n=== Identical hash pairs found ===")
        for s1, s2, h in identical_pairs:
            print(f"'{s1}'  |  '{s2}'  -> {h}")
    else:
        print("\nNo identical hash pairs found.")

if __name__ == "__main__":
    files = [
        "ind_hash/avalanche_pairs/avalanche_len50_pairs100000.txt",
    ]

    for f in files:
        run_avalanche_test(f)