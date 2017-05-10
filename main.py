from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flicklist:MyNewPass@localhost:8889/flicklist'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __repr__(self):
        return '<User %r>' % self.email

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    watched = db.Column(db.Boolean)
    rating = db.Column(db.String(5))

    def __init__(self, name):
        self.name = name
        self.watched = False

    def __repr__(self):
        return '<Movie %r>' % self.name

# a list of movie names that nobody should have to watch
terrible_movies = [
    "Gigli",
    "Star Wars Episode 1: Attack of the Clones",
    "Paul Blart: Mall Cop 2",
    "Nine Lives",
    "Starship Troopers"
]

def getCurrentWatchlist():
    return Movie.query.filter_by(watched=False).all()

def getWatchedMovies():
    return Movie.query.filter_by(watched=True).all()

# TODO 3: Add "/login" GET and POST routes.
# TODO 4: Create login template with username and password.
#         Notice that we've already created a 'login' link in the upper-right corner of the page that'll connect to it.

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not isEmail(email):
            flash('zoiks! "' + email + '" does not seem like an email address')
            return redirect('/register')
        # TODO 1: validate that form value of 'verify' matches password
        # TODO 2: validate that there is no user with that email already
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.email
        return redirect("/")
    else:
        return render_template('register.html')

def isEmail(string):
    # for our purposes, an email string has an '@' followed by a '.'
    # there is an embedded language called 'regular expression' that would crunch this implementation down
    # to a one-liner, but we'll keep it simple:
    atsign_index = string.find('@')
    atsign_present = atsign_index >= 0
    if not atsign_present:
        return False
    else:
        domain_dot_index = string.find('.', atsign_index)
        domain_dot_present = domain_dot_index >= 0
        return domain_dot_present

@app.route("/logout", methods=['POST'])
def Logout():
    del session['user']
    return redirect("/")

# Create a new route called RateMovie which handles a POST request on /rating-confirmation
@app.route("/rating-confirmation", methods=['POST'])
def RateMovie():
    movie_id = request.form['movie_id']
    rating = request.form['rating']

    movie = Movie.query.get(movie_id)
    if not movie:
        # the user tried to rate a movie that isn't in their list,
        # so we redirect back to the front page and tell them what went wrong
        error = "'{0}' is not in your Watchlist, so you can't cross it off!".format(movie)

        # redirect to homepage, and include error as a query parameter in the URL
        return redirect("/?error=" + error)

    # if we didn't redirect by now, then all is well
    movie.rating = rating
    db.session.commit()
    return render_template('rating-confirmation.html', movie=movie, rating=rating)


@app.route("/ratings", methods=['GET'])
def MovieRatings():
    return render_template('ratings.html', movies = getWatchedMovies())


@app.route("/watched-it", methods=['POST'])
def watchMovie():
    watched_movie_id = request.form['watched-movie']

    watched_movie = Movie.query.get(watched_movie_id)
    if not watched_movie:
        return redirect("/?error=Attempt to watch a movie unknown to this database")

    # if we didn't redirect by now, then all is well
    watched_movie.watched = True
    db.session.commit()
    return render_template('watched-it.html', watched_movie=watched_movie)

@app.route("/add", methods=['POST'])
def addMovie():
    # look inside the request to figure out what the user typed
    new_movie_name = request.form['new-movie']

    # if the user typed nothing at all, redirect and tell them the error
    if (not new_movie_name) or (new_movie_name.strip() == ""):
        error = "Please specify the movie you want to add."
        return redirect("/?error=" + error)

    # if the user wants to add a terrible movie, redirect and tell them the error
    if new_movie_name in terrible_movies:
        error = "Trust me, you don't want to add '{0}' to your Watchlist".format(new_movie_name)
        return redirect("/?error=" + error)

    movie = Movie(new_movie_name)
    db.session.add(movie)
    db.session.commit()
    return render_template('add-confirmation.html', movie=movie)

@app.route("/")
def index():
    encoded_error = request.args.get("error")
    return render_template('edit.html', watchlist=getCurrentWatchlist(), error=encoded_error and cgi.escape(encoded_error, quote=True))

# TODO 5: modify this function to rely on a list of endpoints that users can visit without being redirected.
#         It should contain 'register' and 'login'.
@app.before_request
def requireLogin():
    if not ('user' in session or request.endpoint == 'register'):
        return redirect("/register")

# In a real application, this should be kept secret (i.e. not on github)
# As a consequence of this secret being public, I think connection snoopers or
# rival movie sites' javascript could hijack our session and act as us,
# perhaps giving movies bad ratings - the HORROR.
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RU'

if __name__ == "__main__":
    app.run()
