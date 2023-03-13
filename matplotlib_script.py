import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('stephen_king_book_rankings.csv')

# Create a scatter plot with the publication date on the x-axis and the book rating on the y-axis
plt.scatter(df['Date published'], df['Average rating'])

# Label each data point with the book title
for i, row in df.iterrows():
    plt.annotate(row['Title'], xy=(row['Date published'], row['Average rating']), xytext=(5, 5), textcoords='offset points', fontsize=8)

# Set the x-axis label and rotate the x-tick labels for better visibility
plt.xlabel('Publication date')
plt.xticks(rotation=90)

# Set the y-axis label
plt.ylabel('Book rating')

# Show the plot
plt.show()