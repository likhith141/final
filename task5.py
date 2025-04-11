#5
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
from datetime import datetime
import pytz

# Load the dataset
file_path = "googleplaystore14.csv"  # Update with the correct path

df = pd.read_csv(file_path)

# Define the relevant categories
categories_of_interest = {'GAME', 'BEAUTY', 'BUSINESS', 'COMICS', 'COMMUNICATION',
                          'DATING', 'ENTERTAINMENT', 'SOCIAL', 'EVENTS'}

# Filter dataset based on categories and valid ratings
df_filtered = df[df['Category'].isin(categories_of_interest)]
df_filtered = df_filtered[df_filtered['Rating'] > 3.5]
df_filtered = df_filtered.dropna(subset=['Rating', 'Size', 'Installs', 'Reviews', 'Sentiment_Subjectivity'])

# Convert 'Reviews' to numerical values
df_filtered['Reviews'] = df_filtered['Reviews'].astype(int)

# Convert 'Sentiment_Subjectivity' to numerical values
df_filtered['Sentiment_Subjectivity'] = df_filtered['Sentiment_Subjectivity'].astype(float)

# Function to convert 'Size' to numerical values in MB
def convert_size(size):
    if 'M' in size:
        return float(size.replace('M', ''))
    elif 'k' in size:
        return float(size.replace('k', '')) / 1024  # Convert KB to MB
    else:
        return np.nan

df_filtered['Size'] = df_filtered['Size'].apply(convert_size)
df_filtered = df_filtered.dropna(subset=['Size'])

# Convert 'Installs' to numerical values
df_filtered['Installs'] = df_filtered['Installs'].str.replace('[+,]', '', regex=True).astype(int)

# Apply additional filters
df_filtered = df_filtered[(df_filtered['Reviews'] > 500) &
                          (df_filtered['Sentiment_Subjectivity'] > 0.5) &
                          (df_filtered['Installs'] > 50000)]

# Check current time in IST timezone
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist).hour

# Only display graph between 5 PM and 7 PM IST
if 12 <= current_time < 19:
    # Create an interactive bubble chart using Plotly
    fig = px.scatter(df_filtered, x="Size", y="Rating", size="Installs", color="Category",
                     hover_name="App", title="App Size vs. Average Rating (Filtered)",
                     labels={"Size": "App Size (MB)", "Rating": "Average Rating"},
                     size_max=50)
    
    # Save the figure as an interactive HTML file
    pio.write_html(fig, file="app_size_vs_rating.html", auto_open=True)
else:
    print("Graph is only available between 5 PM and 7 PM IST.")
