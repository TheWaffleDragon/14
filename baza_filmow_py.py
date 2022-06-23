#%%Import bibliotek
import pandas as pd
import numpy as np

#%%Import baz z plików

data_movies = pd.read_csv('tmdb_movies.csv')
data_genres = pd.read_csv('tmdb_genres.csv')
data_genres.rename(columns={'Unnamed: 0':'genre_id'},inplace=True)
#1: Zwróć listę 10 najwyżej ocenianych filmów (vote_average), których liczba głosów (vote_count) jest większa od 3. kwartyla rozkładu liczby głosów.

#%% 3. kwartyla rozkładu liczby głosów
q3 = data_movies.quantile(0.75)['vote_count']
data_movie_q3 = data_movies.where(data_movies['vote_count']>q3).dropna()

#%%sortowanie
data_movie_q3 = data_movie_q3.sort_values(by = 'vote_average', ascending=False)

#%%
movies_best = data_movie_q3.head(10)
movies_best = movies_best.reset_index(drop=True)
print('10 najwyzej ocenianych filmów to:')
print(movies_best['title'])

#%%
'''
2: Pogrupuj tabelę w taki sposób, aby otrzymać średni przychód (revenue) oraz 
średni budżet (budget) w danym roku dla filmów opublikowanych od 2010 (włącznie) 
do 2016 roku (włącznie). Następnie na tej podstawie stwórz wykres, w którym 
średnie przychody są wykresem kolumnowym, a średni budżet wykresem liniowym na 
tych samych osiach. Sformatuj odpowiednio oś X oraz oś Y. Dodaj tytuł wykresu, 
oraz legendę, która znajduje się w prawym górnym rogu płótna, lecz poza obszarem osi.
'''

#edycja formatu daty
data_movies['release_date'] = pd.to_datetime(data_movies["release_date"])

#grupowanie po latach
data_movies_year= data_movies[["release_date","budget","revenue"]] 
data_movies_year = data_movies_year.groupby(pd.Grouper(key='release_date',freq='Y')).mean()
data_movies_year = data_movies_year.reset_index()
data_movies_year['release_date'] = data_movies_year['release_date'].dt.year
start = data_movies_year.where(data_movies_year['release_date']>=2010).dropna()
start = start.where(start['release_date']<=2016).dropna().reset_index()

#wykes
import matplotlib.pyplot as plt

def million(x, pos):
        return ' {:2.1f}M'.format(x*1e-6)

fig, ax = plt.subplots()
formatter = plt.FuncFormatter(million)
ax.yaxis.set_major_formatter(formatter)
ax.bar(start['release_date'],start['revenue'], label = "revenue")
ax.plot(start['release_date'],start['budget'], color='red', label = "budget")
ax.set_title("Sredni przychod i budzet filmu w latach 2010-2016")
ax.legend(loc=(1.05,0.8))


#%%
'''
3: Baza filmów zawiera kolumnę z id gatunku (genre_id). 
Na tej podstawie połącz ze sobą bazę filmów z bazą gatunków, 
tak aby w bazie filmów można było odczytać nazwę gatunku filmu.
'''
movies_id = pd.merge(data_movies, data_genres, on='genre_id')


#%%
'''
4: Jaki gatunek filmu z bazy pojawia się w niej najczęściej? 
Ile filmów tego gatunku znajduje się w bazie?
'''
genre_count = movies_id.groupby('genres').count()
x= genre_count.where(genre_count['genre_id'] == genre_count['genre_id'].max()).dropna()
print(x['genre_id'])



#%%
'''
5:Filmy, którego gatunku trwają średnio najdłużej (runtime)?    
'''
genre_run = movies_id['runtime']
genre_run =  movies_id.groupby('genres').mean()
y = genre_run.where(genre_run['runtime'] == genre_run['runtime'].max()).dropna()
print(y['runtime'])

#%%
'''
6: Stwórz histogram czasu trwania filmów z gatunku, 
który cechuje się największym średnim czasem trwania.
'''
hist = movies_id.where(movies_id['genres']=='History').dropna()
hist['runtime'].hist(bins=5)