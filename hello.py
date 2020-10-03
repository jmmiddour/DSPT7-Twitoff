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

# If you add this, you can run the flask app as:
# `python hello.py` in the terminal
# This only works well if you have a one file app.
# Not useful for multi file being ran as a package.
if __name__ == '__main__':
    app.run(debug=True) 
# If debug=True it will restart the Flask app automatically 
#    when you save the .py file.
