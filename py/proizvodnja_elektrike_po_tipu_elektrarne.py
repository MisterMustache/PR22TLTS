import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
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
proizvodi_po_tipu = [[float(n) if n != '-' else 0 for n in row[2:]] for row in data]
skupni_proizvod_po_letih = np.sum(proizvodi_po_tipu, axis=0)

relativni_proizvodi = []
for i, proizvodi in enumerate(proizvodi_po_tipu):
    relativni_proizvodi.append([gwh / skupni_proizvod_po_letih[i] for gwh in proizvodi])

# normaliziraj
normalize = [2 - n for n in np.sum(relativni_proizvodi, axis=0)]
for i, proizvodi in enumerate(relativni_proizvodi):
    relativni_proizvodi[i] = np.multiply(relativni_proizvodi[i], normalize)


# ---------- IZPIS PDOATKOV ----------
years = [str(year) for year in range(2004, 2022)]
colors = ['red', 'green', 'blue', 'orange', 'cyan']
names = ['Hidroelektrarne', 'Termoelektrarne', 'Jedrska elektrarna', 'Sončne elektrarne', 'Vetrne elektrarne']

# prikaz absolutnih podatkov
_, ax = plt.subplots(figsize=(10, 5))
for i, value in enumerate(proizvodi_po_tipu):
    ax.plot(years, value, color=colors[i], label='{}'.format(names[i]))
plt.xlabel('Čas [leta]')
plt.ylabel('Proizvod [GWh]')
plt.title('Proizvodnja električne energije po tipu elektrarne v Sloveniji')
plt.legend(loc='lower left', bbox_to_anchor=(0, 0.1, 1, 0.1))
plt.show()

# prikaz relativnih podatkov
_, ax = plt.subplots(figsize=(10, 5))
for i, value in enumerate(relativni_proizvodi):
    ax.plot(years, value, color=colors[i], label='{}'.format(names[i]))
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1, decimals=0))
plt.xlabel('Čas [leta]')
plt.ylabel('Relativno na celotnem proizvod')
plt.title('Proizvodnja električne energije po tipu elektrarne v Sloveniji')
plt.legend(loc='lower left', bbox_to_anchor=(0, 0.1, 1, 0.1))
plt.show()
