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