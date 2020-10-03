# Module 2:
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
 - In the `base.html` file where you see `{{ some_variable }}` this tells you that you will need to tell it was to populate for that value, like using `{some_variable}` in an f string.
 - I can change the styling of the home page within the `base.html` by researching twitter bootstrap themes. (this is a stretch goal) Would need to create a css file `stylesheet.html` in order to change the style of the website.
- In the `templates` folder create a new file `user.html`, this is where the code will be stored for the page that the you get taken to when you click the "Add User" button.

## New imports to add to `.py` files already created from prior class:
- New imports to add to `app.py`:
 - Add to `from flask import Flask`:
  - `, render_template` a built in method of `flask` that knows how to read the HTML file and then populate some information into that HTML file.
  - `, request` built in method of `flask` to request data from database or `user_name`

## Change some things to the `.py` files already created:
- Changes needed to `app.py`:
 - Under `def root():` the `return` will now change from `return 'Welcome to Twitoff'` to `return render_template('base.html', title='Home', users=User.query.all())`, this will change the layout of the "Home" page of the app website. The `users=User.query.all()` will pull all users from the User table and populate a list on the website.
 - 

## Clean up the database to add new users and tweets:
- Go into `flask shell` in the terminal.
- `import twitoff.db_model import DB` to import database.
- `DB.drop_all()` will remove all data already in the database.
- `DB.create_all()` will start with a fresh database.