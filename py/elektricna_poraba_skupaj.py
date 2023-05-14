import Orange
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np
import csv


# ---------- UVOZ PODATKOV ----------
with open('../podatki/csv/poraba_skupaj_brez-transformacij.csv', encoding="cp1252") as f:
    reader = csv.reader(f)
    data = [row for row in reader]

data = data[1:]


# ---------- PREDPROCESIRANJE PODATKOV ----------
values = []
for row in data:
    # deli se z 3.6, ker je to faktor pretvorbe iz TJ v GWh
    value = [int(n) / 3.6 if n.isdigit() else 0 for n in row[1:]]
    values.append(value)

povprecje_porabe = np.mean(values)
values.append([povprecje_porabe for _ in range(len(values[0]))])

# zamenjaj ju, da povprečna črta ne pokriva črte porabe
values[0], values[1] = values[1], values[0]


# ---------- IZPIS PODATKOV ----------
# od 2008 do 2021
years = [year for year in range(2008, 2022, 1)]
names = ['Povprečna poraba', 'Skupna poraba']
colors = ['lightgrey', 'darkblue']

for i, value in enumerate(values):
    plt.plot(years, value, color=colors[i], label=f"{names[i]}")
plt.xlabel('Čas [leto]')
plt.ylabel('Poraba [GWh]')
plt.title('Skupna poraba elektrike v Sloveniji')
plt.subplots_adjust(bottom=0.25)
plt.legend(loc='lower right')
plt.show()
