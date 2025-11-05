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

# Supaprastinta Blockchain realizacija v0.2

Ši versija išplečia ankstesnį projektą (v0.1), pridėdama **Merkle medžio**, **transakcijų verifikacijos** ir **patobulinto kasimo proceso** funkcionalumą.
Vykdant šią versiją buvo laikomasi užduoties reikalavimų ir palaipsniui integruoti nauji komponentai.

---

## Naujos funkcijos ir patobulinimai

### 1. **Merkle Tree ir Merkle Root Hash**

Transakcijų maišos dabar formuojamos naudojant **Merkle medį** (`merkle.py`):

* kiekvienos transakcijos `txid` yra įtraukiamas kaip lapas;
* lapai poruojami ir maišomi į naujus mazgus;
* galutinis „šaknis“ (Merkle Root Hash) įrašomas į `Header` lauką `transactions_hash`.


<img width="902" height="745" alt="image" src="https://github.com/user-attachments/assets/0e22ef82-30e2-4e06-b2f2-9c768db947fd" />


---

### 2. **Transakcijų verifikacija**

Įdiegta pilna transakcijų patikra prieš įtraukiant į bloką:

* **TXID tikrinimas** – kiekvienai transakcijai iš naujo apskaičiuojamas `hash(sender|receiver|amount)` ir sulyginamas su saugomu `txid`.
* **Balanso tikrinimas** – siuntėjo balansas tikrinamas kaupiamai vieno bloko ribose, kad neįvyktų „dvigubas išleidimas“.
* **Sanity check’ai** – neleidžiamos transakcijos su neigiamomis sumomis, siuntimas sau pačiam ar nežinomais raktais.

Failas `transactions.py` papildytas funkcija `verify_transactions()` (ankstesnis `mine_block()` naudoja tik patikrintas transakcijas).

<img width="1121" height="798" alt="image" src="https://github.com/user-attachments/assets/8c9f6107-0121-40ff-8225-b3abac70b318" />


---

### 3. **Patobulintas kasimo procesas**

Įgyvendintas decentralizuoto kasimo (Proof-of-Work) imitavimas:

#### 3.1. **Kandidatinių blokų generavimas**

* Iš viso sukuriama **5 kandidatinių blokų** po ~100 transakcijų.
* Kiekvienas blokas turi savo `Header` su Merkle Root ir `nonce = 0`.

#### 3.2. **Laiko ir bandymų limitas**

* Visi 5 kandidatai kasami **„round-robin“ principu**, paeiliui skiriant jiems po tam tikrą bandymų kiekį.
* Kasimo procesas trunka iki **5 sekundžių** (ar nurodyto hash bandymų skaičiaus).
* Jei nė vienas blokas neiškasamas, **laiko limitas padvigubinamas** (5s → 10s → 20s) ir ciklas kartojamas.

#### 3.3. **Sėkmės ir backoff mechanizmas**

* Radus pirmą bloką, jo `nonce` ir `block_hash` išsaugomi kaip naujas patvirtintas blokas.
* Jei per tris „backoff“ raundus nieko neiškasama, procesas sustoja.

#### 1 pvz. **Su "000" difficulty**
<img width="809" height="643" alt="image" src="https://github.com/user-attachments/assets/f7bbcb9d-a874-4543-9be4-308eff7726b3" />

#### 2 pvz. **Su "00000" difficulty (pavyko iškast)**
<img width="827" height="389" alt="image" src="https://github.com/user-attachments/assets/6f5e71fe-700a-4dfa-83f5-905f4fa3b270" />

#### 3 pvz. **Su "00000" difficulty (nepavyko iškast)**
<img width="681" height="361" alt="image" src="https://github.com/user-attachments/assets/09c429d3-7143-4684-be37-7fc5cbb326f4" />


---
## Naudojimas

### Išlieka toks pat (žr. v0.1)

---

## AI pagalbos taikymai

AI pagalba (naudota GPT-5) buvo pasitelkta šiais etapais:

* **Merkle Tree** funkcijos kūrimas ir integravimas į `Header`;
* **Kasimo proceso tobulinimas** – 5 kandidatinių blokų generavimas, round-robin ir backoff algoritmas;

---

