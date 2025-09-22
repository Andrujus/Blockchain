def rotl64(x, r):
    return ((x << r) & ((1 << 64) - 1))

def hash_string(user_input):
    MASK64 = (1 << 64) - 1
    h1 = 0x1234567890abcdef
    h2 = 0xfedcba0987654321
    h3 = 0xabcdef1234567890
    h4 = 0x0987654321fedcba
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

    print(f"Hash'as: {rez1}{rez2}{rez3}{rez4}")

def hash_file(file):
    with open(file) as f:
        f_input = f.read()
    hash_string(f_input)
     



loop = True
while loop == True:
    input_str = input("Ar norite hash'inti faila ar string? (f/s): ").strip().lower()
    if input_str == 'f':
        file = input("Iveskite failo pavadinima: ")
        hash_file(file)

    elif input_str == 's':
        user_input = input("Iveskite teksta: ")
        hash_string(user_input)
    else:
        print("Neteisinga ivestis")
        loop = False
        