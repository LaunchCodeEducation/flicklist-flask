from flask import Flask, request, redirect, render_template
import cgi

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too

# a list of movies that nobody should have to watch
terrible_movies = [
    "Gigli",
    "Star Wars Episode 1: Attack of the Clones",
    "Paul Blart: Mall Cop 2",
    "Nine Lives",
    "Starship Troopers"
]

def getCurrentWatchlist():
    # returns user's current watchlist--hard coded for now
    return [ "Star Wars", "Minions", "Freaky Friday", "My Favorite Martian" ]


@app.route("/crossoff", methods=['POST'])
def crossoff_movie():
    crossed_off_movie = request.form['crossed-off-movie']

    if crossed_off_movie not in getCurrentWatchlist():
        # the user tried to cross off a movie that isn't in their list,
        # so we redirect back to the front page and tell them what went wrong
        error = "'{0}' is not in your Watchlist, so you can't cross it off!".format(crossed_off_movie)

        # redirect to homepage, and include error as a query parameter in the URL
        return redirect("/?error=" + error)

    # if we didn't redirect by now, then all is well
    return render_template('crossoff.html', crossed_off_movie=crossed_off_movie)

@app.route("/add", methods=['POST'])
def addMovie():
    # look inside the request to figure out what the user typed
    new_movie = request.form['new-movie']

    # if the user typed nothing at all, redirect and tell them the error
    if (not new_movie) or (new_movie.strip() == ""):
        error = "Please specify the movie you want to add."
        return redirect("/?error=" + error)

    # if the user wants to add a terrible movie, redirect and tell them the error
    if new_movie in terrible_movies:
        error = "Trust me, you don't want to add '{0}' to your Watchlist".format(new_movie)
        return redirect("/?error=" + error)

    # 'escape' the user's input so that if they typed HTML, it doesn't mess up our site
    new_movie_escaped = cgi.escape(new_movie, quote=True)

    # TODO:
    # Use a template to render the confirmation message
    return "Confirmation Message Under Construction..."

# TODO:
# Modify the edit.html file to display the watchlist in an unordered list with bullets in front of each movie.
# Put the list between "Flicklist" and "Edit My Watchlist" under <h3>My Watchlist</h3>

# TODO:
# Change getCurrentWatchlist to return []. This simulates a user with an empty watchlist.
# Modify edit.html to make sense in such a situation:
#  First: Hide the <h3>My Watchlist</h3> and it's unordered list.
#  Second: Hide the crossoff form, since there are no movies to cross off. 

@app.route("/")
def index():
    encoded_error = request.args.get("error")
    return render_template('edit.html', watchlist=getCurrentWatchlist(), error=encoded_error and cgi.escape(encoded_error, quote=True))

app.run()
