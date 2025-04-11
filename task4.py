#4
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

# Load dataset
apps_df = pd.read_csv('googleplaystore.csv')

# Convert 'Size' to numeric (handling 'M' for MB and 'K' for KB)
def convert_size(size):
    if isinstance(size, str):
        if 'M' in size:
            return float(size.replace('M', ''))
        elif 'K' in size:
            return float(size.replace('K', '')) / 1024
    return None  # Ignore sizes like 'Varies with device'

apps_df['Size'] = apps_df['Size'].astype(str).apply(convert_size)

# Convert 'Reviews' to numeric (handling 'M' for millions)
def convert_reviews(reviews):
    if isinstance(reviews, str):
        if 'M' in reviews:
            return float(reviews.replace('M', '')) * 1_000_000
        elif 'K' in reviews:
            return float(reviews.replace('K', '')) * 1_000
    try:
        return float(reviews)
    except ValueError:
        return None

apps_df['Reviews'] = apps_df['Reviews'].astype(str).apply(convert_reviews)

# Convert 'Last Updated' to datetime
apps_df['Last Updated'] = pd.to_datetime(apps_df['Last Updated'], errors='coerce')

# Filter data based on conditions
filtered_df = apps_df[
    (apps_df['Rating'] < 4.0) &
    (apps_df['Reviews'] >= 10) &
    (apps_df['App'].str.contains('C', case=False, na=False))
]

# Get categories with more than 50 apps
category_counts = filtered_df['Category'].value_counts()
valid_categories = category_counts[category_counts > 50].index
filtered_df = filtered_df[filtered_df['Category'].isin(valid_categories)]

# Convert IST time
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist).hour

# Only show the graph if the time is between 4 PM – 6 PM IST
if 16 <= current_time < 18:
    fig = px.violin(
        filtered_df,
        x='Category',
        y='Rating',
        box=True,
        points='all',
        title='Distribution of Ratings for Each App Category',
        color='Category'
    )
    fig.show()
else:
    print("Graph is only visible between 4 PM and 6 PM IST")
