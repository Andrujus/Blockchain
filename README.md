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


### Testavimas Su AI

# Eksperimentinis tyrimas – 1–3 punktai

## 1. Testiniai failai ir jų hash’ai

| Failo pavadinimas     | Turinys / aprašymas                 | Hash rezultatas (64 hex simboliai)                                   |
|-----------------------|-------------------------------------|----------------------------------------------------------------------|
| `a.txt`              | Vienas simbolis `a`                 | `db14591cbe4223503ff33ada24e9fdfb12bf9b0ca09bbb30e56273e2bda4c966` |
| `empty.txt`          | Tuščias failas                      | `9dcf25a293048b0d4ed06288470f77be3a742a91cb88491d045aaa8ba0dd1b60` |
| `test1000_1.txt`     | 1000+ atsitiktinių simbolių          | `63df1cc2c4ad81a6eb9504b38e2641f596393c71575bc78d91d0552ad363536d` |
| `test1000_2.txt`     | 1000+ atsitiktinių simbolių, skiriasi vienu simboliu nuo `test1000_1.txt` | `5a3b7793758e8adcdda504e75f421729304d6d46fd1f8728aaf41860f6409cd7` |

---

## 2. Rezultato dydis
- Visų failų hash’ai buvo **64 simbolių ilgio** (256 bitai).  
- Išvada: išvedimo dydis **nepriklauso nuo įvedimo** → ✅ atitinka reikalavimus.

---

## 3. Deterministiškumas
- Kiekvienas failas hash’uotas kelis kartus.  
- Rezultatai **nesikeitė** – tas pats failas visada duoda tą patį hash’ą.  
- Pvz.:
  - `a.txt` → visada `db14591c...`  
  - `empty.txt` → visada `9dcf25a2...`  

Išvada: algoritmas yra **deterministinis** → ✅ atitinka reikalavimus.

---

## Tarpinė išvada
- Pirmieji testai parodė, kad:
  - Hash’as duoda **pastovaus dydžio** išvedimą.
  - Tas pats įvedimas → visada tas pats hash’as.
  - Net vieno simbolio skirtumas (**`test1000_1.txt` vs `test1000_2.txt`**) lemia visiškai skirtingą rezultatą (lavinos efekto požymis).

Toliau galima atlikti **4 punktą – efektyvumo matavimus** su didesniais failais.

# Eksperimentinis tyrimas – 4 punktas

## 4. Efektyvumo matavimai

Naudotas failas: `konstitucija.txt`  
Kiekvienam įvedimo dydžiui hash funkcija buvo paleista **5 kartus**, skaičiuotas **vidutinis laikas (s)**.

### Rezultatai

| Eilučių skaičius | Vidutinis laikas (s) |
|------------------|-----------------------|
| 1                | 0.000285             |
| 2                | 0.000485             |
| 4                | 0.000794             |
| 8                | 0.001256             |
| 16               | 0.003446             |
| 32               | 0.005585             |
| 64               | 0.010981             |
| 128              | 0.026271             |
| 256              | 0.059209             |
| 512              | 0.134168             |

---

### Grafikas

<img width="1329" height="869" alt="image" src="https://github.com/user-attachments/assets/c680dea0-72ee-4eb7-89d9-be8d7b02ca4d" />


---

### Išvada
- Hashavimo laikas **nuosekliai auga** didėjant įvedimo eilučių skaičiui.  
- Net ir su mažu kiekiu eilučių matomas laipsniškas didėjimas.  
- Dvigubai padidinus įvestį, laikas išauga maždaug **2–3 kartus** (mažose imtyse kiek mažiau, didesnėse – daugiau).  
- Grafike aiškiai matoma, kad algoritmas veikia **artimai linijinei priklausomybei**, todėl yra **skaliojamas**.  
- Tai reiškia, kad didesniems failams laikas bus ilgesnis, bet prognozuojamas ir be „staigių šuolių“.


# 5. Kolizijų paieškos testas

### Užduotis
Sugeneruotos po **100 000 atsitiktinių string porų** keturiems skirtingiems ilgiams:  
- 10 simbolių  
- 100 simbolių  
- 500 simbolių  
- 1000 simbolių  

Kiekvienai porai buvo paskaičiuotas `hash_string` rezultatas ir patikrinta, ar nėra kolizijos (t. y. ar dvi skirtingos eilutės neduoda to paties hash’o).

---

### Rezultatai

| Eilučių ilgis | Patikrinta porų | Kolizijų skaičius | Kolizijų dažnis |
|---------------|-----------------|-------------------|-----------------|
| 10            | 100 000         | 0                 | 0.000000%       |
| 100           | 100 000         | 0                 | 0.000000%       |
| 500           | 100 000         | 0                 | 0.000000%       |
| 1000          | 100 000         | 0                 | 0.000000%       |

