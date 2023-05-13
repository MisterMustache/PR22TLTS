import matplotlib.pyplot as plt
import csv

with open('../podatki/csv/cena_elektrike.csv', encoding="cp1252") as f:
    reader = csv.reader(f)
    data = [row for row in reader]

household = data[1]
non_household = data[7]

quarters = [x for x in data[0]][1:]
colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta']

for i, quarter in enumerate(quarters):
    if i % 4 != 0:
        quarters[i] = str(" ")*i
    else:
        quarters[i] = quarter[:-2]

plt.plot(quarters, [float(x) for x in household[1:]], label=household[0])
plt.plot(quarters, [float(x) for x in non_household[1:]], label=non_household[0])
plt.xlabel('Čas [četrtletje]')
plt.ylabel('Cena [EUR/kWh]')
plt.title('Cena električne energije')
plt.xticks(rotation=-60)
plt.legend(loc='best')
plt.show()
