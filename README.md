# Prekės rezervavimo išmanioji sutartis

## 1. Verslo modelio aprašymas

Ši išmanioji sutartis realizuoja **paprastą prekės rezervavimo** modelį tarp dviejų šalių:

- **Pirkėjas (Buyer)** – nori rezervuoti prekę ir sumoka užstatą (ETH).
- **Pardavėjas (Seller)** – sutinka rezervuoti prekę Pirkėjui ir patvirtina rezervaciją.

Kontraktas veikia kaip tarpininkas / saugus „užstato laikytojas“ (escrow):

1. Pirkėjas rezervuoja prekę ir į kontraktą įneša ETH.
2. Pardavėjas patvirtina rezervaciją.
3. Pirkėjas priima galutinį sprendimą:
   - patvirtina pirkimą → pinigai išmokami Pardavėjui;
   - atšaukia rezervaciją → pinigai grąžinami Pirkėjui.

Taip užtikrinama, kad:
- Pardavėjas negauna pinigų, kol Pirkėjas nepatvirtina.
- Pirkėjas negali vienašališkai atsiimti pinigų po to, kai prekė rezervuota ir sandoris užbaigtas.

---

## 2. Pagrindiniai veikėjai (roles)

- **Buyer (Pirkėjas)**  
  - Kvies `reserveItem` – sukuria rezervaciją ir įneša ETH.  
  - Kvies `approve` – patvirtina pirkimą ir leidžia pervesti ETH Pardavėjui.  
  - Kvies `cancel` – atšaukia rezervaciją (kol sandoris neužbaigtas) ir atgauna ETH.

- **Seller (Pardavėjas)**  
  - Nurodomas rezervuojant prekę (kaip adresas).  
  - Kvies `confirm` – patvirtina, kad sutinka su rezervacija.  
  - Gavęs patvirtinimą (`approve`), gauna ETH.

- **Smart Contract (kontraktas)**  
  - Laiko užstatą (ETH) iki galutinio sprendimo.  
  - Tikrina kas kviečia funkcijas (Pirkėjas ar Pardavėjas).  
  - Valdo rezervacijos būseną (`Status`) ir atlieka pinigų pervedimus.

---