---

### Išvados
- Atlikus testą su **400 000 porų** skirtingo ilgio string’ų, nė karto nepasitaikė kolizijos.  
- Tai rodo, kad `hash_string` funkcija yra **pakankamai atspari kolizijoms** bent jau tokio dydžio duomenų aibėse.  
- Tikėtina, kad kolizijų atsiradimas pareikalaus ženkliai didesnio testų masto (pvz., milijonų ar daugiau porų).  

# Lavinos efektas (Avalanche Effect) – hash_su_ai

**Failas:** `avalanche_pairs/avalanche_len50_pairs100000.txt`  
**Porų skaičius:** 100 000 porų  
**Kiekvienos poros ilgis:** 50 simbolių (skiriasi tik vienu simboliu)

## Rezultatai

| Lygmuo       | Min  | Max  | Vidurkis |
|--------------|------|------|----------|
| **Bitai**    | 0    | 163  | 127.91   |
| **Hex simboliai** | 0    | 64   | 59.95    |

## Interpretacija

- **Bitų lygmuo:**  
  - `min = 0` – egzistuoja porų, kurių hash visiškai nesiskyrė.  
  - `max = 163` – daugiausiai skirtingų bitų poroje.  
  - `avg ≈ 128` – vidutiniškai apie pusė hash bitų pasikeitė, kas rodo gerą lavinos efektą.
 
- **Hex simbolių lygmuo:**  
  - `min = 0` – poros, kurių hex hash buvo identiški.  
  - `max = 64` – maksimaliai pasikeitė visi hex simboliai.  
  - `avg ≈ 60` – vidutiniškai pasikeitė dauguma simbolių.

## Išvada

Hash funkcija `hash_su_ai.py` turi **stiprų lavinos efektą**. Vieno simbolio pakeitimas įvestyje keičia vidutiniškai apie pusę bitų ir daugumą hex simbolių hash’e. Tai geras ženklas kriptografiniam saugumui – apsunkina prognozuoti hash reikšmes ir rasti kolizijas.



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
- 1 testas (vienas simbolis):
- Gaunamas hash'as - "cf133099bc86406de1479f0147b3325f7654150fedf79cb16091a2b3cdcbe743".
- 2 testas (1000 simbolių):
- Gaunamas hash'as - "29d2ee16281f00510dd83234ac2542ee9ddb1bd0c7d1dbac559178753b0afa06"
- 3 testas (1000 simbolių, bet vienas jų - skirtingas)
- Gaunamas hash'as - "29d2ee16281f005165620a405ea054cb6840d0869d8e4ca817104314dd881032"
Pradžia atrodo identiška, reikia tobulinimų.


# Eksperimentinis tyrimas – Hash_be_ai

## Efektyvumo matavimai

Naudotas failas: `konstitucija.txt`  
Kiekvienam įvedimo dydžiui hash funkcija buvo paleista **5 kartus**, skaičiuotas **vidutinis laikas (s)**.

### Rezultatai

| Eilučių skaičius | Vidutinis laikas (s) |
|------------------|-----------------------|
| 8                | 0.000270             |
| 16               | 0.000740             |
| 32               | 0.001906             |
| 64               | 0.003254             |
| 128              | 0.007656             |
| 256              | 0.016723             |
| 512              | 0.038718             |

---

### Grafikas

<img width="1052" height="817" alt="image" src="https://github.com/user-attachments/assets/0ca0fe94-a241-44b1-9051-790d23392824" />


---

### Išvada
- Hashavimo laikas **nuosekliai auga didėjant įvesties eilučių skaičiui**.  
- Algoritmas **žymiai greitesnis** nei ankstesnis `simplehash.py`.  
- Laikas didėja apytiksliai **linijiškai**: dvigubai daugiau eilučių → ~2–3 karto ilgesnis laikas.  
- Šis hash algoritmas yra **skaliojamas ir efektyvus** net didesniems failams, todėl tinkamas realiems testams.  

# Kolizijų paieškos rezultatai

## Testo eiga
Buvo sugeneruota ir patikrinta po **100 000 atsitiktinių string porų** keturiems skirtingiems ilgiams: **10, 100, 500, 1000 simbolių**.  
Kiekviename etape fiksuotas apdorotų porų skaičius bei rastos kolizijos.

### Detalūs rezultatai
- **pairs_len10.txt**  
  - Apdorota: 100 000 porų  
  - Kolizijų: 0  

- **pairs_len100.txt**  
  - Apdorota: 100 000 porų  
  - Kolizijų: 0  

