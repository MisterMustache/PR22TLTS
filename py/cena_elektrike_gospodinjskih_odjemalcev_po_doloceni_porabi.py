import matplotlib.pyplot as plt
import numpy as np
import csv

with open('../podatki/csv/1817515S.csv', encoding="cp1250") as f:
    reader = csv.reader(f)
    data = [row for row in reader]

# izberi taprave aktualne vrstice
quarters = data[0][2:]
data = np.array(data[1:31])

for i, quarter in enumerate(quarters):
    if i % 4 != 0:
        quarters[i] = str(" ")*i
    else:
        quarters[i] = quarter[:-2]

colors = ['red', 'green', 'blue', 'orange', 'magenta']
names = ['do 1000 KWh', '1000 - 2500 KWh', '2500 - 5000 KWh', '5000 - 15000 KWh', 'nad 15000 KWh']
values = []

# izberi vrednosti z vsemi davki
for i, row in enumerate(data):
    if i % 6 == 5:
        values.append([float(n) if n != '-' else 0 for n in row[2:]])

for i, value in enumerate(values):
    plt.plot(quarters, value, color=colors[i], label='{}'.format(names[i]))
plt.xlabel('Čas [četrtletje]')
plt.ylabel('Cena [EUR/kWh]')
plt.title('Cena elektrike gospodinjskih odjemalcev po določeni porabi')
plt.legend(loc='upper left')
plt.xticks(rotation=-60)
plt.show()
