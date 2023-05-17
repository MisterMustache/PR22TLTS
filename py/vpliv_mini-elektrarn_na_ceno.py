import numpy as np
from matplotlib import pyplot as plt
from collections import defaultdict
import statsmodels.api as sm
import scipy.stats as stats
import seaborn as sns
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeRegressor

# ---------- UVOZ PODATKOV ----------
cene_df = pd.read_csv('../podatki/csv/cena_elektrike.csv', encoding='cp1250')
proizvodi_df = pd.read_csv('../podatki/csv/1817604S_20230515-223209.csv', encoding='cp1250').drop('MERITVE', axis=1)


# ---------- PREDPROCESIRANJE ----------
# odstrani povprečne cene (na voljo je več kategoriziranih cen po določeni porabi)
cene_df = cene_df.loc[[0, 6]]

# odstrani neportebne stolpce
cene_df = cene_df.drop([cene_df.keys()[0]], axis=1)
proizvodi_df = proizvodi_df.drop(columns=proizvodi_df.columns[0::3])

# pretvori vrednosti v numerične tipe (errors vrne NaN, če vrednost ni neko število)
for column in cene_df.columns:
    cene_df[column] = pd.to_numeric(cene_df[column], errors='coerce')

for column in proizvodi_df.columns:
    proizvodi_df[f'{column[:4]}_{1 if column[5] == "S" else 2}'] = pd.to_numeric(proizvodi_df[column], errors='coerce')
    proizvodi_df = proizvodi_df.drop(columns=[column])

# pogrupiraj cetrtletja skupaj
cetrtletja_po_letih = defaultdict(list)
for cetrtletje in cene_df.keys():
    cetrtletja_po_letih[cetrtletje[:4]].append(cetrtletje)

# povpreči četrtletja v eno leto
for leto in cetrtletja_po_letih.keys():
    cene_df[leto] = cene_df[cetrtletja_po_letih[leto]].mean(axis=1)
    cene_df = cene_df.drop(cetrtletja_po_letih[leto], axis=1)

# seštej vrednosti para enakih let in počisti imena stolpcev, da bodo samo leta, brez dodatnega besedila
pari_stolpcev = [(f'{leto}_1', f'{leto}_2') for leto in range(1996, 2022)]
for col1, col2 in pari_stolpcev:
    proizvodi_df[col1[:4]] = proizvodi_df[[col1, col2]].sum(axis=1)
proizvodi_df = proizvodi_df.drop(columns=[col for col in proizvodi_df.columns if len(col) > 4])

# prikaži graf proizvodnje mini-elektrarn skozi čas (1996 - 2021)
_, ax = plt.subplots(figsize=(10, 6))
ax.plot(proizvodi_df.columns, proizvodi_df.loc[0])
plt.title('Proizvodnja zasebnih mini-elektrarn skozi leta v Sloveniji')
plt.xlabel('Čas [leto]')
plt.ylabel('Proizvod [GWh]')
plt.xticks(rotation=-45)
plt.show()

# obdrži podatke le za tista leta, ki so skupna obema
veljavna_leta = [str(n) for n in range(2012, 2022)]
for leto in proizvodi_df.keys():
    if leto not in veljavna_leta:
        proizvodi_df = proizvodi_df.drop(leto, axis=1)

# transponiraj in ponastavi indekse (trenutno so indeksi leta, zato bodo shranjena v nov stolpec)
cene_df = cene_df.transpose()
proizvodi_df = proizvodi_df.transpose()
cene_df.reset_index(inplace=True)
proizvodi_df.reset_index(inplace=True)

# ustrezno spremeni imena stolpcev in ju združi
cene_df.rename(columns={'index': 'leto', 0: 'cena_gosp', 6: 'cena_negosp'}, inplace=True)
proizvodi_df.rename(columns={'index': 'leto', 0: 'proizvod'}, inplace=True)

# spremeni nov stolpec leto v numerično vrednost
cene_df['leto'] = pd.to_numeric(cene_df['leto'], errors='coerce')
proizvodi_df['leto'] = pd.to_numeric(proizvodi_df['leto'], errors='coerce')

# razdeli cene na dva dataframe-a, saj se dva stolpca cen navezujeta na različne skupine odjemalcev
gosp_cene_df = cene_df[['leto', 'cena_gosp']].copy()
negosp_cene_df = cene_df[['leto', 'cena_negosp']].copy()

# k obema dodaj porabo (glede na leto) in popravi ime cene, da bosta enaki
gosp_cene_df = pd.merge(proizvodi_df, gosp_cene_df, on='leto')
negosp_cene_df = pd.merge(proizvodi_df, negosp_cene_df, on='leto')
gosp_cene_df.rename(columns={'cena_gosp': 'cena'}, inplace=True)
negosp_cene_df.rename(columns={'cena_negosp': 'cena'}, inplace=True)


# ---------- ANALIZE ----------
def analyze(df, odjemalci):
    correlation, p_value = stats.pearsonr(df['proizvod'], df['cena'])
    print(f'---------- {odjemalci.upper()} ODJEMALCI ----------')
    print(f'Korelacija: {correlation}')
    print(f'p-vrednost: {p_value}')

    # OLS regresijski model
    X = df['proizvod']
    y = df['cena']
    X = sm.add_constant(X)
    model = sm.OLS(y, X)
    results = model.fit()
    print(results.summary())

    # prikaz korelacije med ceno in proizvodom
    plt.subplots(figsize=(7, 5))
    sns.scatterplot(data=df, x='proizvod', y='cena')
    sns.regplot(data=df, x='proizvod', y='cena', color='darkblue')
    plt.xlabel('Proizvod [GWh]')
    plt.ylabel('Cena [EUR/KWh]')
    plt.title(f'Korelacija med proizvodom mini-elektrarn in ceno ({odjemalci} odjemalci)')
    plt.show()


# odstranitev osamelcev
gosp_cene_df.drop([8], inplace=True)
negosp_cene_df.drop([0, 1], inplace=True)

print(gosp_cene_df)
print(negosp_cene_df)

analyze(gosp_cene_df, 'gospodinjski')
analyze(negosp_cene_df, 'negospodinjski')
