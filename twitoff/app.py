from flask import Flask
from .db_model import DB, User, Tweet

# The code to run this app:
# export FLASK_APP=twitoff:APP 
# ^-- twitoff=directory, APP=defined function in the __init__.py file
# flask run

def create_app():
    '''
    Create and configure an instance of our Flask application
    '''
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///twitoff.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)  # Connect FLask A

    @app.route('/')  # The website for the app.
    def root():
        return 'Welcome to Twitoff!'

    @app.route('/<username>/<followers>')
    def add_user(username, followers):
        user = User(username=username, followers=followers)
        DB.session.add(user)
        DB.session.commit()

        return f'{username} has been added to the DB!'
    
    @app.route('/<username>/<tweet>')
    def add_user(username, tweet):
        tweet = Tweet(username=User(username), tweet=tweet)
        DB.session.add(tweet)
        DB.session.commit()

        return f'{username} has been added to the DB!'

    return app