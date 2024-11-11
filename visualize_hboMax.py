#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import re

# Function to read and parse HBO_Max_Top_Picks.txt
def parse_hbo_file(file_path):
    data = {
        "Title": [],
        "Genre": [],
        "Year": [],
        "IMDb Rating": [],
        "Available Regions": []
    }

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 6):  # Every entry has 6 lines (5 data lines + 1 empty line)
            title = re.search(r"Title: (.+)", lines[i]).group(1)
            genre = re.search(r"Genre: (.+)", lines[i + 1]).group(1)
            year = int(re.search(r"Year: (\d+)", lines[i + 2]).group(1))
            imdb_rating = float(re.search(r"IMDb Rating: ([\d.]+)", lines[i + 3]).group(1))
            available_regions = re.search(r"Available in: (.+)", lines[i + 4]).group(1)

            data["Title"].append(title)
            data["Genre"].append(genre)
            data["Year"].append(year)
            data["IMDb Rating"].append(imdb_rating)
            data["Available Regions"].append(available_regions)

    # Create DataFrame
    df = pd.DataFrame(data)
    return df

# Function to plot the data
def plot_hbo_data(df):
    # Plot 1: Histogram of IMDb Ratings
    plt.figure(figsize=(10, 6))
    plt.hist(df["IMDb Rating"], bins=10, color='skyblue', edgecolor='black')
    plt.title("Distribution of IMDb Ratings")
    plt.xlabel("IMDb Rating")
    plt.ylabel("Frequency")
    plt.grid()
    plt.show()

    # Plot 2: Bar plot of Top Genres
    plt.figure(figsize=(12, 6))
    genre_counts = df["Genre"].value_counts().head(10)
    genre_counts.plot(kind='bar', color='lightgreen')
    plt.title("Top Genres in HBO Max Picks")
    plt.xlabel("Genre")
    plt.ylabel("Number of Titles")
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.show()

    # Plot 3: Scatter plot of IMDb Rating vs Year
    plt.figure(figsize=(10, 6))
    plt.scatter(df["Year"], df["IMDb Rating"], color='purple', alpha=0.7)
    plt.title("IMDb Rating vs. Release Year")
    plt.xlabel("Release Year")
    plt.ylabel("IMDb Rating")
    plt.grid()
    plt.show()

# Main function
if __name__ == "__main__":
    file_path = 'HBO_Max_Top_Picks.txt'
    df = parse_hbo_file(file_path)
    
    if not df.empty:
        print("Data successfully parsed. Here is a preview:")
        print(df.head())

        # Plot the data
        plot_hbo_data(df)
    else:
        print("No data found in the text file.")

