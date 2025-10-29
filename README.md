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

2. **Transakcijos**  
   Sugeneruojama 10 000 atsitiktinių transakcijų tarp vartotojų.  
   Išsaugoma į `transactions.json`.

3. **Bloko formavimas**  
   Atsitiktinai parenkama 100 transakcijų, jos supakuojamos į bloką.  
   Sukuriamas `Header`, sugeneruojamas bloko hash.

4. **Kasimas (Proof-of-Work)**  
   Blokas kasamas tol, kol hash prasideda nulių seka pagal `difficulty` (pvz., `"000"`).

5. **Patvirtinimas**  
   - Įtrauktos transakcijos pašalinamos iš `transactions.json`.
   - Atnaujinami vartotojų balansai faile `users.json`.
   - Naujas blokas įtraukiamas į `blockchain.json`.

## Naudojimas

### 1. Sugeneruoti vartotojus ir transakcijas
```bash
python users.py
python transactions_gen.py
```

### 2. Iškasti blokus
```bash
python transactions.py
```

Rezultatai:
- `users.json` – vartotojų sąrašas ir jų balansai.
- `transactions.json` – likusios transakcijos (nepanaudotos).
- `blockchain.json` – blokų grandinė su patvirtintais blokais.
