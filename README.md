# Forma-1 Adatelemző Program (NumPy)

Ez a projekt egy interaktív parancssori adatelemző alkalmazás, amely a Kaggle Formula-1 adathalmazát dolgozza fel. A program különlegessége, hogy a statisztikai és matematikai számításokhoz kizárólag a **NumPy** könyvtárat, az adatok beolvasásához pedig a Python beépített `csv` modulját használja (külső adatmanipulációs keretrendszerek, például Pandas nélkül).

---

## Szükséges fájlok és környezet

* **Python verzió:** Python 3.x
* **Külső függőség:** `numpy` (telepítése: `pip install numpy`)
* **Bemeneti adatfájlok** (a szkripttel azonos mappában kell elhelyezni őket):
  * `pit_stops.csv` – Bokszkiállások adatai
  * `lap_times.csv` – Köridők adatai
  * `results.csv` – Futamok végeredményei
  * `races.csv` – Futamok alapadatai
  * `qualifying.csv` – Időmérő edzések eredményei

---

## A program felépítése és működése

### 0. Adatbetöltés (`load_csv`)
A program elején egy saját segédfüggvény (`load_csv`) `csv.DictReader` segítségével beolvassa a szükséges CSV-fájlokat, és szótárak listájaként tárolja őket a memóriában. A hiányzó adatokat (`\N`) a program a szűrések során figyelmen kívül hagyja.

### 1. Feladat: Interaktív Pit Stop Outlier Szűrés
* **Cél:** A kiugróan lassú vagy gyors bokszkiállások (outlierek) kiszűrése a teljes adathalmazból.
* **Működés:** A program kiszámítja a kiállási idők mediánját (`np.median`) és szórását (`np.std`). A felhasználótól bekér egy szórás-szorzót (alapértelmezetten `2.5`), majd logikai indexeléssel meghatározza az alsó és felső határértékek közé eső kiállások számát.

### 2. Feladat: Interaktív Versenytempó Elemzés
* **Cél:** Egy adott versenyző teljesítményének és egyenletességének vizsgálata egy konkrét futamon.
* **Működés:** A felhasználó megadhatja a futam azonosítóját (`raceId`, alapértelmezett: `841`) és a pilóta azonosítóját (`driverId`, alapértelmezett: `20`). A program másodpercre váltja a köridőket, majd kiszámítja az átlagos köridőt (`np.mean`), a szórást (`np.std`) és a relatív szórást, azaz az ingadozási indexet ($CV = \frac{\sigma}{\mu}$).

### 3. Feladat: Futamgyőzelmek statisztikája
* **Cél:** A legtöbb futamgyőzelemmel rendelkező konstruktőr (csapat) azonosítása.
* **Működés:** A `results.csv` fájlból kigyűjti az 1. helyen végzett (`positionOrder == '1'`) konstruktőrök azonosítóit, majd az `np.unique(..., return_counts=True)` és az `np.argmax()` függvényekkel megkeresi a legsikeresebb csapatot és győzelmeinek számát.

### 4. Feladat: Rajthely és Célba érkezés eltérése
* **Cél:** A versenyzők futam alatti előrelépésének vagy visszaesésének vizsgálata az időmérős eredményükhöz képest.
* **Működés:** Összekapcsolja a `qualifying.csv` és a `results.csv` adatait `(raceId, driverId)` kulcsok alapján. Kiszámítja a rajt- és célpozíció különbségét, majd `np.mean`, `np.max` és `np.min` segítségével megadja az átlagos pozícióváltozást, valamint a legnagyobb előzést és visszaesést.

### 5. Feladat: Bokszkiállások eloszlása
* **Cél:** Annak vizsgálata, hogy milyen kiállási stratégiák (1, 2, 3 stb. kiállás) a leggyakoribbak a futamokon.
* **Működés:** Versenyzőnként és futamonként rögzíti a maximális kiállásszámot, majd az `np.bincount()` függvény segítségével gyors gyakorisági eloszlást készít.

---

## Futtatás

Nyisd meg a terminált abban a mappában, ahol a Python fájl és a CSV-k találhatók, majd futtasd a következő parancsot:

```bash
python proba.py
```

A program futás közben 3 interaktív bemenetet kér (szórás szorzója, futam ID, pilóta ID). Ha egyszerűen csak **Entert** nyomsz, a szkript az előre beállított alapértelmezett értékekkel számol tovább.