#  Nuomos Užtikrinimo Sistema (Smart Contract)

Šis projektas įgyvendina blockchain pagrįstą **nuomos saugumo modelį**, kuriame dalyvauja **trys šalys**:

- **Nuomininkas (Renter)** — rezervuoja objektą ir sumoka depozitą.
- **Nuomotojas (Owner)** — patvirtina rezervaciją ir gauna mokėjimą po patikrinimo.
- **Prižiūrėtojas/Brokeris (Inspector/Broker)** — nepriklausomas trečias asmuo, kuris patvirtina objekto būklę prieš išmokant lėšas.

Sistema užtikrina, kad **depozitas būtų laikomas saugiai kontrakte**, kol procesas pilnai užbaigtas.

---

##  Pagrindinė idėja

1. **Nuomininkas** rezervuoja objektą ir į kontraktą sumoka depozitą.
2. **Nuomotojas** patvirtina, kad nuoma galioja.
3. **Prižiūrėtojas** po nuomos laikotarpio atlieka patikrą.

### Remiantis patikros rezultatu:

-  **Jei objektas tvarkingas** → depozitas atitenka Nuomotojui
-  **Jei yra pažeidimų arba ginčas** → depozitas grąžinamas Nuomininkui

Sistema sukurta taip, kad **nė viena šalis negalėtų pavogti ar pasisavinti lėšų** — kontraktas yra tarpininkas, valdantis procesą pagal aiškias, nekintamas taisykles.

---

##  Kontrakto struktūra

### Dalyviai:

- **renter** — rezervavęs nuomininkas
- **owner** — objekto savininkas
- **inspector** — patikrą atliekanti šalis

### Kontrakto būsenos:

- `PENDING` — Laukiama Nuomotojo patvirtinimo
- `APPROVED` — Nuomotojas patvirtino, laukiama Prižiūrėtojo patikros
- `INSPECTED` — Prižiūrėtojas atliko patikrą
- `RELEASED` — Pinigai išmokėti, sandoris baigtas
- `CANCELLED` — Sandoris atšauktas, depozitas grąžintas

### Pagrindinės funkcijos:

#### `rentProperty(address _owner, address _inspector) payable`

- Nuomininkas rezervuoja objektą ir sumoka depozitą
- Reikalingas: `msg.value > 0`

#### `confirmRental()`

- Nuomotojas patvirtina nuomos sandorį
- Keičia būseną į `APPROVED`

#### `inspectProperty(bool _isGood)`

- Prižiūrėtojas patvirtina objekto būklę
- `_isGood = true` → depozitas atitenka Nuomotojui
- `_isGood = false` → depozitas grąžinamas Nuomininkui

#### `cancelRental()`

- Nuomininkas gali atšaukti sandorį (tik `PENDING` būsenoje)
- Depozitas grąžinamas Nuomininkui

#### `releaseDeposit()`

- Nuomotojo saugumo funkcija — išmoka depozitą po Prižiūrėtojo patvirtinimo

---

##  Tipiniai scenarijai

 **Saugumo užtikrinimas** — Trečias nepriklausomas asmuo (Inspector) užtikrina šalių sąžiningumą  
 **Nepildomos pervedimų** — Pinigai išmokami tik atlikus nustatytus žingsnius  
 **Ginčo sprendimas** — Jei objektas pažeistas, depozitas grąžinamas Nuomininkui  

---
## Verslo modelio srautų diagrama (Squence diagram)

<img width="602" height="592" alt="Blockchain drawio" src="https://github.com/user-attachments/assets/83fac583-58b4-480a-a037-731b8598fbee" />
