#final dashboard

import os
import webbrowser
import pandas as pd
import plotly.express as px
import plotly.io as pio
from datetime import datetime
import pytz
import numpy as np

# Load datasets (update paths if needed)
apps_df = pd.read_csv("googleplaystore.csv")
reviews_df = pd.read_csv("googleplaystore_user_reviews.csv")
file_path = "googleplaystore14.csv"  # Update with the correct path

# Convert Last Updated column to datetime
apps_df["Last Updated"] = pd.to_datetime(apps_df["Last Updated"], errors='coerce')

# Remove non-numeric values and convert "Installs" column to float
apps_df["Installs"] = pd.to_numeric(apps_df["Installs"].str.replace(r'[,\+]', '', regex=True), errors='coerce')

# Convert "Reviews" column to numeric
apps_df["Reviews"] = pd.to_numeric(apps_df["Reviews"], errors='coerce')

# Merge datasets on 'App' column
merged_df = pd.merge(apps_df, reviews_df, on='App')

# Filter apps with more than 1,000 reviews
filtered_df = merged_df.groupby('App').filter(lambda x: len(x) > 1000)

# Identify top 5 categories by total reviews
top_categories = filtered_df.groupby('Category').size().nlargest(5).index

# Filter for top 5 categories
filtered_df = filtered_df[filtered_df['Category'].isin(top_categories)]

# Define rating groups
def rating_group(rating):
    if rating <= 2:
        return '1-2 Stars'
    elif rating <= 4:
        return '3-4 Stars'
    else:
        return '4-5 Stars'

filtered_df['Rating_Group'] = filtered_df['Rating'].apply(rating_group)

# Count sentiments within each group
sentiment_counts = filtered_df.groupby(['Category', 'Rating_Group', 'Sentiment']).size().reset_index(name='Count')

# Create stacked bar chart
fig1 = px.bar(
    sentiment_counts,
    x='Rating_Group',
    y='Count',
    color='Sentiment',
    facet_col='Category',
    title='Sentiment Distribution by Rating Group for Top 5 App Categories',
    barmode='stack'
)
fig1.write_html("app_rating_distribution.html")

# Time-based access control
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist).time()

def is_time_allowed(start, end):
    return start <= current_time <= end

# Delete previous files if they exist
for filename in ["top_categories.html", "global_installs.html", "filtered_apps.html", "app_size_vs_rating.html"]:
    if os.path.exists(filename):
        os.remove(filename)

# Task 2: Available 3 PM – 5 PM IST
if is_time_allowed(datetime.strptime("15:00", "%H:%M").time(), datetime.strptime("17:00", "%H:%M").time()):
    category_counts = apps_df['Category'].value_counts().nlargest(10)
    fig2 = px.bar(category_counts, x=category_counts.index, y=category_counts.values, title='Top 10 Categories by Number of Apps', labels={'x': 'Category', 'y': 'Number of Apps'})
    fig2.write_html("top_categories.html")

# Task 3: Available 6 PM – 8 PM IST
if is_time_allowed(datetime.strptime("18:00", "%H:%M").time(), datetime.strptime("20:00", "%H:%M").time()):
    df = pd.read_csv(file_path)
    df = df[['Category', 'Installs', 'Country']].dropna()
    df['Installs'] = df['Installs'].astype(str).str.replace(r'[^\d]', '', regex=True)
    df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce').fillna(0).astype(int)
    df = df[~df['Category'].str.startswith(('A', 'C', 'G', 'S'))]
    top_categories = df.groupby('Category')['Installs'].sum().nlargest(5).index
    df = df[df['Category'].isin(top_categories)]
    df_grouped = df.groupby(['Country', 'Category'])['Installs'].sum().reset_index()
    df_grouped['Highlight'] = df_grouped['Installs'] > 1_000_000
    fig3 = px.choropleth(
        df_grouped,
        locations="Country",
        locationmode="country names",
        color="Category",
        hover_data=["Installs"],
        title="Global Installs by Category (Filtered)"
    )
    fig3.write_html("global_installs.html")

# Task 4: Available 4 PM – 6 PM IST
if is_time_allowed(datetime.strptime("16:00", "%H:%M").time(), datetime.strptime("18:00", "%H:%M").time()):
    filtered_df = apps_df[(apps_df['Rating'] < 4.0) & (apps_df['Reviews'] >= 10)]
    category_counts = filtered_df['Category'].value_counts()
    valid_categories = category_counts[category_counts > 50].index
    filtered_df = filtered_df[filtered_df['Category'].isin(valid_categories)]
    fig4 = px.violin(filtered_df, x='Category', y='Rating', box=True, points='all', title='Distribution of Ratings for Each App Category', color='Category')
    fig4.write_html("filtered_apps.html")

# Task 5: Available 5 PM – 7 PM IST
if is_time_allowed(datetime.strptime("17:00", "%H:%M").time(), datetime.strptime("19:00", "%H:%M").time()):
    fig5 = px.scatter(filtered_df, x="Installs", y="Rating", size="Installs", color="Category", hover_name="App", title="App Installs vs. Average Rating")
    fig5.write_html("app_size_vs_rating.html")

# Generate dashboard with buttons
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Google Play Store Analytics</title>
    <script>
        function openPlot(filename) {
            window.open(filename, '_blank');
        }
    </script>
</head>
<body style='background-color: black; color: white; text-align: center;'>
    <h1><img src='https://tse4.mm.bing.net/th?id=OIP.aK0pFHbj6X0jqS0ZGmqGmAHaEK&pid=Api&P=0&h=180' alt='Google Play Store Logo' width='50' style='vertical-align: middle;'> Google Play Store Analytics</h1>
    <button onclick="openPlot('app_rating_distribution.html')">Sentiment Distribution</button>
    <button onclick="openPlot('top_categories.html')">Top Categories</button>
    <button onclick="openPlot('global_installs.html')">Global Installs</button>
    <button onclick="openPlot('filtered_apps.html')">Filtered Apps</button>
    <button onclick="openPlot('app_size_vs_rating.html')">App Size vs Rating</button>
</body>
</html>
"""

with open("dashboard.html", "w", encoding="utf-8") as f:
    f.write(html_content)

webbrowser.open('file://' + os.path.realpath("dashboard.html"))