- **pairs_len500.txt**  
  - Apdorota: 100 000 porų  
  - Kolizijų: 0  

- **pairs_len1000.txt**  
  - Apdorota: 100 000 porų  
  - Kolizijų: 0  

---

## Galutiniai rezultatai
| String ilgis | Porų skaičius | Kolizijų skaičius | Kolizijų dažnis |
|--------------|---------------|-------------------|-----------------|
| 10           | 100 000       | 0                 | 0.000000%       |
| 100          | 100 000       | 0                 | 0.000000%       |
| 500          | 100 000       | 0                 | 0.000000%       |
| 1000         | 100 000       | 0                 | 0.000000%       |

---

## Išvada
Visuose keturiuose testuose neaptikta nė vienos kolizijos.  
Tai atitinka teorinę tikimybę, kad 256 bitų hash erdvėje, naudojant vos 100 tūkst. bandymų, kolizijų tikimybė yra praktiškai lygi nuliui.

# Lavinos efektas (Avalanche Effect) – hash_be_ai

**Failas:** `avalanche_pairs/avalanche_len50_pairs100000.txt`  
**Porų skaičius:** 100 000 porų  
**Kiekvienos poros ilgis:** 50 simbolių (skiriasi tik vienu simboliu)

## Rezultatai

| Lygmuo           | Min  | Max  | Vidurkis |
|------------------|------|------|----------|
| **Bitai**        | 17   | 163  | 120.85   |
| **Hex simboliai** | 12   | 64   | 56.71    |

## Interpretacija

- **Bitų lygmuo:**  
  - `min = 17` – mažiausias bitų skirtumas poroje, nėra visiškai identiškų hash’ų.  
  - `max = 163` – daugiausiai skirtingų bitų poroje.  
  - `avg ≈ 121` – vidutiniškai apie pusė hash bitų pasikeitė, kas rodo gerą lavinos efektą.
 
- **Hex simbolių lygmuo:**  
  - `min = 12` – mažiausiai pasikeitusių hex simbolių poroje.  
  - `max = 64` – maksimaliai pasikeitė visi hex simboliai.  
  - `avg ≈ 57` – vidutiniškai pasikeitė dauguma simbolių.

## Išvada

Hash funkcija `hash_be_ai.py` turi **stiprų lavinos efektą**. Vieno simbolio pakeitimas įvestyje keičia vidutiniškai apie pusę bitų ir daugumą hex simbolių hash’e. Tai geras ženklas kriptografiniam saugumui – apsunkina prognozuoti hash reikšmes ir rasti kolizijas.

# Negrįžtamumo demonstracija hash_su_ai

| hash + SALT               |    laikas, s | Bandymų sk. |
|---------------------------|--------------|-------------|
| **Be SALT/su žinomu SALT**|    7.15      |   37288     |
| **Hex simboliai**         |    300.59    |   13800556  |

## Tyrimo sąlygos

#### Originalus pasirinktas tekstas: "101".
#### pasirinktas fiksuotas SALT'as: "ac".

SALT'as bei įvestis pasirinkti ypač paprasti siekiant parodyti, jog tyrimas veikia, pradinę būseną teoriškai įmanoma atspėti. Pasirinkus ilgesnį SALT ir ilgesnę įvestį pradinio teksto atspėti praktiškai neįmanoma.


# Negrįžtamumo demonstracija hash_be_ai

| hash + SALT               |    laikas, s | Bandymų sk. |
|---------------------------|--------------|-------------|
| **Be SALT/su žinomu SALT**|    0.24      |   37288     |
| **Su nežinomu SALT**      |    10.92     |   1380952   |

## Tyrimo sąlygos

#### Originalus pasirinktas tekstas: "101".
#### pasirinktas fiksuotas SALT'as: "ac".

SALT'as bei įvestis pasirinkti ypač paprasti siekiant parodyti, jog tyrimas veikia, pradinę būseną teoriškai įmanoma atspėti. Pasirinkus ilgesnį SALT ir ilgesnę įvestį pradinio teksto atspėti praktiškai neįmanoma. Versija, kurioje nenaudojami AI įrankiai matome, jog nors ir su nežinomu SALT'u pradinė reikšmė randama panašiu metu, nes ir ten ir ten visi simboliai buvo tikrinami iš eilės.

## IŠvados

Abi versijos yra vienodai vienodai atsparios tikrinimams, negrįžtamumas aiškiai parodytas. Pasirinkus ilgesnią/ sunkesnią SALT reikšmę rezultatai keistųsi eksponentiškai, pradinės reikšmės atstatyti būtų praktiškai neįmanoma.

# Hash algoritmų tyrimo išvados

Šiame projekte pateikiami du hash algoritmų variantai:

