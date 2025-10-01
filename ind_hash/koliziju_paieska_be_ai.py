# collision_test_existing_files.py
from pathlib import Path
from test_hash_be_ai import hash_string  # tavo hash funkcija

# Konfigūracija — atliksime testus tik su egzistuojančiais failais
OUT_DIR = Path("collision_pairs")
LENGTHS = [10, 100, 500, 1000]
PROGRESS_EVERY = 10_000  # kas kiek porų atspausdinti progresą

def test_collisions_from_file(path: Path):
    """Skaito failą eilutėmis ir tikrina kolizijas: s1\\ts2"""
    collisions = 0
    total = 0
    print(f"[test] Tikrinam: {path}")
    if not path.exists():
        print(f"  ! Failas neegzistuoja: {path} — praleidžiam.")
        return collisions, total

    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t", 1)
            if len(parts) != 2:
                # jei eilutė netinkamo formato, praleidžiam
                continue
            s1, s2 = parts
            h1 = hash_string(s1, print_output=False)
            h2 = hash_string(s2, print_output=False)
            if h1 == h2:
                collisions += 1
            total += 1
            if i % PROGRESS_EVERY == 0:
                print(f"  -> apdorota {i} porų, kolizijų: {collisions}")
    print(f"[done] {path.name}: apdorota {total} porų, kolizijų {collisions}")
    return collisions, total

def main():
    results = {}
    # Patikriname kiekvieną ilgį (tik jei atitinkamas failas egzistuoja)
    for L in LENGTHS:
        path = OUT_DIR / f"pairs_len{L}.txt"
        if not path.exists():
            print(f"[skip] Failas nerastas: {path}")
            continue
        c, t = test_collisions_from_file(path)
        results[L] = (c, t)

    # Santrauka
    print("\n=== GALUTINIAI REZULTATAI ===")
    if not results:
        print("Nei vienas testuojamas failas nerastas. Įdėk pairs_len{L}.txt į collision_pairs/")
        return

    for L in sorted(results.keys()):
        c, t = results[L]
        perc = (c / t * 100) if t else 0.0
        print(f"Ilgis {L}: {c} kolizijų iš {t} porų ({perc:.6f}%)")

if __name__ == "__main__":
    main()