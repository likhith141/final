#2
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

# Load dataset
apps_df = pd.read_csv('googleplaystore.csv')

# Convert 'Size' to numeric (handling 'M' for MB and 'K' for KB)
def convert_size(size):
    if isinstance(size, str):  # Ensure it's a string before processing
        if 'M' in size:
            return float(size.replace('M', ''))
        elif 'K' in size:
            return float(size.replace('K', '')) / 1024
    return None  # Ignore 'Varies with device' and NaN values

apps_df['Size'] = apps_df['Size'].astype(str).apply(convert_size)

# Convert 'Last Updated' to datetime
apps_df['Last Updated'] = pd.to_datetime(apps_df['Last Updated'], errors='coerce')

# Ensure 'Rating' is numeric
apps_df['Rating'] = pd.to_numeric(apps_df['Rating'], errors='coerce')

# Ensure 'Reviews' is numeric
apps_df['Reviews'] = pd.to_numeric(apps_df['Reviews'], errors='coerce')

# Ensure 'Installs' is numeric, handling any unexpected values
apps_df['Installs'] = apps_df['Installs'].str.replace('[+,]', '', regex=True)
apps_df['Installs'] = pd.to_numeric(apps_df['Installs'], errors='coerce')

# Filter data based on conditions
filtered_df = apps_df[
    (apps_df['Rating'] >= 4.0) &
    (apps_df['Size'].notna()) & (apps_df['Size'] >= 10) &
    (apps_df['Last Updated'].dt.month == 1)
]

# Get top 10 categories by installs
top_categories = filtered_df.groupby('Category')['Installs'].sum().nlargest(10).index
filtered_df = filtered_df[filtered_df['Category'].isin(top_categories)]

# Aggregate data for plotting
category_stats = filtered_df.groupby('Category').agg(
    {'Rating': 'mean', 'Reviews': 'sum'}
).reset_index()

# Convert IST time
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist).hour

# Only show the graph if the time is between 3 PM – 5 PM IST
if 15 <= current_time < 17:
    fig = px.bar(
        category_stats.melt(id_vars='Category', var_name='Metric', value_name='Value'),
        x='Category',
        y='Value',
        color='Metric',
        title='Comparison of Average Rating and Total Reviews for Top 10 App Categories',
        barmode='group'
    )
    fig.show()
else:
    print("Graph is only visible between 3 PM and 5 PM IST")


