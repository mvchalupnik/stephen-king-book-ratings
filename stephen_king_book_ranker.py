import requests
from bs4 import BeautifulSoup
import csv
import re

import pandas as pd
import plotly.express as px
import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sns

"""
This file contains functions which will:
- generate a CSV of Stephen King's bibliography of books from Wikipedia (only including novels and short story collections)
- generate a CSV of Stephen King's bibliography from Goodreads including three columns (title, average rating, and year published)
- plot and perform a linear regression of average rating vs year using matplotlib
- plot and perform a linear regression of average rating vs year using plotly
"""


def generate_bibliography_from_wikipedia(bibliography_file_name):
    """ Generate a CSV of Stephen King's bibliography of books from Wikipedia
    (only including novels and short story collections)

    :param csv_file_name: string to save CSV to
    """

    # Initialize a list to store the book rankings
    books = []

    def add_books(url, books):
        # Send a request to the URL and get the HTML response
        response = requests.get(url)

        # Parse the HTML response with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table that contains Stephen King's books
        tables = soup.find_all('table', {'class': 'wikitable sortable'})

        # The first two tables contain the novels and short story collections
        # which are what we are interested in
        for table in tables[0:2]:
            # Loop through each element under column 1 of the table
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                for cell in cells:
                    # Get the book title and URL from the first column in the row
                    cell_contents = cell.find('a').text.strip()

                    if not cell_contents.isnumeric():
                        # Strip any words before a colon
                        match = re.search(r'(?<=: ).*', cell_contents)
                        if match:
                           cell_contents = match.group(0)

                        # Replace 'and' with '&' where needed
                        cell_contents = cell_contents.replace(' & ', ' and ')

                        # Add to the list and break out of loop
                        books.append((cell_contents))
                        break

    # Add books by Stephen King from wikipedia page to books list
    url = f'https://en.wikipedia.org/wiki/Stephen_King_bibliography'
    add_books(url=url, books=books)

    # Write the list of books to a CSV file
    with open(bibliography_file_name + '.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for book in books:
            writer.writerow([book])


def generate_rating_list_from_goodreads(bibliography_file_name, csv_file_name):
    """ generate a CSV of Stephen King's bibliography from Goodreads including three columns
    (title, average rating, and year published)
    
    :param bibliography_file_name: file name containing the CSV with the full bibliography of 
           Stephen King's novels and short story collections
    :param csv_file_name: file name to save a CSV with the title of each of Stephen King's
           books, the average rating on Goodreads, and the year the book was published
    """

    # Initialize a dict to store the book rankings
    books = {}

    # Initialize empty set to store the book titles
    stephen_king_bibliography = set(())

    # Load in a saved CSV of all of Stephen King's books
    with open(bibliography_file_name + '.csv', 'r') as file:
        for title in csv.reader(file):
            stephen_king_bibliography.add(title[0].rstrip('"').lstrip('"'))

    def add_books(url, books):
        # Send a request to the URL and get the HTML response
        response = requests.get(url)

        # Parse the HTML response with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table that contains Stephen King's books
        table = soup.find('table', {'class': 'tableList'})

        # Loop through each table row element (tr) in the table
        for row in table.find_all('tr'):
            # Get the book title and URL from the first column in the row
            cell = row.find('a', {'class': 'bookTitle'}).text.strip()

            # Strip off quotation marks, if present
            cell = cell.lstrip('"').rstrip('"')

            # Get rid of parentheses and anything inside
            cells = cell.split(' (')
            title = cells[0]

            # Don't add book titles that are not part of the set of Stephen King's books from Wikipedia
            if title not in stephen_king_bibliography:
                continue

            # Get the book rating
            book_info = row.find('span', class_='greyText smallText uitext').text.strip()
            match = re.search(r'(\d+\.\d+) avg rating', book_info)
            if match is None:
                continue
            rating = float(match.group(1))

            # Get the book publication date
            match = re.search(r'published\s*(\d{4})', book_info)
            if match is None:
                continue
            year_published = int(match.group(1))

            # Get the number of ratings
            match = re.search(r'([\d,]+) ratings', book_info)
            if match is None:
                continue
            number_of_ratings = int(match.group(1).replace(',', ''))

            # If the title already exists in our list, create a weighted average of the rating
            # and don't add a duplicate identical title
            if title in books:
                rating_copy, year_published_copy, number_of_ratings_copy = books[title]
                rating = (rating * number_of_ratings + rating_copy * number_of_ratings_copy) / (number_of_ratings + number_of_ratings_copy)

            # Don't include spam book entries with less than 12,000 ratings
            if number_of_ratings < 12000:
                continue

            # Append the title, rating, and year published
            books[title] = ((rating, year_published, number_of_ratings))

    # Add books by Stephen King
    for page_number in range(1,5):
        url = f'https://www.goodreads.com/author/list/3389.Stephen_King?page={page_number}&per_page=30'
        add_books(url, books)

    # Add books by Richard Bachman (Stephen King's pseudonym)
    for page_number in range(1,2):
        url = f'https://www.goodreads.com/author/list/5858.Richard_Bachman?page={page_number}&per_page=30'
        add_books(url, books)

    # Write the rankings to a CSV file
    with open('stephen_king_book_rankings.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Average rating', 'Date published'])
        for title, (rating, year_published, number_of_ratings) in books.items():
            writer.writerow([title, rating, year_published])


def plot_with_matplotlib(csv_name, plot_file_name):
    """ Plot and perform a linear regression of average rating vs year using matplotlib. Save
    plot to png file.

    :param csv_name: string of the csv file containing Stephen King book titles, average Goodreads
                     ratings, and years published
    :param plot_file_name: string with file name to save plot to
    """

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_name + '.csv')

    # Create a scatter plot with the publication date on the x-axis and the book rating on the y-axis
    plt.scatter(df['Date published'], df['Average rating'])

    # Label each data point with the book title
    texts = []
    for i, row in df.iterrows():
        texts = plt.annotate(row['Title'], xy=(row['Date published'], row['Average rating']), xytext=(3, 3), textcoords='offset points', fontsize=8)

    # Set the x-axis label and rotate the x-tick labels for better visibility
    plt.xlabel('Publication date')
    plt.xticks(rotation=90)

    # Set the y-axis label
    plt.ylabel('Book rating')

    # Fit a linear regression through the data
    X = df['Date published'].values.reshape(-1, 1)
    y = df['Average rating'].values.reshape(-1, 1)
    model = LinearRegression().fit(X, y)
    plt.plot(X, model.predict(X), color='red')

    # Save plot
    plt.savefig(plot_file_name + ".png")


def plot_with_plotly(csv_name, plot_file_name):
    """ Plot and perform a linear regression of average rating vs year using plotly, save plot to HTML

    :param csv_name: string of the csv file containing Stephen King book titles, average Goodreads
                     ratings, and years published
    :param plot_file_name: string with file name to save plot to
    """

    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(csv_name + '.csv')

    # Create a scatter plot of the data, with publication year on the x-axis and rating on the y-axis
    fig = px.scatter(df, x='Date published', y='Average rating', hover_data=['Title'], labels=['Title'],
                    title='Stephen King Book Ratings')

    # calculate the linear regression line
    x = df['Date published']
    y = df['Average rating']
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    line = slope * x + intercept

    # add the linear regression line to the figure
    fig.add_trace(px.line(x=x, y=line, color_discrete_sequence=['darksalmon'], title='Linear Regression').data[0])

    # Save the plot to an HTML file
    fig.write_html(plot_file_name + ".html")
