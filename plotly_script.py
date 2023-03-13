import pandas as pd
import plotly.express as px

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv('stephen_king_ratings.csv')

# Create a scatter plot of the data, with publication year on the x-axis and rating on the y-axis
fig = px.scatter(df, x='year', y='rating', hover_data=['title'], title='Stephen King Book Ratings')

# Show the plot
fig.show()