# On Windows:
# export FLASK_APP=hello.py
# Might have to use "set FLASK_APP=hello.py" if there is a problem with export
# flask run

from flask import Flask
app = Flask(__name__)

@app.route('/')  # The website for the app.
def hello_world():
    return 'Hello, World!'

@app.route('/new_page')  # The website for the app.
def new_page():
    return 'This is another page'

# If you add this, you can run the flask 

