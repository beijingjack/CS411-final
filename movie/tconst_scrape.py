import pandas as pd
from requests import get
from bs4 import BeautifulSoup
import unicodedata

def findMovie(arr):
    headers = {"Accept-Language": "en-US, en;q=0.5"}
    pages = [str(i) for i in range(1,2)]
    years_url = [str(i) for i in range(2010,2018)]
    # Redeclaring the lists to store data in
    names = []
    years = []
    imdb_ratings = []
    metascores = []
    votes = []



    # For every year in the interval 2000-2017
    for m in arr:
            response = get('http://www.imdb.com/title/' + m, headers = headers)
            # Parse the content of the request with BeautifulSoup
            page_html = BeautifulSoup(response.text, 'html.parser')

            container = page_html.find('div', class_ = 'title_wrapper')

            # Scrape the name
            title = str(container.h1.text)
            name = unicodedata.normalize("NFKD", title.split('(')[0])
            names.append(name)

            # Scrape the year
            year = title.split('(')[1][:-2]
            years.append(year)

            # Scrape the IMDB rating
            imdb = page_html.find('div', class_ = 'ratingValue').span.text
            imdb_ratings.append(imdb)


            # Scrape the number of votes
            vote = (page_html.find('div', class_ = 'imdbRating').a.text)
            votes.append(vote)

    movie_ratings = {'movie': names,
                                  'year': years,
                                  'imdb': imdb_ratings,
                                  'votes': votes}
    return movie_ratings
