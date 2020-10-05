# Module 1:
## Start up:
- Create and clone a new Github repository.
- Create pip environment with the following code:
    `pipenv --python 3.8`
- Install Flask and Flask-SQLAlchemy in pip environment:
    `pipenv install Flask Flask-SQLAlchemy`
- Activate my pipenv shell:
    `pipenv shell`

## Create a Mininum Flask Application:
First file to create is `hello.py` with some simple code to confirm that I have Flask installed correctly.

- To run the Flask app on Mac:
    - `FLASK_APP=hello.py flask run`
- To run the Flask app on Windows:
    - `export FLASK_APP=hello.py` or `set FLASK_APP=hello.py` (depends on terminal running in)
    - `flask run`

The code `@app.route('/')` is the route or endpoint for the home page/directory of your website that the Flask app is running on.

Create another page by using this code instead `@app.route('/new_page')` and just replace new_page with what you want the endpoint to be.

As long as you have Flask running in your terminal, you will see all interactions with that route and if there were any errors that occured.

Error Codes and what they mean:
- 100's = Information
- 200's = Successful - Everything happened as it was suposed to.
- 300's = Redirect
- 400's = Client Error - You went to a route that doesn't exist.
- 500's = Server Error - Correct route but when processed threw an error.

Under the `@app.route` code you will define the function that you want the app to preform.

## Create the app package:
- Create a new folder and name the folder what you want the module name to be.
- Create the `__init__.py` file. Can initialize the core application in this file.
  - If you initialize the core app in the `__init__.py` file, you would be able to run the Flask packge by runing the following code in the terminal:
    `export FLASK_APP=twitoff:APP` then `flask run`
- Create `app.py` for the majority of the core funtionality.
  - All the configuration code for the app will go in this file.
- Create `db_model.py` to tie a database to the app.
  - This is where you will add the code create your database and tables.

## Using Flask to create and make entries in your DB file:
Once you have your `__init__.py`, `app.py`, and `db_model.py` all setup it is time to create your database and add some toy data to it using your Flask app.
- From the terminal run the following codes:
  - `flask shell` opens a shell similar to the python shell.
  - `from twitoff.db_model import DB, User, Tweet` 
  - `dir(DB)` gives you the directory of everything in your DB package.
  - `DB` will give you the location of your database.
  - `DB.create_all()` will create your database and tables as defined in `db_model.py`.
  - `u1 = User(username='some user', followers='num of followers')` now adds this information to a variable which can then be called by imputting `u1`.
  - `DB.session.add(u1)` will add `u1` user to the "staging area" to be added to the database.
  - `DB.session.commit(u1)` will save this new user to the database.

How to create new tweets in the Tweet table:
- From the terminal run the following codes:
  - `flask shell` opens a shell similar to the python shell.
  - `from twitoff.db_model import DB, User, Tweet`
  - `tweet1 = Tweet(tweet='Sample tweet #awesome!', user=u1)` if you already have `u1` in the memory of the flask shell you are currently in.
  - If you are just entering a new Tweet for a user that is already populated in the User table and not saved as a variable in your current session you would have to run the following code:
    - `User.query.all()` will give you a list of all the users in the user table.
    - `tweet2 = Tweet(tweet='Some new tweet', user=User.query.filter_by(username='the user associated with the tweet').first())` this will associate the tweet with the first user in the User table with the username specified.
  - `DB.session.add(the tweet you are adding to the db)`
  - `DB.session.commit()` to save the new tweet to the database.
