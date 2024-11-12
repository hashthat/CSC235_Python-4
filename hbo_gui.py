#!/usr/bin/env python3
import os
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load the HBO Max dataset
data_file = 'HBO_Max_Top_Picks.txt'

# Function to load and normalize data
def load_data():
    try:
        # Attempt to read with different delimiters
        data = pd.read_csv(data_file, delimiter='\t', engine='python')
        if len(data.columns) == 1:  # Fallback if it didn't read correctly
            data = pd.read_csv(data_file, delimiter=',', engine='python')
        if len(data.columns) == 1:
            data = pd.read_csv(data_file, delimiter='|', engine='python')

        # Normalize column names
        data.columns = data.columns.str.strip().str.lower()

        print("Normalized Columns:", data.columns)
        print(data.head())  # Preview the data

        return data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {e}")
        return pd.DataFrame()

# Function to display data in a table
# Function to display data in a table
def display_data():
    data = load_data()
    if data.empty:
        return

    # Use lowercase column names
    for i, row in data.iterrows():
        # Access using lowercase and stripped column names
        tree.insert("", "end", values=(
            row.get('title', 'N/A'),
            row.get('genre', 'N/A'),
            row.get('year', 'N/A'),
            row.get('imdb rating', 'N/A'),
            row.get('available regions', 'N/A')
))

# Function to plot IMDb ratings histogram
def plot_imdb_histogram():
    data = load_data()
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.hist(data['IMDb Rating'], bins=10, color='skyblue', edgecolor='black')
    ax.set_title("IMDb Ratings Histogram")
    ax.set_xlabel("IMDb Rating")
    ax.set_ylabel("Frequency")
    plot_canvas(fig)

# Function to plot top genres bar plot
def plot_top_genres():
    data = load_data()
    genres = data['Genre'].str.split(', ').explode().value_counts().head(10)
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    genres.plot(kind='bar', ax=ax, color='lightcoral')
    ax.set_title("Top 10 Genres")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Count")
    plot_canvas(fig)

# Function to create a scatter plot of IMDb rating vs. year
def plot_rating_vs_year():
    data = load_data()
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.scatter(data['Year'], data['IMDb Rating'], color='darkgreen')
    ax.set_title("IMDb Rating vs. Release Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("IMDb Rating")
    plot_canvas(fig)

# Function to update the plot canvas
def plot_canvas(fig):
    for widget in plot_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Initialize the Tkinter window
root = tk.Tk()
root.title("HBO Max Top Picks Viewer")
root.geometry("800x600")

# Table to display data
tree = ttk.Treeview(root, columns=('Title', 'Genre', 'Year', 'IMDb Rating', 'Available Regions'), show='headings')
tree.heading('Title', text='Title')
tree.heading('Genre', text='Genre')
tree.heading('Year', text='Year')
tree.heading('IMDb Rating', text='IMDb Rating')
tree.heading('Available Regions', text='Available Regions')
tree.pack(pady=10)

# Button frame
button_frame = tk.Frame(root)
button_frame.pack()

# Buttons for different plots
btn_imdb_histogram = tk.Button(button_frame, text="Show IMDb Ratings Histogram", command=plot_imdb_histogram)
btn_imdb_histogram.pack(side=tk.LEFT, padx=10)

btn_top_genres = tk.Button(button_frame, text="Show Top Genres", command=plot_top_genres)
btn_top_genres.pack(side=tk.LEFT, padx=10)

btn_scatter_plot = tk.Button(button_frame, text="Show Rating vs. Year", command=plot_rating_vs_year)
btn_scatter_plot.pack(side=tk.LEFT, padx=10)

# Frame for displaying plots
plot_frame = tk.Frame(root)
plot_frame.pack(pady=10)

# Load and display data in the table
display_data()

# Start the Tkinter main loop
root.mainloop()

