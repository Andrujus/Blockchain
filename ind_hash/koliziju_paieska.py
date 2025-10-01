# collision_test_with_files.py
import random
import string
from pathlib import Path
from hash_su_ai import simplehash_string  # tavo hash implementacija

# --- Konfigūracija ---
LENGTHS = [10, 100, 500, 1000]
PAIRS = 100_000
OUT_DIR = Path("collision_pairs")
PROGRESS_EVERY = 10_000

rng = random.SystemRandom()


def random_string(length: int) -> str:
    """Sugeneruoja atsitiktinį stringą iš raidžių ir skaičių."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(rng.choices(alphabet, k=length))


def generate_pair_file(length: int, pairs: int = PAIRS, out_dir: Path = OUT_DIR):
    """Sugeneruoja failą su poromis: s1 \t s2"""
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"pairs_len{length}.txt"

    if path.exists():
        existing_lines = sum(1 for _ in open(path, "r", encoding="utf-8"))
        if existing_lines >= pairs:
            print(f"[skip] Failas {path} jau egzistuoja ({existing_lines} eilučių).")
            return path

    print(f"[gen] Generuojam {pairs} porų: {path} (ilgis={length})")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for i in range(1, pairs + 1):
            s1 = random_string(length)
            s2 = random_string(length)
            f.write(f"{s1}\t{s2}\n")
            if i % PROGRESS_EVERY == 0:
                print(f"  -> sugeneruota {i}/{pairs}")
    return path


def test_collisions_from_file(path: Path):
    """Skaito failą eilutėmis ir tikrina kolizijas."""
    collisions = 0
    total = 0
    print(f"[test] Tikrinam: {path}")
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            s1, s2 = line.strip().split("\t", 1)
            h1 = simplehash_string(s1)
            h2 = simplehash_string(s2)
            if h1 == h2:
                collisions += 1
            total += 1
            if i % PROGRESS_EVERY == 0:
                print(f"  -> {i} porų, kolizijų: {collisions}")
    print(f"[done] {path.name}: {total} porų, kolizijų {collisions}")
    return collisions, total


def main():
    results = {}
    # Sugeneruoti failus
    for L in LENGTHS:
        generate_pair_file(L, PAIRS, OUT_DIR)
    # Patikrinti kolizijas
    for L in LENGTHS:
        path = OUT_DIR / f"pairs_len{L}.txt"
        c, t = test_collisions_from_file(path)
        results[L] = (c, t)

    print("\n=== GALUTINIAI REZULTATAI ===")
    for L in LENGTHS:
        c, t = results[L]
        perc = c / t * 100 if t else 0
        print(f"Ilgis {L}: {c} kolizijų iš {t} porų ({perc:.6f}%)")


if __name__ == "__main__":
    main()