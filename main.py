from stephen_king_book_ranker import generate_bibliography_from_wikipedia,\
									generate_rating_list_from_goodreads,\
									plot_with_matplotlib, plot_with_plotly



# Generate Stephen King bibliography from Wikipedia and save to CSV
bibliography_file_name = 'stephen_king_bibliography'
generate_bibliography_from_wikipedia(bibliography_file_name=bibliography_file_name)

# Generating CSV of average ratings of Stephen King books from Goodreads
csv_file_name = 'stephen_king_book_rankings'
generate_rating_list_from_goodreads(bibliography_file_name=bibliography_file_name,
									csv_file_name=csv_file_name)

# Plot ratings against year using matplotlib
plot_fname = 'stephen_king_books'
plot_with_matplotlib(csv_name=csv_file_name, plot_file_name=plot_fname)

# Plot ratings against year using plotly
plot_with_plotly(csv_name=csv_file_name, plot_file_name=plot_fname)
