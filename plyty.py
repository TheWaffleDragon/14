import pandas as pd

data = pd.read_html('https://www.officialcharts.com/chart-news/the-best-selling-albums-of-all-time-on-the-official-uk-chart__15551/', header=0)
df = data[0]
#%%
#1 Zamień nagłówki kolumn na polskie odpowiedniki: ['TYTUŁ','ARTYSTA','ROK','MAX POZ']
df.rename(columns={'TITLE':'TYTUŁ','ARTIST':'ARTYSTA','YEAR':'ROK','HIGH POSN':'MAX POZ'},inplace=True)
#%%
#2 Ilu pojedynczych artystów znajduje się na liście?
n_artists = df['ARTYSTA'].nunique()
print(f'na liscie znajduje się : {n_artists} indywidualnych artystów')
#%%
#3 Które zespoły pojawiają się najczęściej na liście?
freq_artists = df['ARTYSTA'].value_counts()
n = freq_artists.max()
artists_max = freq_artists.where(freq_artists==n)
artists_max = artists_max.dropna()
print(f'Na liscie najczęciej pojawiały sie: {artists_max.index[0]} i {artists_max.index[1]}')
#%%
#4 Zmień nagłówki kolumn, tak aby każdy z nich rozpoczynał się od wielkiej litery, a pozostałe były wprowadzone małymi literami
df.columns = df.columns.astype("str")
df.columns = df.columns.str.lower()
df.columns = df.columns.str.capitalize()

#%%
#5 Wyrzuć z tabeli kolumnę ‘Max Poz’
df = df.drop('Max poz',axis=1)

#%%
#6 W którym roku wyszło najwięcej albumów znajdujących się na liście?
freq_year = df['Rok'].value_counts()
print(f' Najwiecej albumow wydano w roku: {freq_year.head(1).index[0]}')

#%%
#7 Ile albumów wydanych między 1960 a 1990 rokiem włącznie znajduje się na liście?
df_sorted = df.sort_values(by='Rok')
cutoff = df_sorted.where(df_sorted['Rok']<=1990).dropna()['Rok']
n_records = cutoff.count()
print(f' Do roku 1990 wydano: {n_records} albumy')

#%%
#8 W którym roku wydany został najmłodszy album na liście?
newest = df.sort_values(by ="Rok", ascending=False).head(1)['Rok']
newest = newest.reset_index(drop=True)
print(f'Najnowszy album na liscie zostal wydany w roku: {newest.get(key=0)}')

#%%
#9 Przygotuj listę najwcześniej wydanych albumów każdego artysty, który znalazł się na liście.
grupy = df.groupby('Artysta').min()
grupy = grupy.drop('Pos', axis=1)

#%%
#10 Listę zapisz do pliku csv.
grupy.to_csv('Pierwsze_plyty', index=True)
print('Lista pierwszych plyt została wygenerowana i zapisana do pliku.')
