#1
import pandas as pd
import plotly.express as px

# Load the dataset
apps_df = pd.read_csv('googleplaystore.csv')
reviews_df = pd.read_csv('googleplaystore_user_reviews.csv')

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
fig = px.bar(
    sentiment_counts,
    x='Rating_Group',
    y='Count',
    color='Sentiment',
    facet_col='Category',
    title='Sentiment Distribution by Rating Group for Top 5 App Categories',
    barmode='stack'
)
fig.show()

