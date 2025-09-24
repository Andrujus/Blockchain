import time
import matplotlib.pyplot as plt
from test_hash_be_ai import hash_string  # importuojam iš tavo failo

def benchmark_hash(lines, repeats=5):
    text = "\n".join(lines)
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        hash_string(text, print_output=False)  # naudosim tik skaičiavimą, be print
        end = time.perf_counter()
        times.append(end - start)
    return sum(times) / len(times)

def main():
    file = "test_files/konstitucija.txt"
    with open(file, encoding="utf-8") as f:
        all_lines = f.readlines()

    sizes = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    results = {}

    for n in sizes:
        avg_time = benchmark_hash(all_lines[:n])
        results[n] = avg_time
        print(f"{n} eilutės -> {avg_time:.6f} s")

    # grafikas
    plt.plot(list(results.keys()), list(results.values()), marker='o')
    plt.xlabel("Eilučių skaičius")
    plt.ylabel("Vidutinis laikas (s)")
    plt.title("Hash algoritmo efektyvumas")
    plt.grid(True)
    plt.savefig("efektyvumas_be_ai.png")
    plt.show()

if __name__ == "__main__":
    main()
