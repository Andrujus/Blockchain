
def rotl64(x, r):
    """64 bitų rotacija į kairę."""
    return ((x << r) & ((1 << 64) - 1)) | (x >> (64 - r))

def hash_string(user_input, print_output=True):
    """Apskaičiuoja 64-bitų hash kombinaciją h1-h4.
       print_output=False tik skaičiuoja, nespausdina.
    """
    MASK64 = (1 << 64) - 1
    h1 = 0x1234567890abcdef
    h2 = 0xfedcba0987654321
    h3 = 0xabcdef1234567890
    h4 = 0x0987654321fedcba

    if isinstance(user_input, str):
        user_input = user_input.encode('utf-8')

    for b in user_input:
        h1 ^= b
        h1 = rotl64(h1, 13)
        h1 = (h1 * 31 + b ^ (b >> 3)) & MASK64

        h2 ^= rotl64(b, 7)
        h2 = (h2 * 27 + b ^ (b >> 5)) & MASK64

        h3 ^= rotl64(b, 10)
        h3 = (h3 * 29 + b ^ (b >> 7)) & MASK64

        h4 ^= rotl64(b, 17)
        h4 = (h4 * 37 + b ^ (b >> 11)) & MASK64

    rez1 = f"{h1:016x}"
    rez2 = f"{h2:016x}"
    rez3 = f"{h3:016x}"
    rez4 = f"{h4:016x}"

    result = rez1 + rez2 + rez3 + rez4

    if print_output:
        print(f"Hash'as: {result}")

    return result

def hash_file(file_path, print_output=True):
    """Hashuoja visą failą."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return hash_string(content, print_output=print_output)

# --- Interaktyvus paleidimas ---
if __name__ == "__main__":
    loop = True
    while loop:
        choice = input("Ar norite hash'inti failą ar string? (f/s): ").strip().lower()
        if choice == 'f':
            file_path = input("Įveskite failo pavadinimą: ").strip()
            try:
                hash_file(file_path)
            except FileNotFoundError:
                print(f"Failas '{file_path}' nerastas.")
        elif choice == 's':
            user_input = input("Įveskite tekstą: ")
            hash_string(user_input)
        else:
            print("Neteisinga įvestis, programa baigiama.")
            loop = False
