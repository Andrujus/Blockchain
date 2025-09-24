import time
import matplotlib.pyplot as plt
from hash_be_ai import hash_string

def measure_time(data: bytes, repeats=5):
    """Pamatuoja hashavimo laiką, grąžina vidurkį (sekundėmis)."""
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        hash_string(data)
        end = time.perf_counter()
        times.append(end - start)
    return sum(times) / len(times)

def main():
    # nuskaitom visą konstitucija.txt
    with open("test_files/konstitucija.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    sizes = []
    avg_times = []

    n = 1  # pradedam nuo 1 eilutės
    while n <= len(lines):
        test_data = "".join(lines[:n]).encode("utf-8")
        avg_time = measure_time(test_data, repeats=5)
        sizes.append(n)
        avg_times.append(avg_time)
        print(f"{n} eilutės -> {avg_time:.6f} s")
        n *= 2  # didinam 2 kartus

    # piešiam grafiką
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, avg_times, marker="o", linestyle="-", color="blue")
    plt.xlabel("Įvedimo dydis (eilutės)")
    plt.ylabel("Vidutinis hashavimo laikas (s)")
    plt.title("SimpleHash efektyvumo matavimai")
    plt.grid(True)
    plt.xscale("log")
    plt.yscale("log")
    plt.savefig("efektyvumas.png", dpi=150)  # išsaugom paveiksliuką
    plt.show()

if __name__ == "__main__":
    main()
