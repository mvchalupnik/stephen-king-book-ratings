import requests
from bs4 import BeautifulSoup
import csv

# Define the URL of the page that contains Stephen King's books on Goodreads.com
url = 'https://www.goodreads.com/author/show/3389.Stephen_King'

# Send a request to the URL and get the HTML response
response = requests.get(url)

# Parse the HTML response with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table that contains Stephen King's books
table = soup.find('table', {'class': 'tableList'})

# Initialize an empty list to store the book rankings
book_rankings = []

# Loop through each row in the table, skipping the first row (header row)
for row in table.find_all('tr')[1:]:
    # Get the book title and URL from the first column in the row
    title = row.find('a', {'class': 'bookTitle'}).text.strip()
    book_url = 'https://www.goodreads.com' + row.find('a', {'class': 'bookTitle'})['href']

    # Send a request to the book's URL and get the HTML response
    book_response = requests.get(book_url)

    # Parse the HTML response with BeautifulSoup
    book_soup = BeautifulSoup(book_response.text, 'html.parser')

    # Find the element that contains the book's average rating
    rating_element = book_soup.find('span', {'itemprop': 'ratingValue'})

    # If the element exists, get the rating and append it to the list of rankings
    if rating_element:
        rating = rating_element.text.strip()
        book_rankings.append((title, rating))

# Sort the list of rankings by descending order of rating
book_rankings.sort(key=lambda x: float(x[1]), reverse=True)

# Write the rankings to a CSV file
with open('stephen_king_book_rankings.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Title', 'Average rating'])
    for title, rating in book_rankings:
        writer.writerow([title, rating])