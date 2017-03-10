#!/usr/bin/env python
import datetime
import os
import sys
import time

from RatS.utils import file_impex
from RatS.inserters.movielense_inserter import MovielenseInserter
from RatS.parsers.imdb_parser import IMDBRatingsParser

TIMESTAMP = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
EXPORTS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'RatS', 'exports'))
JSON_FILE = TIMESTAMP + '_imdb.json'


def main():
    # PARSING DATA
    movies = parse_data_from_source(IMDBRatingsParser())
    # FILE LOADING
    # movies = load_data_from_file('20170224211816_imdb.json')
    # POSTING THE DATA
    insert_movie_ratings(MovielenseInserter(), movies)


def parse_data_from_source(parser):
    movies = parser.parse()
    file_impex.save_movies_json(movies, folder=EXPORTS_FOLDER, filename=JSON_FILE)
    sys.stdout.write('\r\n===== %s: saved %i parsed movies to %s/%s\r\n' %
                     (type(parser.site).__name__, len(movies), EXPORTS_FOLDER, JSON_FILE))
    sys.stdout.flush()
    return movies


def load_data_from_file(filename):
    movies = file_impex.load_movies_json(folder=EXPORTS_FOLDER, filename=filename)
    sys.stdout.write('\r\n===== loaded %i movies from %s/%s\r\n' % (len(movies), EXPORTS_FOLDER, filename))
    sys.stdout.flush()
    return movies


def insert_movie_ratings(inserter, movies):
    inserter.insert(movies)


if __name__ == "__main__":
    main()