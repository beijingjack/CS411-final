import json
import pprint
from selenium import webdriver

def get_nth_key(dictionary, n=0):
    if n < 0:
        n += len(dictionary)
    for i, key in enumerate(dictionary.keys()):
        if i == n:
            return key
    raise IndexError("dictionary index out of range")


def get_html(theater):
    return theater.get_attribute('innerHTML')

def get_movie_by_thea(theater):
    movie_names = []
    names = theater.find_elements_by_xpath(".//div[@class = 'fd-movie__details']")
    for name in names:
        movie_names.append(name.text)

    movies = dict.fromkeys(movie_names)
    times = theater.find_elements_by_xpath(".//ul[@class = 'fd-movie__showtimes']")

    i = 0
    for time in times:
        available_times = time.find_elements_by_xpath(".//ol[@class = 'fd-movie__btn-list']")
        all_times = ''
        for each in available_times:
            all_times += " " + each.text
        movies[get_nth_key(movies,i)] = all_times
        i += 1
    return movies

def printitems(dictObj, indent=0):
    p=[]
    p.append('<ul>\n')
    for k,v in dictObj.iteritems():
        if isinstance(v, dict):
            p.append('<li>'+ k+ ':')
            p.append(printitems(v))
            p.append('</li>')
        else:
            p.append('<li>'+ k+ ':'+ v+ '</li>')
    p.append('</ul>\n')
    return '\n'.join(p)

def findmovie():
    wd = webdriver.Chrome()
    wd.get("https://www.fandango.com/61801_movietimes?mode=general&q=61801")

    #First get all the theaters in one zip code
    theaters = wd.find_elements_by_xpath("//li[@class = 'fd-theater']")
    theater_names = []
    for theater in theaters:
        theater_names.append(theater.find_element_by_xpath(".//div[@class = 'fd-theater__name-wrap']").text)

    #The final dictionary which include all movies by theater
    movies_by_thea = dict.fromkeys(theater_names)

    i = 0
    for theater in theaters:
        movies_by_thea[theater_names[i]] = get_movie_by_thea(theater)
        i += 1

    # with open('movies_by_zip.json', 'w') as fp:
    #     json.dump(movies_by_thea, fp)
    #

    return movies_by_thea;

