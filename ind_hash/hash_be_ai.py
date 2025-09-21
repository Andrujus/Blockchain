

def hash_string():
    user_input = input("Iveskite teksta: ")
    MASK64 = (1 << 64) - 1
    h = 0x1234567890abcdef
    user_input = user_input.encode('utf-8')
    for b in user_input:
        h = (h*31 + b) & MASK64
    print(f"Hash'as: {h}")



loop = True
while loop == True:
    input_str = input("Ar norite hash'inti faila ar string? (f/s): ").strip().lower()
    if input_str == 'f':
        file = input("Iveskite failo pavadinima: ")
        hash_file(file)

    elif input_str == 's':
        hash_string()
    else:
        print("Neteisinga ivestis")
        loop = False
        