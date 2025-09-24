# hash_su_ai

## Pagrindinė logika

1. Inicializuoti pradinę būseną (8 skaičiai po 32 bitus)
2. Papildyti duomenis (padding), kad ilgis būtų tinkamas
3. Apdoroti kiekvieną 4 baitų žodį:
   - XOR su būsena
   - Maišyti kelis kartus (`mix_once`)
4. Finalizacija:
   - XOR su pradiniu duomenų ilgiu
   - Maišyti kelis kartus (final rounds)
5. Grąžinti rezultatą kaip 64 simbolių hex eilutę

---

## Pagalbinės funkcijos

- `rotl32(x, r)` – pasuka 32 bitų skaičiaus bitus į kairę
- `u32_le(b, i)` – paima 4 baitus iš duomenų ir paverčia į skaičių (little-endian formatu)
- `pad(data)` – prideda `0x80`, nuliais užpildo iki 4 baitų, gale prideda duomenų ilgį
- `mix_once(state)` – maišo 8 skaičius būsenoje naudojant bitų posūkius, XOR ir konstantas

---

## Naudojimas

- Jei paleidžiama su failo keliu → perskaito failą ir grąžina jo hash
- Jei paleidžiama be argumento → paprašo vartotojo įvesti tekstą ir grąžina jo hash


------------------------------------------------------------------------------------------------

# hash_be_ai

# Pagrindinė logika

1. Inicializuoti pradinę būseną (4 skaičiai po 64 bitus: h1, h2, h3, h4)
2. Konvertuoti įvestį (tekstą ar failo turinį) į baitus (UTF-8)
3. Apdoroti kiekvieną baitą:
- h1 maišomas su baitu per XOR, rotaciją, daugybą ir shift’us
- h2 maišomas su rotuotu baitu ir konstantom
- h3 maišomas kitu rotuotu baitu ir konstantom
- h4 maišomas dar kitu rotuotu baitu ir konstantom
- visi veiksmai ribojami 64 bitais
4. Finalizacija:
- Kiekvienas h1, h2, h3, h4 pavirsta į 16 simbolių hex
- Visi sujungiami į vieną 64 simbolių eilutę
5. Grąžinti rezultatą kaip 64 simbolių eilutę

# Pagalbinės funkcijos
- rotl64(x, r) – pasuka 64 bitų skaičių
- hash_string(data) – gauna tekstą, paverčia į baitus ir prasuką per pagrindinį maišymą
- hash_file(file) – perskaito failo turinį ir iškviečia hash_string

# Naudojimas

- Jei vartotojas pasirenka failą → paprašo failo pavadinimo, perskaito ir hash’ina jo turinį
- Jei vartotojas pasirenka string → paprašo teksto ir hash’ina jį
- Jei įvestis bloga → parodo klaidos žinutę ir baigia darbą

### Testavimas Be AI
1 testas (vienas simbolis):
- Gaunamas hash'as - "cf133099bc86406de1479f0147b3325f7654150fedf79cb16091a2b3cdcbe743".
2 testas (1000 simbolių):
- Gaunamas hash'as - "29d2ee16281f00510dd83234ac2542ee9ddb1bd0c7d1dbac559178753b0afa06"
3 testas (1000 simbolių, bet vienas jų - skirtingas)
- Gaunamas hash'as - "29d2ee16281f005165620a405ea054cb6840d0869d8e4ca817104314dd881032"
Pradžia atrodo identiška, reikia tobulinimų.