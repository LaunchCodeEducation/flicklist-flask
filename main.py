from flask import Flask
import random

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

    # build the response string
    content = page_header + edit_header + add_form + page_footer

    return content

def getRandomMovie():
    return random.choice(["The Big Lebowski", "The Royal Tenenbaums", "Princess Mononoke", "The Princess Bride", "Star Trek IV: The Voyage Home"])


app.run()
