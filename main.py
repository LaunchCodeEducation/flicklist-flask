from flask import Flask
import random
import datetime

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too

@app.route("/")
def index():
    # choose a movie by invoking our new function
    movie = get_random_movie()

    # build the response string
    content = "<h1>Movie of the Day</h1>"
    content += "<ul>"
    content += "<li>" + movie + "</li>"
    content += "</ul>"

    # TODO: pick another random movie, and display it under
    # the heading "<h1>Tommorrow's Movie</h1>"
    movie = get_random_movie()
    content += "<h1>Tommorrow's Movie</h1>"
    content += "<ul>"
    content += "<li>" + movie + "</li>"
    content += "</ul>"

    return content

 # TODO: make a list with at least 5 movie titles 
movie_list = [
        "The Big Lebowski",
        "Mulan",
        "Hot Fuzz",
        "Fargo",
        "Little Women"
        ]
def get_random_movie():
    random_movie = random.choice(movie_list)

    # TODO: randomly choose one of the movies, and return it
    return random_movie


app.run()
