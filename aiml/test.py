# %%
import re
import pickle
import operator
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
from scipy.sparse import csr_matrix
from pandas.api.types import is_numeric_dtype
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

import warnings
warnings.filterwarnings("ignore")

books = pd.read_csv("./Books.csv", delimiter=';', error_bad_lines=False, warn_bad_lines=True, encoding='ISO-8859-1')

users = pd.read_csv(r"Users.csv", delimiter=';', on_bad_lines='warn', encoding='ISO-8859-1')
ratings = pd.read_csv(r"Book-Ratings.csv", delimiter=';', on_bad_lines='warn', encoding='ISO-8859-1')

print("Books Data:    ", books.shape)
print("Users Data:    ", users.shape)
print("Books-ratings: ", ratings.shape)

books.drop(['Image-URL-M', 'Image-URL-L'], axis=1, inplace=True)


# %%
## Checking for null values
books.isnull().sum() 

# %%
books.loc[books['Book-Author'].isnull(),:]

# %%
books.loc[books['Publisher'].isnull(),:]

# %%
books.at[187689 ,'Book-Author'] = 'Other'

books.at[128890 ,'Publisher'] = 'Other'
books.at[129037 ,'Publisher'] = 'Other'

# %%
## Checking for column Year-of-publication
books['Year-Of-Publication'].unique()

# %%
pd.set_option('display.max_colwidth', None)

# %%
books.loc[books['Year-Of-Publication'] == 'DK Publishing Inc',:]

# %%
books.loc[books['Year-Of-Publication'] == 'Gallimard',:]

# %%
books.at[209538 ,'Publisher'] = 'DK Publishing Inc'
books.at[209538 ,'Year-Of-Publication'] = 2000
books.at[209538 ,'Book-Title'] = 'DK Readers: Creating the X-Men, How It All Began (Level 4: Proficient Readers)'
books.at[209538 ,'Book-Author'] = 'Michael Teitelbaum'

books.at[221678 ,'Publisher'] = 'DK Publishing Inc'
books.at[221678 ,'Year-Of-Publication'] = 2000
books.at[209538 ,'Book-Title'] = 'DK Readers: Creating the X-Men, How Comic Books Come to Life (Level 4: Proficient Readers)'
books.at[209538 ,'Book-Author'] = 'James Buckley'

books.at[220731 ,'Publisher'] = 'Gallimard'
books.at[220731 ,'Year-Of-Publication'] = '2003'
books.at[209538 ,'Book-Title'] = 'Peuple du ciel - Suivi de Les bergers '
books.at[209538 ,'Book-Author'] = 'Jean-Marie Gustave Le ClÃ?Â©zio'

# %%
## Converting year of publication in Numbers
books['Year-Of-Publication'] = books['Year-Of-Publication'].astype(int)

# %%
print(sorted(list(books['Year-Of-Publication'].unique())))

# %%
## Replacing Invalid years with max year
count = Counter(books['Year-Of-Publication'])
[k for k, v in count.items() if v == max(count.values())]

# %%
books.loc[books['Year-Of-Publication'] > 2021, 'Year-Of-Publication'] = 2002
books.loc[books['Year-Of-Publication'] == 0, 'Year-Of-Publication'] = 2002

# %%
## Uppercasing all alphabets in ISBN
books['ISBN'] = books['ISBN'].str.upper()

# %%
## Drop duplicate rows
books.drop_duplicates(keep='last', inplace=True) 
books.reset_index(drop = True, inplace = True)

# %%
books.info()

# %%
books.head()

# %%
"""
<b>Users Dataset Pre-processing
"""

# %%
print("Columns: ", list(users.columns))
users.head()

# %%
## Checking null values
print(users.isna().sum())               

# %%
## Check for all values present in Age column
print(sorted(list(users['Age'].unique())))

# %%
required = users[users['Age'] <= 80]
required = required[required['Age'] >= 10]

