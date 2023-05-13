import Orange
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np
import csv

with open('../podatki/csv/poraba_skupaj_brez-transformacij.csv', encoding="cp1252") as f:
    reader = csv.reader(f)
    data = [row for row in reader]

data = data[1:]

values = []
names = []
for row in data:
    names.append(row[0])
    # deli se z 3.6, ker je to faktor pretvorbe iz TJ v GWh
    value = [int(n) / 3.6 if n.isdigit() else 0 for n in row[1:]]
    values.append(value)

# od 2008 do 2021
years = [year for year in range(2008, 2022, 1)]
colors = ['blue']

fig, ax = plt.subplots(figsize=(8, 5))
for i, value in enumerate(values):
    ax.plot(years, value, color=colors[i])
plt.xlabel('Leto')
plt.ylabel('Poraba [GWh]')
plt.title('Skupna poraba elektrike v Sloveniji')
plt.subplots_adjust(bottom=0.25)
plt.show()
