from flask import Flask, request, redirect
import cgi

app = Flask(__name__)

page_header = """
<!DOCTYPE html>
<html>
    <head>
        <title>FlickList</title>
    </head>
    <body>
        <h1>FlickList</h1>
"""

page_footer = """
    </body>
</html>
"""

# a list of movies that nobody should have to watch
terrible_movies = [
    "Gigli",
    "Star Wars Episode 1: Attack of the Clones",
    "Paul Blart: Mall Cop 2",
    "Nine Lives",
    "Starship Troopers"
]

def getCurrentWatchlist():
    # For now, we are just pretending
    # returns user's current watchlist
    return [ "Star Wars", "Minions", "Freaky Friday", "My Favorite Martian" ]



@app.route("/crossoff", methods=['POST'])
def crossoffMovie():
    crossed_off_movie = request.form['crossed-off-movie']

    if (crossed_off_movie in getCurrentWatchlist()) == False:
        # the user tried to cross off a movie that isn't in their list,
        # so we redirect back to the front page and tell them what went wrong
        error = "'{0}' is not in your Watchlist, so you can't cross it off!".format(crossed_off_movie)

        # redirect to homepage, and include error as a query parameter in the URL
        return redirect("/?error=" + error)

    # if we didn't redirect by now, then all is well
    crossed_off_movie_element = "<strike>" + crossed_off_movie + "</strike>"
    confirmation = crossed_off_movie_element + " has been crossed off your Watchlist."
    content = page_header + "<p>" + confirmation + "</p>" + page_footer

    return content


@app.route("/add", methods=['POST'])
def addMovie():
    # look inside the request to figure out what the user typed
    new_movie = request.form['new-movie']

    # if the user typed nothing at all, redirect and tell them the error
    if (not new_movie) or (new_movie.strip() == ""):
        error = "Please specify the movie you want to add."
        return redirect("/?error=" + cgi.escape(error, quote=True))

    # if the user wants to add a terrible movie, redirect and tell them the error
    if new_movie in terrible_movies:
        error = "Trust me, you don't want to add '{0}' to your Watchlist".format(new_movie)
        return redirect("/?error=" + cgi.escape(error, quote=True))

    # 'escape' the user's input so that if they typed HTML, it doesn't mess up our site
    new_movie_escaped = cgi.escape(new_movie, quote=True)

    # build response content
    new_movie_element = "<strong>" + new_movie_escaped + "</strong>"
    sentence = new_movie_element + " has been added to your Watchlist!"
    content = page_header + "<p>" + sentence + "</p>" + page_footer

    return content


@app.route("/")
def index():
    edit_header = "<h2>Edit My Watchlist</h2>"

    # a form for adding new movies
    add_form = """
        <form action="/add" method="post">
            <label>
                I want to add
                <input type="text" name="new-movie"/>
                to my watchlist.
            </label>
            <input type="submit" value="Add It"/>
        </form>
    """

    # a form for crossing off watched movies
    # (first we build a dropdown from the current watchlist items)
    crossoff_options = ""
    for movie in getCurrentWatchlist():
        crossoff_options += '<option value="{0}">{0}</option>'.format(movie)

    crossoff_form = """
        <form action="/crossoff" method="post">
            <label>
                I want to cross off
                <select name="crossed-off-movie"/>
                    {0}
                </select>
                from my watchlist.
            </label>
            <input type="submit" value="Cross It Off"/>
        </form>
    """.format(crossoff_options)

    # if we have an error, make a <p> to display it
    error = request.args.get("error")
    if error:
        error_esc = cgi.escape(error, quote=True)
        error_element = '<p class="error">' + error_esc + '</p>'
    else:
        error_element = ''

    # combine all the pieces to build the content of our response
    main_content = edit_header + add_form + crossoff_form + error_element


    # build the response string
    content = page_header + main_content + page_footer

    return content


app.run()
