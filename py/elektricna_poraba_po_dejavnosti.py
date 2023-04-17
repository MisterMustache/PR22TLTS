import Orange
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np
import csv

with open('../podatki/csv/poraba_podejavnosti_breztransformacij.csv', encoding="cp1252") as f:
    reader = csv.reader(f)
    data = [row for row in reader]

new_data = []
for row in data:
    if str(row[0])[1] == " ":
        new_data.append(row)

data = new_data
values = []
names = []
for row in data:
    print(row)
    names.append(row[0])
    value = [int(n) if n.isdigit() else 0 for n in row[1:]]
    values.append(value)

# od 2008 do 2021
years = [year for year in range(2008, 2022, 1)]
colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta']

fig, ax = plt.subplots(figsize=(8, 8))
for i, value in enumerate(values):
    ax.plot(years, value, color=colors[i], label='{}'.format(names[i]))
plt.xlabel('Leto')
plt.ylabel('Poraba v TJ')
plt.title('Poraba')
ax.legend(loc='lower center', bbox_to_anchor=(0, -0.4, 1, 0.1))
plt.subplots_adjust(bottom=0.25)
plt.show()
