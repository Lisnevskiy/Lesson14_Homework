from flask import Flask, request

from utils import find_movie_by_title, find_by_range, \
    search_movies_by_genre, search_by_rating, find_by_cast

app = Flask(__name__)


@app.route('/movie/<title>')
def find_movie(title):
    return find_movie_by_title(title)


@app.route('/movie/year/to/year')
def find_by_year():
    fy = request.args['fy']
    sy = request.args['sy']
    return find_by_range(fy, sy)


@app.route('/rating/children')
def find_by_rating_children():
    return search_by_rating(('G'))


@app.route('/rating/family')
def find_by_rating_family():
    return search_by_rating(('G', 'PG', 'PG-13'))


@app.route('/rating/adult')
def find_by_rating_adult():
    return search_by_rating(('R', 'NC-17'))


@app.route('/genre/<genre>')
def find_by_genre(genre):
    return search_movies_by_genre(genre)


@app.route('/cast/<actor1>/<actor2>')
def find_by_actors(actor1, actor2):
    return find_by_cast(actor1, actor2)


if __name__ == '__main__':
    app.run(debug=True)
