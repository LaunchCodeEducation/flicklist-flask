from flask import Flask

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

    return content

def get_random_movie():
    # TODO: make a list with at least 5 movie titles
    # TODO: randomly choose one of the movies, and return it
    return "The Big Lebowski"


app.run()
