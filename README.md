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

## Verslo modelio srautų diagrama (Sequence diagram)

<img width="602" height="592" alt="Blockchain drawio" src="https://github.com/user-attachments/assets/83fac583-58b4-480a-a037-731b8598fbee" />

# RentalEscrow – Veikimo Principas

## Apžvalga
`RentalEscrow` – tai išmanusis kontraktas, skirtas nuomos depozito laikymui (escrow) tarp trijų šalių:
- **Renter** – nuomininkas (įneša depozitą)
- **Owner** – nuomotojas (patvirtina nuomą)
- **Inspector** – nepriklausomas patikrintojas (priima sprendimą)

Kontraktas laiko depozitą iki patikros pabaigos ir automatiškai jį išmoka teisingai pusei.

---

## Būsenų eiga (State Machine)

1. **PENDING** – renter sukuria užsakymą ir įneša depozitą  
2. **APPROVED** – owner patvirtina nuomą  
3. **INSPECTED** – inspector atlieka patikrą (passed / failed)  
4. **RELEASED** – depozitas išmokėtas owner arba renter  
5. **CANCELLED** – renter atšaukia kol dar PENDING (depozitas grąžinamas)

---

## Pagrindinės funkcijos

### `rentProperty(owner, inspector)`
- Kviečia **renter**
- Sukuria užsakymą ir įneša ETH depozitą
- Būsena → `PENDING`

### `confirmRental(orderId)`
- Kviečia **owner**
- Patvirtina nuomą
- Būsena → `APPROVED`

### `cancelRental(orderId)`
- Kviečia **renter**
- Galima tik `PENDING` būsenoje
- Depozitas grąžinamas renter
- Būsena → `CANCELLED`

### `inspectProperty(orderId, passed)`
- Kviečia **inspector**
- Atlieka patikrą
- Būsena → `INSPECTED`

### `releaseDeposit(orderId)`
- Gali kviesti bet kas
- Jei `passed == true` → depozitas owner
- Jei `passed == false` → depozitas renter
- Būsena → `RELEASED`

---

## Saugumas
- Naudojamas `nonReentrant` apsaugai nuo reentrancy atakų
- Griežti role-based modifieriai (`onlyRenter`, `onlyOwner`, `onlyInspector`)
- ETH pervedimai vykdomi tik po būsenos atnaujinimo

---

# RentalEscrow – Lokalaus Tinklo Testavimas (Ganache + Truffle)

Šiame dokumente aprašomas **`RentalEscrow` išmaniosios sutarties testavimas lokaliame Ethereum tinkle**, naudojant **Ganache** ir **Truffle Console**.  
Testavimo tikslas – įrodyti, kad **depozitas (ETH) teisingai pervedamas** pagal verslo logiką.

---

## 1. Testavimo aplinka

- Lokalūs Ethereum mazgai: **Ganache**
- Smart contract valdymas: **Truffle**
- Tinklas: `development`
- Kontraktas: `RentalEscrow`

**Naudojami accountai:**
- `accounts[0]` – Renter (nuomininkas)
- `accounts[1]` – Owner (nuomotojas)
- `accounts[2]` – Inspector (inspektorius)
- `accounts[3]` – Trečiasis asmuo (kviečia `releaseDeposit`)
---

## 2. Pradiniai balansai (prieš testą)

Per Truffle console patikrinami balansai:

- Renter: ~99.99 ETH  
- Owner: 100 ETH  
- Inspector: 100 ETH  

Tai rodo, kad **dar prieš testą jokie pervedimai nebuvo įvykę**.
<img width="1368" height="239" alt="image" src="https://github.com/user-attachments/assets/c6a64e94-240a-4676-8a1c-8e6e991768c5" />

---

## 3. Užsakymo (Order) sukūrimas

Renter sukuria nuomos užsakymą ir įneša **1 ETH depozitą**:

- Kvietimas: `rentProperty(owner, inspector)`
- Būsena: `PENDING`
- Sugeneruojamas `orderId = 1`

<img width="1694" height="122" alt="image" src="https://github.com/user-attachments/assets/31b3d696-9751-4105-a2d5-db066ae342e6" />


---

## 4. Nuomos patvirtinimas (Owner)

Owner patvirtina nuomos užsakymą:

- Kvietimas: `confirmRental(1)`
- Būsena pasikeičia į: `APPROVED`

<img width="2331" height="1110" alt="image" src="https://github.com/user-attachments/assets/357e0330-911f-408c-8f31-944dcea286c4" />


---

## 5. Turto patikra (Inspector)

Inspector atlieka patikrą:

- Kvietimas: `inspectProperty(1, true)`
- `inspectionPassed = true`
- Būsena pasikeičia į: `INSPECTED`

<img width="1960" height="1124" alt="image" src="https://github.com/user-attachments/assets/191684b9-abb3-4a06-b49e-e7054b15b86c" />

---

## 6. Depozito išmokėjimas

Trečiasis asmuo iškviečia depozito išmokėjimą:

- Kvietimas: `releaseDeposit(1)`
- Kadangi `inspectionPassed = true`, **1 ETH pervedamas Owner**
- Būsena pasikeičia į: `RELEASED`

<img width="1636" height="869" alt="image" src="https://github.com/user-attachments/assets/8f97adb1-cf40-4224-8173-6568a3f841bb" />


---

## 7. Užsakymo galutinė būsena

Užsakymo duomenys po testavimo:

- `status = RELEASED`
- `depositWei = 0`
- `inspectionPassed = true`
- Užfiksuoti visi laiko žymėjimai (`createdAt`, `approvedAt`, `inspectedAt`, `closedAt`)

<img width="632" height="131" alt="image" src="https://github.com/user-attachments/assets/2058de98-aeb0-4cb0-a125-c54c690c098f" />
<img width="403" height="338" alt="image" src="https://github.com/user-attachments/assets/1cf35ca9-6ef7-44ae-971f-88f5c4279d74" />



---

## 8. Balansai po testavimo (rezultatas)

Po depozito išmokėjimo:

- **Renter**: balansas sumažėjo ~1 ETH + gas
- **Owner**: balansas padidėjo ~1 ETH (minus minimalus gas)
- **Inspector**: balansas beveik nepakitęs (tik gas)

<img width="875" height="163" alt="image" src="https://github.com/user-attachments/assets/c8a692cb-6569-419c-a49a-844fdaf5c34c" />


Tai patvirtina, kad **depozitas buvo pervestas teisingai pagal verslo logiką**.

---
<img width="2878" height="1793" alt="kontrak1" src="https://github.com/user-attachments/assets/718e3de6-cc66-4f27-a6ac-e1036b2de20d" />

<img width="2808" height="1095" alt="kontrakt2" src="https://github.com/user-attachments/assets/1d66cfa1-f297-4882-a8d3-0fc84ed01272" />


