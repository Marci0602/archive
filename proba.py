import csv
import numpy as np

# ---------------------------------------------------------
# SEGÉDFÜGGVÉNY: CSV Fájlok beolvasása tiszta Pythonnal
# ---------------------------------------------------------
def load_csv(filename):
    data = []
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

print("=== F1 ADATELEMZŐ BEADANDÓ (CSAK NUMPY) ===")
print("Adatok betöltése folyamatban...")

pit_stops = load_csv('pit_stops.csv')
lap_times = load_csv('lap_times.csv')
results = load_csv('results.csv')
races = load_csv('races.csv')
qualifying = load_csv('qualifying.csv')

print("Adatok sikeresen betöltve!\n")

# ---------------------------------------------------------
# 1. FELADAT: Interaktív Pit Stop Outlier szűrés NumPy-val
# ---------------------------------------------------------
print("--- 1. Feladat: Pit Stop Outlier Szűrés ---")
pit_times = np.array([float(row['milliseconds']) for row in pit_stops if row['milliseconds'] != '\\N'])

median_val = np.median(pit_times)
std_val = np.std(pit_times)

# Felhasználói bemenet kérése a szórás szorzójához
user_mult = input("Add meg a szórás szorzóját az outlier szűréshez (alapértelmezett: 2.5): ")
mult = float(user_mult) if user_mult.strip() else 2.5

lower_bound = median_val - mult * std_val
upper_bound = median_val + mult * std_val

filtered_pit_times = pit_times[(pit_times >= lower_bound) & (pit_times <= upper_bound)]

print(f"-> Eredeti kiállások száma: {len(pit_times)}")
print(f"-> Szűrt kiállások száma (szorzó: {mult}): {len(filtered_pit_times)}")
print(f"-> Medián kiállási idő: {median_val / 1000:.2f} másodperc\n")

# ---------------------------------------------------------
# 2. FELADAT: Interaktív Versenytempó Elemzés NumPy-val
# ---------------------------------------------------------
print("--- 2. Feladat: Versenytempó Elemzés ---")
user_race_id = input("Add meg a futam ID-jét (pl. 841): ")
user_driver_id = input("Add meg a pilóta ID-jét (pl. 20 - Lewis Hamilton): ")

race_id = user_race_id.strip() if user_race_id.strip() else '841'
driver_id = user_driver_id.strip() if user_driver_id.strip() else '20'

lap_list = [
    float(row['milliseconds']) for row in lap_times 
    if row['raceId'] == race_id and row['driverId'] == driver_id
]

if lap_list:
    lap_times_np = np.array(lap_list) / 1000.0  # másodpercbe váltva
    mean_time = np.mean(lap_times_np)
    std_time = np.std(lap_times_np)
    cv_index = std_time / mean_time

    print(f"-> Eredmények a(z) {race_id}. futamhoz és {driver_id}. pilótához:")
    print(f"   Átlagos köridő: {mean_time:.3f} s")
    print(f"   Köridők szórása: {std_time:.3f} s")
    print(f"   Pilóta ingadozási indexe (CV): {cv_index:.4f}\n")
else:
    print("-> Nincs találat a megadott adatokkal.\n")

# ---------------------------------------------------------
# 3. FELADAT: Futamgyőzelmek statisztikája NumPy-val
# ---------------------------------------------------------
print("--- 3. Feladat: Győzelmek statisztikája ---")
win_constructor_ids = [int(row['constructorId']) for row in results if row['positionOrder'] == '1']
wins_np = np.array(win_constructor_ids)

unique_constructors, counts = np.unique(wins_np, return_counts=True)
top_winner_idx = np.argmax(counts)
best_constructor_id = unique_constructors[top_winner_idx]
max_wins = counts[top_winner_idx]

print(f"-> A legtöbb győzelmet elért konstruktőr ID-je: {best_constructor_id}")
print(f"-> Összes győzelmek száma: {max_wins}\n")

# ---------------------------------------------------------
# 4. FELADAT: Rajthely vs. Célba érkezés eltérése NumPy-val
# ---------------------------------------------------------
print("--- 4. Feladat: Rajthely és Célba érkezés eltérése ---")
quali_dict = { (row['raceId'], row['driverId']): int(row['position']) for row in qualifying if row['position'] != '\\N' }

grid_diffs = []
for row in results:
    key = (row['raceId'], row['driverId'])
    if key in quali_dict and row['positionOrder'] != '\\N':
        grid_pos = quali_dict[key]
        final_pos = int(row['positionOrder'])
        grid_diffs.append(grid_pos - final_pos)

diffs_np = np.array(grid_diffs)
print(f"-> Elemzett pozíció-változások száma: {len(diffs_np)}")
print(f"-> Átlagos pozícióváltozás (pozitív = javított): {np.mean(diffs_np):.2f} hely")
print(f"-> Legnagyobb előzés (pozíció javulás): {np.max(diffs_np)}")
print(f"-> Legnagyobb visszaesés: {np.min(diffs_np)}\n")

# ---------------------------------------------------------
# 5. FELADAT: Bokszkiállások eloszlása NumPy-val
# ---------------------------------------------------------
print("--- 5. Feladat: Bokszkiállások eloszlása ---")
stop_counts_map = {}
for row in pit_stops:
    stop_counts_map[(row['raceId'], row['driverId'])] = int(row['stop'])

stops_np = np.array(list(stop_counts_map.values()))
bins_count = np.bincount(stops_np)

print("Bokszkiállások eloszlása (hány kiállást választottak a versenyzők):")
for i, count in enumerate(bins_count):
    if count > 0:
        print(f"  - {i} kiállás: {count} alkalom")

print("\nA beadandó program sikeresen lefutott!")