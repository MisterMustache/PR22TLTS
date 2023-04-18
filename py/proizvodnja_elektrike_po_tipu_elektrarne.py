import matplotlib.pyplot as plt
import numpy as np
import csv

with open('../podatki/csv/proizvodnja_elektrike_po_tipu_elektrarne.csv', encoding="cp1250") as f:
    reader = csv.reader(f)
    data = [row for row in reader]

# izberi taprave aktualne vrstice
data = np.array(data[2:8])
data = np.delete(data, 1, axis=0)

values = []

# pretvori v števila
for row in data:
    values.append([float(n) if n != '-' else 0 for n in row[2:]])

years = [str(year) for year in range(2004, 2022)]
colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta']
names = ['Hidroelektrarne', 'Termoelektrarne', 'Jedrska elektrarna', 'Sončne elektrarne', 'Vetrne elektrarne']

for i, value in enumerate(values):
    plt.plot(years, value, color=colors[i], label='{}'.format(names[i]))
plt.xlabel('Čas [leta]')
plt.ylabel('Proizvod [GWh]')
plt.title('Proizvodnja električne energije')
plt.legend(loc='lower left')
plt.show()

