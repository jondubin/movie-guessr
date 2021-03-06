from application import r
from flask import send_file
import requests
from StringIO import StringIO
import tmdbsimple as tmdb
from application import TMDB_KEY, BING_KEY
from bing_search_api import BingSearchAPI

tmdb.API_KEY = TMDB_KEY


def return_from_cache(hash_name, url_fn, key):
    if not key:
        return ""
    key = key.lower()
    cached = r.hget(hash_name, key)
    if cached:
        image = StringIO(cached)
        image.seek(0)
    else:
        image_url = url_fn(key)
        req = requests.get(image_url)
        image = StringIO(req.content)
        image.seek(0)
        r.hset(hash_name, key, image.getvalue())
    return send_file(image, mimetype='image/jpeg')


def get_poster_url(movie_name):
    search = tmdb.Search()
    response = search.movie(query=movie_name)
    if response:
        movie_url = "http://image.tmdb.org/t/p/original" + search.results[0]['poster_path']
    return movie_url


def get_actor_url(actor_name):
    bing = BingSearchAPI(BING_KEY)
    params = {'ImageFilters':'"Face:Face"',
              '$format': 'json',
              '$top': 1,
              '$skip': 0}
    actor_name = actor_name.encode('utf-8')
    data = bing.search('image',
                       actor_name,
                       params).json()
    return data['d']['results'][0]['Image'][0]['Thumbnail']['MediaUrl']
