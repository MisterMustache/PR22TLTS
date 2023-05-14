import matplotlib.pyplot as plt
import numpy as np
import csv

# ---------- UVOZ PODATKOV ----------
with open('../podatki/csv/proizvodnja_elektrike_po_tipu_elektrarne.csv', encoding="cp1250") as f:
    reader = csv.reader(f)
    data = [row for row in reader]

# izberi prave aktualne vrstice
data = np.array(data[2:8])
data = np.delete(data, 1, axis=0)


# ---------- PREDPROCESIRANJE ----------
values = []

# pretvori v števila
for row in data:
    values.append([float(n) if n != '-' else 0 for n in row[2:]])


# ---------- IZPIS PDOATKOV ----------
years = [str(year) for year in range(2004, 2022)]
colors = ['red', 'green', 'blue', 'orange', 'cyan']
names = ['Hidroelektrarne', 'Termoelektrarne', 'Jedrska elektrarna', 'Sončne elektrarne', 'Vetrne elektrarne']

fig, ax = plt.subplots(figsize=(10, 5))
for i, value in enumerate(values):
    ax.plot(years, value, color=colors[i], label='{}'.format(names[i]))
plt.xlabel('Čas [leta]')
plt.ylabel('Proizvod [GWh]')
plt.title('Proizvodnja električne energije po tipu elektrarne v Sloveniji')
plt.legend(loc='lower left', bbox_to_anchor=(0, 0.1, 1, 0.1))
plt.show()
