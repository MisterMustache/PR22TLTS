import matplotlib.pyplot as plt
import numpy as np
import csv


# ---------- UVOZ PODATKOV ----------
with open('../podatki/csv/poraba_skupaj_brez-transformacij.csv', encoding="cp1252") as f:
    reader = csv.reader(f)
    data = [row for row in reader]

podatki_porabe = data[1:]

with open('../podatki/csv/cena_elektrike.csv', encoding="cp1252") as f:
    reader = csv.reader(f)
    podatki_cene = [row for row in reader]


# ---------- PREDPROCESIRANJE PODATKOV ----------
poraba_skupaj = []
for row in podatki_porabe:
    # deli se z 3.6, ker je to faktor pretvorbe iz TJ v GWh
    value = [float(n) / 3.6 if n.isdigit() else 0 for n in row[1:]]
    poraba_skupaj.append(value)

household = [float(x) for x in podatki_cene[1][1:]]
non_household = [float(x) for x in podatki_cene[7][1:]]
cene_skupaj = np.concatenate((household, non_household))


# --------- IZPIS PODATKOV ----------
plt.hist(household, density=False, bins=25)
plt.title('Distribucija cen gospodinjskih odjemalcev')
plt.xlabel('Cena [EUR]')
plt.ylabel('Število pojavitev')
plt.show()

plt.hist(non_household, density=False, bins=25)
plt.title('Distribucija cen negospodinjskih odjemalcev')
plt.xlabel('Cena [EUR]')
plt.ylabel('Število pojavitev')
plt.show()

plt.hist(cene_skupaj, density=False, bins=25)
plt.title('Distribucija cen vseh odjemalcev')
plt.xlabel('Cena [EUR]')
plt.ylabel('Število pojavitev')
plt.show()

plt.hist(poraba_skupaj, density=False, bins=7)
plt.title('Distribucija porab')
plt.xlabel('Poraba [GWh]')
plt.ylabel('Število pojavitev')
plt.show()
