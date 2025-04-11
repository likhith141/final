#3
import pandas as pd
import plotly.express as px
import datetime
import pytz

# Load the dataset (Ensure you have the Google Playstore dataset)
df = pd.read_csv("googleplaystore14.csv")  # Replace with actual dataset path

# Convert IST timezone and check time restriction
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.datetime.now(ist).time()
allowed_start = datetime.time(18, 0)
allowed_end = datetime.time(20, 0)

if allowed_start <= current_time <= allowed_end:
    # Data Preprocessing
    # Exclude categories starting with 'A', 'C', 'G', or 'S'
    df = df[['Category', 'Installs', 'Country']].dropna()
    df['Installs'] = df['Installs'].astype(str).str.replace(r'[^\d]', '', regex=True)
    df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce').fillna(0).astype(int)

    
    df = df[~df['Category'].str.startswith(('A', 'C', 'G', 'S'))]
    
    # Get top 5 categories based on total installs
    top_categories = df.groupby('Category')['Installs'].sum().nlargest(5).index
    df = df[df['Category'].isin(top_categories)]
    
    # Aggregate installs by country and category
    df_grouped = df.groupby(['Country', 'Category'])['Installs'].sum().reset_index()
    df_grouped['Highlight'] = df_grouped['Installs'] > 1_000_000  # Highlight installs > 1M
    
    # Create Choropleth Map
    fig = px.choropleth(
        df_grouped,
        locations="Country",
        locationmode="country names",
        color="Category",
        hover_data=["Installs"],
        title="Global Installs by Category (Filtered)"
    )
    
    fig.show()
else:
    print("The visualization is only available between 6 PM and 8 PM IST.")
