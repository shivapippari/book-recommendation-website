import json
import pandas as pd
from collections import Counter

# Load the data
books = pd.read_csv(r"./filtered_Books.csv", delimiter=';', on_bad_lines='warn', encoding='ISO-8859-1')
ratings = pd.read_csv(r"filtered_Book-Ratings.csv", delimiter=';', on_bad_lines='warn', encoding='ISO-8859-1')

# Preprocess the data
books['ISBN'] = books['ISBN'].str.upper()
books.drop_duplicates(keep='last', inplace=True)
books.reset_index(drop=True, inplace=True)


# Preprocess the ratings data
ratings['ISBN'] = ratings['ISBN'].str.upper()
ratings.drop_duplicates(keep='last', inplace=True)
ratings.reset_index(drop=True, inplace=True)

# Merge the data
dataset = pd.merge(books, ratings, on='ISBN', how='inner')
#books = dataset.drop_duplicates(subset='ISBN')
# Save the sampled dataset to a new CSV file
# Create the pivot table
popularity_threshold = 30
user_count = dataset['User-ID'].value_counts()
data = dataset[dataset['User-ID'].isin(user_count[user_count >= popularity_threshold].index)]
rat_count = data['Book-Rating'].value_counts()
data = data[data['Book-Rating'].isin(rat_count[rat_count >= popularity_threshold].index)]
matrix = data.pivot_table(index='User-ID', columns='ISBN', values='Book-Rating').fillna(0)
average_rating = pd.DataFrame(dataset.groupby('ISBN')['Book-Rating'].mean())
average_rating['ratingCount'] = pd.DataFrame(dataset.groupby('ISBN')['Book-Rating'].count())
average_rating.sort_values('ratingCount', ascending=False).head()

# Define the recommendation function
def get_recommendations(book_name):
    
    book_row = books.loc[books['Book-Title'] == book_name].reset_index(drop=True)
    
    if book_row.empty:
        return [] 
    
    isbn = book_row.iloc[0]['ISBN']
    
    if isbn not in matrix.columns:
        return [] 
    
   
    row = matrix[isbn]
    correlation = pd.DataFrame(matrix.corrwith(row), columns=['Pearson Corr'])
    corr = correlation.join(average_rating['ratingCount'])
    res = corr.sort_values('Pearson Corr', ascending=False).head(6)[1:].index
    corr_books = pd.merge(pd.DataFrame(res, columns=['ISBN']), books[['ISBN', 'Book-Title', 'Image-URL-L']], on='ISBN')
    recommendations = [{"title": row['Book-Title'], "image_url": row['Image-URL-L']} for index, row in corr_books.iterrows()]
    
    return recommendations


import sys
user_preferences = json.loads(sys.argv[1])
book_name = user_preferences['bookName']
recommendations = get_recommendations(book_name)

# recommendations= get_recommendations("Harry Potter and the Sorcerer's Stone (Harry Potter (Paperback))")

print(json.dumps(recommendations))