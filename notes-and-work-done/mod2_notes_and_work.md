# Module 2:
## Starting up:
- Open this repository in VSCode.
- `pipenv shell` to activate my virtual environment.
- `pipenv install tweepy python-dotenv spacy` installs the following packages into my virtual environment:
  - `tweepy` a convenient way to access the Twitter API using Python.
  - `pyhton-dotenv` allows me to store environment variables in a .env file for use in my python files.
  - `spacy` an easy way to preform Natural Language Processing (NLP) on the tweets I will be pulling from Twitter. It will turn the raw text tweets into a numerical form that can then be passed into a machine learning model.
- `pipenv install --dev jupyter` gives me the ability to run jupyter notebooks.
- `python -m spacy download en_core_web_md` installs the English language package for SpaCy in my virtual environment.
- Can open the jupyter notebook with the virtual environment with the code `pipenv run jupyter notebook` or `pipenv run jupyter lab`

## Create the HTML files to make the app usable from the website:
- In the twitoff folder, create a new folder called `templates`, this will hold the HTML files for each page within the app.
- In the `templates` folder create a new file `base.html`, this will be where the "home" page code will be stored for the layout of the "home" page.
 - In the `base.html` file where you see `{{ some_variable }}` this tells you that you will need to tell it what to populate for that value, like using `{some_variable}` in an f string.
 - I can change the styling of the home page within the `base.html` by researching twitter bootstrap themes. (this is a stretch goal) Would need to create a css file `stylesheet.html` in order to change the style of the website.
- In the `templates` folder create a new file `user.html`, this is where the code will be stored for the page that the you get taken to when you click the "Add User" button or one of the user name hyperlinks.

## New imports to add to `.py` files already created from prior class:
- New imports to add to `app.py`:
 - Add to `from flask import Flask`:
  - `, render_template` a built in method of `flask` that knows how to read the HTML file and then populate some information into that HTML file.
  - `, request` built in method of `flask` to request data from database or `user_name`
 - `from .twitter import add_user_tweepy` imports the method created in `twitter.py`
- Added a new file to the directory `twitter.py`

## Change some things to the `.py` files already created:
- Changes needed to `app.py`:
 - Under `def root():` the `return` will now change from `return 'Welcome to Twitoff'` to `return render_template('base.html', title='Home', users=User.query.all())`, this will change the layout of the "Home" page of the app website. The `users=User.query.all()` will pull all users from the User table and populate a list on the website.
 - Added 2 new `@app.route` and commented out the old code from last session and moved it to the bottom of the file since it was no longer needed.
- Changes needed to `db_model.py`:
 - Under `User` class changed `id = DB.Column(DB.Interger,...)` to `id = DB.Column(DB.BigInteger,...)` because the actual Twitter id numbers are large numbers.
 - Under `User` class added `newest_tweet_id` to show the most recent tweet id.
 - Under `Tweet` class added `embedding` to use for when we add the machine learning model to the app.

## Clean up the database to add new users and tweets:
- Go into `flask shell` in the terminal.
- `import twitoff.db_model import DB` to import database.
- `DB.drop_all()` will remove all data already in the database.
- `DB.session.commit()` to save the changes.
- `DB.create_all()` will start with a fresh database.
- `DB.session.commit()` to save the fresh database.

## How to run Flask in debug mode:
- In the `bash` terminal in my `pipenv` need to run the following codes:
 - `export FLASK_ENV=development` this will put you into debug mode until you close VS Code.
 - Then just run `flask run` and you will see the debugger is active now.
- Some advantages to running in debug mode:
 - When you are working on the files that are associated with your app, when you save the file the flask run app will automatically restart itself. This leads to less time closing it out and going back into it whenever you make changes to one or more of the files.
 - Even though the app may give you a 200 response code, when you are in debug mode, it will tell you what the issue was if the app did not preform properly even though it appears to have went through correctly.