# %%
mean = round(required['Age'].mean())   
mean

# %%
users.loc[users['Age'] > 80, 'Age'] = mean    #outliers with age grater than 80 are substituted with mean 
users.loc[users['Age'] < 10, 'Age'] = mean    #outliers with age less than 10 years are substitued with mean
users['Age'] = users['Age'].fillna(mean)      #filling null values with mean
users['Age'] = users['Age'].astype(int)       #changing Datatype to int

# %%
list_ = users.Location.str.split(', ')

city = []
state = []
country = []
count_no_state = 0    
count_no_country = 0

for i in range(0,len(list_)):
    if list_[i][0] == ' ' or list_[i][0] == '' or list_[i][0]=='n/a' or list_[i][0] == ',':  #removing invalid entries too
        city.append('other')
    else:
        city.append(list_[i][0].lower())

    if(len(list_[i])<2):
        state.append('other')
        country.append('other')
        count_no_state += 1
        count_no_country += 1
    else:
        if list_[i][1] == ' ' or list_[i][1] == '' or list_[i][1]=='n/a' or list_[i][1] == ',':   #removing invalid entries 
            state.append('other')
            count_no_state += 1            
        else:
            state.append(list_[i][1].lower())
        
        if(len(list_[i])<3):
            country.append('other')
            count_no_country += 1
        else:
            if list_[i][2] == ''or list_[i][1] == ',' or list_[i][2] == ' ' or list_[i][2] == 'n/a':
                country.append('other')
                count_no_country += 1
            else:
                country.append(list_[i][2].lower())
        
users = users.drop('Location',axis=1)

temp = []
for ent in city:
    c = ent.split('/')            #handling cases where city/state entries from city list as state is already given 
    temp.append(c[0])

df_city = pd.DataFrame(temp,columns=['City'])
df_state = pd.DataFrame(state,columns=['State'])
df_country = pd.DataFrame(country,columns=['Country'])

users = pd.concat([users, df_city], axis=1)
users = pd.concat([users, df_state], axis=1)
users = pd.concat([users, df_country], axis=1)

print(count_no_country)   #printing the number of countries didnt have any values 
print(count_no_state)     #printing the states which didnt have any values

# %%
## Drop duplicate rows
users.drop_duplicates(keep='last', inplace=True)
users.reset_index(drop=True, inplace=True)

# %%
users.info()

# %%
users.head()

# %%
"""
<b>Books-Ratings Dataset Pre-processing
"""

# %%
print("Columns: ", list(ratings.columns))
ratings.head()

# %%
## Checking for null values
ratings.isnull().sum() 

# %%
## checking all ratings number or not
print(is_numeric_dtype(ratings['Book-Rating']))

# %%
## checking User-ID contains only number or not
print(is_numeric_dtype(ratings['User-ID']))

# %%
## checking ISBN
flag = 0
k =[]
reg = "[^A-Za-z0-9]"

for x in ratings['ISBN']:
    z = re.search(reg,x)    
    if z:
        flag = 1

if flag == 1:
    print("False")
else:
    print("True")

# %%
## removing extra characters from ISBN (from ratings dataset) existing in books dataset
bookISBN = books['ISBN'].tolist() 
reg = "[^A-Za-z0-9]" 
for index, row_Value in ratings.iterrows():
    z = re.search(reg, row_Value['ISBN'])    
    if z:
        f = re.sub(reg,"",row_Value['ISBN'])
        if f in bookISBN:
            ratings.at[index , 'ISBN'] = f

# %%
## Uppercasing all alphabets in ISBN
ratings['ISBN'] = ratings['ISBN'].str.upper()

# %%
## Drop duplicate rows
ratings.drop_duplicates(keep='last', inplace=True)
ratings.reset_index(drop=True, inplace=True)

# %%
ratings.info()

# %%
ratings.head()

# %%
"""
<h3><b>Merging of all three Tables
"""

