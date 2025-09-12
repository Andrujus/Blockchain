import hashlib

def hash_string():
    user_input = input("Enter a string to hash: ")
    hashed = hashlib.sha1(user_input.encode()).hexdigest()
    print(f"SHA-1 hash of {user_input}: {hashed}")
loop = True
while loop == True:
    input_str = input("Ar norite hash'inti failą ar stringą? (f/s): ").strip().lower()
    if input_str == 'f':
        break
    elif input_str == 's':
        hash_string()
    else:
        print("Neteisinga įvestis")
        loop = False
        