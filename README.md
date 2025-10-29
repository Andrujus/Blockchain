# Supaprastinta Blockchain realizacija v0.1


## Struktūra

- **classes.py** – pagrindinės klasės: `User`, `Transaction`, `Header`, `Block`, taip pat maišos funkcija `hash_string` (iš pirmos užduoties).
- **users.py** – vartotojų generavimas, jų saugojimas ir įkėlimas.
- **txgen.py** – transakcijų generavimas tarp vartotojų ir išsaugojimas į failą.
- **transactions.py** – blokų kasimas, patvirtinimas, balansų atnaujinimas ir blockchain išsaugojimas.

## Funkcionalumas

1. **Vartotojai**  
   Sukuriama 1000 vartotojų su atsitiktiniais vardais, viešais raktais ir pradiniais balansais.
   Išsaugoma į `users.json`.
   <img width="1137" height="692" alt="image" src="https://github.com/user-attachments/assets/a00f6bf2-5144-4302-86ed-d91f7e03d89c" />


2. **Transakcijos**  
   Sugeneruojama 10 000 atsitiktinių transakcijų tarp vartotojų.  
   Išsaugoma į `transactions.json`.
   <img width="1115" height="615" alt="image" src="https://github.com/user-attachments/assets/d2428820-35dc-4a54-a92f-7e26f09a61dc" />


4. **Bloko formavimas**  
   Atsitiktinai parenkama 100 transakcijų, jos supakuojamos į bloką.  
   Sukuriamas `Header`, sugeneruojamas bloko hash.
   <img width="1186" height="176" alt="image" src="https://github.com/user-attachments/assets/e5b72b05-790b-42bd-aa8b-ef7706532ba4" />

5. **Kasimas (Proof-of-Work)**  
   Blokas kasamas tol, kol hash prasideda nulių seka pagal `difficulty` (pvz., `"000"`).
   <img width="1235" height="622" alt="image" src="https://github.com/user-attachments/assets/85122116-35fb-43ec-b39f-6ad6f0d4e294" />


6. **Patvirtinimas**  
   - Įtrauktos transakcijos pašalinamos iš `transactions.json`.
   - Atnaujinami vartotojų balansai faile `users.json`.
   - Naujas blokas įtraukiamas į `blockchain.json`.
   <img width="1192" height="554" alt="image" src="https://github.com/user-attachments/assets/fae21703-5e64-45e1-86a5-49f5db2a0222" />


## Naudojimas

### 1. Sugeneruoti vartotojus ir transakcijas
```bash
python users.py
python txgen.py
```

### 2. Iškasti blokus
```bash
python transactions.py
```

Rezultatai:
- `users.json` – vartotojų sąrašas ir jų balansai.
- `transactions.json` – likusios transakcijos (nepanaudotos).
- `blockchain.json` – blokų grandinė su patvirtintais blokais.