- `hash_su_ai` – sukurtas naudojant AI pagalbą
- `hash_be_ai` – sukurtas be AI pagalbos, pasinaudota pagalba iš Igno (AI pagalbą naudojančio asmens)

Tyrimo tikslas – patikrinti, ar šie algoritmai atitinka pagrindinius hash funkcijų reikalavimus: pastovaus dydžio rezultatas, deterministiškumas, lavinos efektas, atsparumas kolizijoms, efektyvumas ir negrįžtamumas.

---

## Pagrindinės savybės

- Rezultatas: visada 64 simbolių (256 bitų) hex eilutė
- Deterministiškumas: tas pats įvedimas visada duoda tą patį hash
- Lavinos efektas: vieno simbolio pakeitimas įvestyje pakeičia apie pusę hash bitų
- Kolizijos: atlikus 400 000 testų porų, kolizijų neaptikta
- Efektyvumas: hashavimo laikas auga artimai linijinei priklausomybei didėjant duomenų kiekiui
- Negrįžtamumas: hash reikšmės atstatyti praktiškai neįmanoma

---

## Eksperimentiniai rezultatai

### Rezultato dydis
- Abiejų algoritmų hash ilgis visada 64 simboliai.

### Deterministiškumas
- Tas pats failas visada grąžina tą patį hash.

### Lavinos efektas

| Algoritmas   | Vidutinis skirtingų bitų skaičius | Vidutinis skirtingų hex simbolių skaičius |
|--------------|-----------------------------------|-------------------------------------------|
| hash_su_ai   | ~128 iš 256                       | ~60 iš 64                                  |
| hash_be_ai   | ~121 iš 256                       | ~57 iš 64                                  |

### Kolizijos
- Patikrinta 400 000 skirtingų string porų
- Kolizijų neaptikta

### Efektyvumas
- Hashavimo laikas abiejuose algoritmuose auga beveik linijiškai
- `hash_be_ai` yra šiek tiek greitesnis

### Negrįžtamumas
- Net ir su paprastu SALT atstatymas užtrunka labai ilgai
- Su sudėtingesniu SALT pradinę reikšmę atspėti tampa praktiškai neįmanoma

---

## Galutinės išvados

Abu algoritmai atitinka pagrindinius hash funkcijų kriterijus. Abiejuose hash'ų generatoriuose būtų vertinga iškart naudoti SALT reikšmes, hash_be_ai versijoje trūksta pilnos bit'ų rotacijos, didesnių maišymų, geresnio lavinos efekto realizavimo (vienu simboliu besikeičiančios reikšmės palieka labai panašią pirmųjų ~29 simbolių reikšmę 64-ių simbolių rezultate).


# Hash algoritmų palyginimas

| Testas | hash_su_ai | hash_be_ai | sha256 |
|--------|------------|-------------|--------|
| **1. Testiniai failai** | a.txt, empty.txt, 1000+ simbolių failai, skirtingi vienu simboliu – rezultatai gauti | a.txt, empty.txt, 1000+ simbolių failai, skirtingi vienu simboliu – rezultatai gauti | failai, skirtingi vienu simboliu – rezultatai gauti |
| **2. Rezultato dydis** | 64 hex simboliai (256 bitai) | 64 hex simboliai (256 bitai) | 64 hex simboliai (256 bitai) |
| **3. Deterministiškumas** | Tas pats failas → tas pats hash | Tas pats failas → tas pats hash | Tas pats failas → tas pats hash |
| **4. Efektyvumas (konstitucija.txt)** | Laikas ~ linijinis, pvz. 512 eilučių → ~0.134 s | Laikas ~ linijinis, pvz. 512 eilučių → ~0.039 s | Laikas ~ linijinis, pvz. 512 eilučių → ~0.000021 s |
| **5. Kolizijų paieška (100k porų)** | 0 kolizijų (10, 100, 500, 1000 simbolių) | 0 kolizijų (10, 100, 500, 1000 simbolių) | 0 kolizijų (10, 100, 500, 1000 simbolių) |
| **6. Lavinos efektas** | Bitai: min=0, max=163, avg≈128  Hex: min=0, max=64, avg≈60 | Bitai: min=17, max=163, avg≈121  Hex: min=12, max=64, avg≈57 | Bits -> min: 95, max: 159, avg: 127.98 Hex  -> min: 50, max: 64, avg: 60.00 |
| **7. Negrįžtamumas (HASH + SALT)** | Bandant atspėti su žinomu SALT → 7.15s, su nežinomu → 300s+ | Bandant atspėti su žinomu SALT → 0.24s, su nežinomu → 10.9s | Bandant atspėti su žinomu SALT → 0.05s, su nežinomu → 2.03s |

