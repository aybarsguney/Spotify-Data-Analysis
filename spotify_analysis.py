import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# Load the Data
file_path = "spotify_2019.xlsx"
df = pd.read_excel(file_path)

# Handling Missing Values
df = df.dropna()

# Handling Empty Genres and Popularity of 0
df = df[(df['track_genres'].notna()) & (df['track_genres'] != '')]
df = df[df['track_popularity'] != 0]

# Preprocess the Data
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d.%m.%Y')

# Extract month and season
df['month'] = df['timestamp'].dt.month
seasons = {1: 'Winter', 2: 'Winter', 3: 'Spring', 4: 'Spring', 5: 'Spring', 6: 'Summer', 7: 'Summer', 8: 'Summer', 9: 'Fall', 10: 'Fall', 11: 'Fall', 12: 'Winter'}
df['season'] = df['month'].map(seasons)

num_songs_season = df['season'].value_counts()
print("Number of Songs Listened Each Season:")
print(num_songs_season)

# Print the Most Common Genres in Each Season
for season, group in df.groupby('season'):
    most_common_genres = group['track_genres'].value_counts().idxmax()
    print(f"Most common genre in {season}: {most_common_genres}")

# Filter the Top 3 Genres
top_genres = df['track_genres'].value_counts().nlargest(3).index
df_top_genres = df[df['track_genres'].isin(top_genres)]

# Explore the Data and Visualize
plt.figure(figsize=(10, 6))
sns.countplot(x='season', data=df)
plt.title('Distribution of Songs Across Seasons')
plt.show()

plt.figure(figsize=(12, 8))
sns.boxplot(x='season', y='track_popularity', data=df_top_genres, hue='track_genres')
plt.title('Distribution of Track Popularity Across Top 3 Genres and Seasons')
plt.show()

plt.figure(figsize=(10, 6))
sns.countplot(x='season', hue='track_genres', data=df_top_genres)
plt.title('Top 3 Genres Occurrence in Each Season')
plt.show()

# Hypothesis:
# Null Hypothesis (H0): There is no significant evidence that the most common genres remain constant across seasons.
# Alternative Hypothesis (H1): There is evidence that the most common genres change over time seasonally.
contingency_table = pd.crosstab(df_top_genres['season'], df_top_genres['track_genres'])

# Perform Chi-Square Test for Independence
chi2_stat, p_value, _, _ = chi2_contingency(contingency_table)

# Print Results
print("Chi-Square Test Statistic:", chi2_stat)
print("P-value:", p_value)

# Decide whether to accept or reject the null hypothesis
alpha = 0.05  # significance level
if p_value < alpha:
    print("Reject the null hypothesis. There is evidence that the most common genres change over time seasonally.")
else:
    print("Fail to reject the null hypothesis. There is no significant evidence that the most common genres change over time seasonally.")









