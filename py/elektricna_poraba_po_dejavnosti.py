import matplotlib.pyplot as plt
import numpy as np
import csv


def getdigit(n):
    if n.isdigit():
        return n
    # nekateri vnosi imajo na koncu to črko, ostali pa ne
    elif n[-1] == 'M':
        return int(n[:-1])
    return 0


# ---------- UVOZ PODATKOV ----------
with open('../podatki/csv/poraba_podejavnosti_breztransformacij.csv', encoding="cp1252") as f:
    reader = csv.reader(f)
    podatki = [row for row in reader]

novi_podatki = []
for row in podatki:
    if str(row[0])[1] == " ":
        novi_podatki.append(row)


# ---------- PREDPROCESIRANJE PODATKOV ----------
# tukaj se zgodi pretvorba različnih enot v eno samo [GWh], ki je skladna drugje
# nekatere vrednost imajo na koncu črko 'M', kar onemogoči direktno pretvorbo v število
# nekatere celotne dejavnosti pa vsebujejo preveč manjkajočih vrednosti, da bi bile uporabne
podatki = novi_podatki
porabe_po_dejavnosti = []
names = []
for row in podatki:
    if row[0][0] in ['A', 'D', 'E']:
        continue
    names.append(row[0])
    # deli se z 3.6, ker je to faktor pretvorbe iz TJ v GWh
    value = [int(getdigit(n)) / 3.6 for n in row[1:]]
    porabe_po_dejavnosti.append(value)


# ---------- TRANSFORMACIJA PODATKOV ----------
relativne_porabe_po_dejavnosti = []
for tabela_porab in porabe_po_dejavnosti:
    povp_poraba = np.mean(tabela_porab)
    relativne_porabe_po_dejavnosti.append([poraba / povp_poraba for poraba in tabela_porab])


# ---------- IZPIS PODATKOV ----------
# od 2008 do 2021
years = [year for year in range(2008, 2022, 1)]
colors = ['blue', 'red', 'green']

plt.axhline(y=1, color='grey', linestyle='--')
for i, value in enumerate(relativne_porabe_po_dejavnosti):
    plt.plot(years, value, color=colors[i], label='{}'.format(names[i]))
plt.xlabel('Čas [leto]')
plt.ylabel('Relativna sprememba od povprečne porabe')
plt.title('Električna poraba po dejavnosti v Sloveniji')
plt.legend(loc='upper left')
plt.show()
