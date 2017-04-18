from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return """
        <h1>Movie of the Day</h1>
        <ul>
            <li>The Big Lebowski</li>
        </ul>
    """

app.run()
