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

def get_current_watchlist():
    # returns user's current watchlist--hard coded for now
    return [ "Star Wars", "Minions", "Freaky Friday", "My Favorite Martian" ]

# TODO: 
# Modify "My Watchlist" so that you eliminate the need for the "crossoff" form in edit.html. 
# Now, next to every list item/movie listed in "My Watchlist" you should display a button that says "I Watched it!". 
# Clicking the button will result in a confirmation message that the movie has been watched. 
# So you'll need to add a form within the <li> tags of "My Watchlist"
# Once this is done, delete the "crossoff" form in edit.html

# TODO:
# Make a ratings.html template which lists all movies that have been crossed off.
# It should have a header of <h2>Movies I Have Watched</h2>
# Add a form for rating EACH list item/movie using a <select> dropdown with the options/values
# in this list: ["How was it?", "*", "**", "***", "****", "*****"]
# And with a button that says "Rate It!" to submit the user's rating.
# Give this form the action of "/rating-confirmation" and the method of post.

# TODO: 
# Add a function, movie_ratings, to handle a get request and render the template at "/ratings"

# TODO:
# Add a function, get_watched_movies, to get the list of crossed off movies. 
# For now, create a hard-coded list with a few movie titles. 

# TODO:
# Make a rating-confirmation.html template, to be displayed when the user rates a movie 
# they have crossed off. 

# TODO: 
# create a rate_movie function that handles a post request on /rating-confirmation and 
# renders the `rating-confirmation` template.

@app.route("/crossoff", methods=['POST'])
def crossoff_movie():
    crossed_off_movie = request.form['crossed-off-movie']

    if crossed_off_movie not in get_current_watchlist():
        # the user tried to cross off a movie that isn't in their list,
        # so we redirect back to the front page and tell them what went wrong
        error = "'{0}' is not in your Watchlist, so you can't cross it off!".format(crossed_off_movie)

        # redirect to homepage, and include error as a query parameter in the URL
        return redirect("/?error=" + error)

    # if we didn't redirect by now, then all is well
    return render_template('crossoff.html', crossed_off_movie=crossed_off_movie)

@app.route("/add", methods=['POST'])
def add_movie():
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

    return render_template('add-confirmation.html', movie=new_movie)


@app.route("/")
def index():
    encoded_error = request.args.get("error")
    return render_template('edit.html', watchlist=get_current_watchlist(), error=encoded_error and cgi.escape(encoded_error, quote=True))

app.run()

