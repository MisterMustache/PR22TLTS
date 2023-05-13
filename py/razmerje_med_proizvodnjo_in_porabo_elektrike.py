import matplotlib.pyplot as plt
import numpy as np
import csv

# ---------- UVOZ PODATKOV ----------
with open('../podatki/csv/poraba_skupaj_brez-transformacij.csv', encoding="cp1252") as f:
    reader = csv.reader(f)
    podatkiPorabe = [row for row in reader]

with open('../podatki/csv/proizvodnja_elektrike_po_tipu_elektrarne.csv', encoding="cp1250") as f:
    reader = csv.reader(f)
    podatkiProizvodov = [row for row in reader]


# ---------- PORABA ----------
data = podatkiPorabe[1:]

porabe_skupaj = []
names = []
for row in data:
    names.append(row[0])
    # deli se z 3.6, ker je to faktor pretvorbe iz TJ v GWh
    value = [int(n) / 3.6 if n.isdigit() else 0 for n in row[1:]]
    porabe_skupaj.append(value)
porabe_skupaj = porabe_skupaj[0]


# ---------- PROIZVODNJA ----------
# izberi taprave aktualne vrstice
data = np.array(podatkiProizvodov[2:8])
data = np.delete(data, 1, axis=0)

proizvodi_po_tipu_elektrarn = []

# pretvori v števila
for row in data:
    proizvodi_po_tipu_elektrarn.append([float(n) if n != '-' else 0 for n in row[2:]][4:])

# seštej proizvode različnih tipov elektrarn (sešteje stolpce) in
# odstrani prve 4 zapise (podatki porabe se začnejo leta 2008, proizvodov pa 2004)
proizvodi_skupaj = np.sum(proizvodi_po_tipu_elektrarn, axis=0)


# ---------- RAZMERJA ----------
# če je razmerje večje od 1, potem je viška elektrike, sicer jo je bilo potrebno uvažati
razmerja_skupno = np.divide(proizvodi_skupaj, porabe_skupaj)

razmerja_po_tipu_elektrarn = []
for proizvodi_tipa_elektrarne in proizvodi_po_tipu_elektrarn:
    razmerja_po_tipu_elektrarn.append(np.divide(proizvodi_tipa_elektrarne, porabe_skupaj))


# ---------- IZPIS PODATKOV ----------

names = ['Hidroelektrarne', 'Termoelektrarne', 'Jedrska elektrarna', 'Sončne elektrarne', 'Vetrne elektrarne']
colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta']
leta = [leto for leto in range(2008, 2022, 1)]

# prikaz razmerja skupne proizvodnje in skupne porabe
plt.plot(leta, razmerja_skupno, color=colors[0])
plt.xlabel('Čas [leta]')
plt.ylabel('Razmerje [proizvod/poraba]')
plt.title('Razmerje med skupno proizvodnjo in porabo elektrike v Sloveniji')
plt.show()

# prikaz razmerja proizvodnje po tipu elektrarne in skupne porabe
plt.axhline(y=1, color='black', linestyle='--')
for i, value in enumerate(razmerja_po_tipu_elektrarn):
    plt.plot(leta, value, color=colors[i], label='{}'.format(names[i]))
plt.xlabel('Čas [leta]')
plt.ylabel('Razmerje [proizvod/poraba]')
plt.title('Razmerje med proizvodnjo po tipu elektrarne in porabo elektrike v Sloveniji')
plt.legend(loc='lower left', bbox_to_anchor=(0, 0.1, 1, 0.1))
plt.show()
