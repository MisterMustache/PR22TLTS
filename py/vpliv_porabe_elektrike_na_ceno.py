from matplotlib import pyplot as plt
from collections import defaultdict
import statsmodels.api as sm
import scipy.stats as stats
import seaborn as sns
import pandas as pd


# ---------- UVOZ PODATKOV ----------
cene_df = pd.read_csv('../podatki/csv/cena_elektrike.csv', encoding='cp1250')
porabe_df = pd.read_csv('../podatki/csv/poraba_skupaj_brez-transformacij.csv', encoding='cp1250')


# ---------- PREDPROCESIRANJE ----------
# odstrani povprečne cene (na voljo je več kategoriziranih cen po določeni porabi)
cene_df = cene_df.loc[[0, 6]]

# odstrani stolpca, ki vsebujeta ime skupin/dejavnosti
cene_df = cene_df.drop([cene_df.keys()[0]], axis=1)
porabe_df = porabe_df.drop([porabe_df.keys()[0]], axis=1)

# pretvori vrednosti v numerične tipe (errors vrne NaN, če vrednost ni neko število)
for column in cene_df.columns:
    cene_df[column] = pd.to_numeric(cene_df[column], errors='coerce')

for column in porabe_df.columns:
    porabe_df[column] = pd.to_numeric(porabe_df[column], errors='coerce') / 3.6     # dodatna pretvorba iz TJ v GWh

# pogrupiraj cetrtletja skupaj
cetrtletja_po_letih = defaultdict(list)
for cetrtletje in cene_df.keys():
    cetrtletja_po_letih[cetrtletje[:4]].append(cetrtletje)

# povpreči četrtletja v eno leto
for leto in cetrtletja_po_letih.keys():
    cene_df[leto] = cene_df[cetrtletja_po_letih[leto]].mean(axis=1)
    cene_df = cene_df.drop(cetrtletja_po_letih[leto], axis=1)

# odstrani nepotrebno besedilo poleg leta
for naziv in porabe_df.keys():
    porabe_df[naziv[:4]] = porabe_df[naziv]
    porabe_df = porabe_df.drop(naziv, axis=1)

# obdrži podatke le za tista leta, ki so skupna obema
veljavna_leta = [str(n) for n in range(2012, 2022)]
for leto in cene_df.keys():
    if leto not in veljavna_leta:
        cene_df = cene_df.drop(leto, axis=1)

for leto in porabe_df.keys():
    if leto not in veljavna_leta:
        porabe_df = porabe_df.drop(leto, axis=1)

# transponiraj in ponastavi indekse (trenutno so indeksi leta, zato bodo shranjena v nov stolpec)
cene_df = cene_df.transpose()
porabe_df = porabe_df.transpose()
cene_df.reset_index(inplace=True)
porabe_df.reset_index(inplace=True)

# ustrezno spremeni imena stolpcev in ju združi
cene_df.rename(columns={'index': 'leto', 0: 'cena_gosp', 6: 'cena_negosp'}, inplace=True)
porabe_df.rename(columns={'index': 'leto', 0: 'poraba'}, inplace=True)

# razdeli cene na dva dataframe-a, saj se dva stolpca cen navezujeta na različne skupine odjemalcev
gosp_cene_df = cene_df[['leto', 'cena_gosp']].copy()
negosp_cene_df = cene_df[['leto', 'cena_negosp']].copy()

# k obema dodaj porabo (glede na leto) in popravi ime cene, da bosta enaki
gosp_cene_df = pd.merge(porabe_df, gosp_cene_df, on='leto')
negosp_cene_df = pd.merge(porabe_df, negosp_cene_df, on='leto')
gosp_cene_df.rename(columns={'cena_gosp': 'cena'}, inplace=True)
negosp_cene_df.rename(columns={'cena_negosp': 'cena'}, inplace=True)

# ---------- ZDRUŽEVANJE ---------- (izkazalo se je, da to daje slabše rezultate)
# obema dataframe-u dodaj stolpec, ki označuje svojo grupo
# gosp_cene_df['skupina'] = 0
# negosp_cene_df['skupina'] = 1

# združi ju v en dataframe
# main_df = pd.concat([gosp_cene_df, negosp_cene_df], ignore_index=True)
# print(main_df)


# ---------- ANALIZE ----------
def analyze(df, odjemalci):
    correlation, p_value = stats.pearsonr(df['poraba'], df['cena'])
    print(f'---------- {odjemalci.upper()} ODJEMALCI ----------')
    print(f'Korelacija: {correlation}')
    print(f'p-vrednost: {p_value}')

    X = df['poraba']
    y = df['cena']
    X = sm.add_constant(X)
    model = sm.OLS(y, X)
    results = model.fit()
    print(results.summary())

    sns.scatterplot(x='poraba', y='cena', data=df)
    sns.regplot(x='poraba', y='cena', data=df)
    plt.title(f'Vpliv porabe elektrike na ceno ({odjemalci} odjemalci)')
    plt.xlabel('Poraba [GWh]')
    plt.ylabel('Cena [EUR/KWh]')
    plt.show()


analyze(gosp_cene_df, 'gospodinjski')
analyze(negosp_cene_df, 'negospodinjski')
