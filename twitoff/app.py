from flask import Flask, render_template, request
from .db_model import DB, User, Tweet
from .twitter import add_user_tweepy

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
    DB.init_app(app)  # Connect FLask app to the SQLAlchemy database

    @app.route('/')  # The website for the app.
    def root():  # This is the root directory/home page of the app.
        return render_template('base.html', title='Home', users=User.query.all())

    @app.route('/user', methods=['POST'])  # Adds data from a form to Database
    @app.route('/user/<name>', methods=['GET'])  # Displays data from Database
    def add_or_update_user(name=None, message=''):
        name = name or request.values['user_name']

        try:
            if request.method == 'POST':
                add_user_tweepy(name)
                message = f'User {name} has successfully been added to the Database!'
                # This will pull the tweet atributes for the user just specified:
                tweets = User.query.filter(User.username == name).one().tweet
        
        except Exception as e:
            print(f'Error adding {name}: ERROR = {e}')
            tweets = []
        
        return render_template('user.html', title=name, tweets=tweets,
                               message=message)
    
    return app

    ## The following code was from module 1 and is no longer needed:
    # @app.route('/add_user/<username>/<followers>')  
    # # ^-- Will allow to enter information to the route and commit it to the DB.
    # def add_user(username, followers):
    #     user = User(username=username, followers=followers)
    #     DB.session.add(user)  # Adds data to "staging area" to be saved to DB.
    #     DB.session.commit()  # Saves new data to the database.

    #     return f'{username} has been added to the Database!'
    
    # @app.route('/add_tweet/<user_id>/<tweet>')
    # def tweet(user_id, tweet):
    #     new_tweet = Tweet(user_id=user_id, tweet=tweet)
    #     DB.session.add(new_tweet)
    #     DB.session.commit()

    #     return f'{tweet} has been added to the DB!'

    # return app