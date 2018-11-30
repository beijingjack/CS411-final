import pandas as pd
from requests import get
from bs4 import BeautifulSoup
import unicodedata

def findMovie(arr):
    headers = {"Accept-Language": "en-US, en;q=0.5"}
    movie_ratings = {}


    # For every year in the interval 2000-2017
    for m in arr:
            response = get('http://www.imdb.com/title/' + m, headers = headers)
            # Parse the content of the request with BeautifulSoup
            page_html = BeautifulSoup(response.text, 'html.parser')

            container = page_html.find('div', class_ = 'title_wrapper')

            # Scrape the name
            title = str(container.h1.text)
            name = unicodedata.normalize("NFKD", title.split('(')[0])

            # Scrape the year
            year = title.split('(')[1][:-2]

            # Scrape the IMDB rating
            imdb = page_html.find('div', class_ = 'ratingValue').span.text


            # Scrape the number of votes
            vote = (page_html.find('div', class_ = 'imdbRating').a.text)

            movie_ratings[m] = {'movie': name,
                             'year': year,
                             'rating': imdb,
                             'votes': vote}

    return movie_ratings
