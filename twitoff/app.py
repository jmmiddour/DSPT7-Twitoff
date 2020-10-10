from os import getenv
from flask import Flask, render_template, request
from .db_model import DB, User
from .twitter import add_user_tweepy, add_user_history, update_all_users
from .predict import predict_user

def create_app():
    '''
    Create and configure an instance of my Flask application
    '''
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)  # Connect FLask app to the SQLAlchemy database

    @app.route('/')  # The home page for the app.
    def root():  # This is the defining the root directory/home page of the app.
        return render_template('base.html', title='Welcome to TwitOff', users=User.query.all())

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
        
        return render_template('user.html', title=f'User: {name}', tweets=tweets,
                               message=message)
    
    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1 = request.values['user1']
        user2 = request.values['user2']
        tweet_text = request.values['tweet_text']

        if user1 == user2:
            message = "Can not compare a user to themselves."
        else:
            prediction = predict_user(user1, user2, tweet_text)

            message = f"""
                       @{user1 if prediction else user2} 
                       is more likey to tweet this than 
                       @{user2 if prediction else user1}.
                       """

        return render_template('predict.html', title='Your Prediction', 
                                users=User.query.all(), **locals())

    @app.route('/reset_my_DB')
    def reset():
        DB.drop_all()
        DB.create_all()

        return render_template('base.html', title='Reset Database',
                               message=f'The database has been reset.',
                               users=User.query.all())

    @app.route('/update')
    def update():
        update_all_users()
        return render_template('base.html', title='Updated Tweets', 
                                message='All Tweets have been Updated!', 
                                users=User.query.all())

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

# The code to run this app:
# export FLASK_APP=twitoff:APP 
# ^-- twitoff=directory, APP=defined function in the __init__.py file
# flask run