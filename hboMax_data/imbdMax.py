#!/usr/bin/env python3
import os
import difflib
import pandas as pd
import matplotlib.pyplot as plt

# Load the HBO Max dataset
data = pd.read_csv('data.csv')

# Normalize column names
data.columns = data.columns.str.strip().str.lower()

# Helper function to get the closest match for a column name
def get_column_name(guess, columns):
    matches = difflib.get_close_matches(guess, columns, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Get column names using the helper function
imdb_rating_col = get_column_name('imdb_rating', data.columns)
genres_col = get_column_name('genre', data.columns)
release_year_col = get_column_name('year', data.columns)
available_countries_col = get_column_name('available_regions', data.columns)

# Check if the necessary columns were found
if not all([imdb_rating_col, genres_col, release_year_col, available_countries_col]):
    print("One or more required columns could not be found. Please check the column names.")
    exit(1)

# Filter for top picks with IMDb ratings above 7.5
top_picks = data[data[imdb_rating_col] > 7.5].sort_values(by=imdb_rating_col, ascending=False)

# Select relevant columns for display
top_picks_list = top_picks[['title', genres_col, release_year_col, imdb_rating_col, available_countries_col]]

# Display the top picks
print(top_picks_list.head())

# Create a bar chart for top-rated shows
plt.figure(figsize=(12, 8))
top_titles = top_picks_list['title'].head(10)
top_ratings = top_picks_list[imdb_rating_col].head(10)

# Plotting
plt.barh(top_titles, top_ratings, color='skyblue')
plt.xlabel('IMDb Rating')
plt.title('Top 10 HBO Max Picks by IMDb Rating')
plt.gca().invert_yaxis()  # Invert y-axis to have the highest rating at the top
plt.grid(axis='x')

# Display the plot
plt.tight_layout()
plt.show()

