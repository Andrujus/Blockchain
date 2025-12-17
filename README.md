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

## Verslo modelio srautų diagrama (Squence diagram)

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

## Paskirtis
Šis kontraktas skirtas:
- decentralizuotai nuomos depozito kontrolei
- skaidriam ir automatiškam lėšų paskirstymui
- paprastam integravimui į DApp ar Front-End sprendimus