# %%
"""
<b>Merging Books, Users and Rating Tables in One
"""

# %%
dataset = pd.merge(books, ratings, on='ISBN', how='inner')
dataset = pd.merge(dataset, users, on='User-ID', how='inner')
dataset.info()

# %%
"""
<b>Divide complete data on the basis of Implicit and Explicit ratings datasets
"""

# %%
## Explicit Ratings Dataset
dataset1 = dataset[dataset['Book-Rating'] != 0]
dataset1 = dataset1.reset_index(drop = True)
dataset1.shape

# %%
## Implicit Ratings Dataset
dataset2 = dataset[dataset['Book-Rating'] == 0]
dataset2 = dataset2.reset_index(drop = True)
dataset2.shape

# %%
dataset1.head()
len(dataset1)

"""
<h2><b>Recommendation Systems
"""

# %%
bookName = input("Enter a book name: ")
number = int(input("Enter number of books to recommend: "))

# Harry Potter and the Sorcerer's Stone (Harry Potter (Paperback))
"""
<b><h5>3. Books by same author, publisher of given book name
"""

# %%
def printBook(k, n):
    z = k['Book-Title'].unique()
    for x in range(len(z)):
        print(z[x])
        if x >= n-1:
            break


# %%
def get_books(dataframe, name, n):
    print("\nBooks by same Author:\n")
    au = dataframe['Book-Author'].unique()
    data = dataset1[dataset1['Book-Title'] != name]
    k2 = None  # Initialize k2

    if au[0] in list(data['Book-Author'].unique()):
        k2 = data[data['Book-Author'] == au[0]]
        k2 = k2.sort_values(by=['Book-Rating'])
        printBook(k2, n)
    else:
        print("Author not found in the dataset.")

    print("\n\nBooks by same Publisher:\n")
    pu = dataframe['Publisher'].unique()  # Changed variable name to pu for clarity

    if pu[0] in list(data['Publisher'].unique()):
        k2 = pd.DataFrame(data[data['Publisher'] == pu[0]])
        k2 = k2.sort_values(by=['Book-Rating'])
        printBook(k2, n)
    else:
        print("Publisher not found in the dataset.")


# %%
if bookName in list(dataset1['Book-Title'].unique()):
    d = dataset1[dataset1['Book-Title'] == bookName]
    get_books(d, bookName, number)
else:
    print("Invalid Book Name!!")

# %%
# %%
popularity_threshold = 50

user_count = dataset1['User-ID'].value_counts()
data = dataset1[dataset1['User-ID'].isin(user_count[user_count >= popularity_threshold].index)]
rat_count = data['Book-Rating'].value_counts()
data = data[data['Book-Rating'].isin(rat_count[rat_count >= popularity_threshold].index)]

matrix = data.pivot_table(index='User-ID', columns='ISBN', values = 'Book-Rating').fillna(0)
average_rating = pd.DataFrame(dataset1.groupby('ISBN')['Book-Rating'].mean())
average_rating['ratingCount'] = pd.DataFrame(ratings.groupby('ISBN')['Book-Rating'].count())
average_rating.sort_values('ratingCount', ascending=False).head()
isbn = books.loc[books['Book-Title'] == bookName].reset_index(drop = True).iloc[0]['ISBN']
row = matrix[isbn]
correlation = pd.DataFrame(matrix.corrwith(row), columns = ['Pearson Corr'])
corr = correlation.join(average_rating['ratingCount'])

res = corr.sort_values('Pearson Corr', ascending=False).head(number+1)[1:].index
# Merge to include the Image-URL-S
corr_books = pd.merge(pd.DataFrame(res, columns=['ISBN']), books[['ISBN', 'Book-Title', 'Image-URL-S']], on='ISBN')
print("\n Recommended Books: \n")
for index, row in corr_books.iterrows():
    print(f"Title: {row['Book-Title']}, Image URL: {row['Image-URL-S']}")
