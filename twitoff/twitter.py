from os import getenv
import tweepy
import spacy
from dotenv import load_dotenv
from .db_model import DB, User, Tweet

# Load .env credentials:
load_dotenv()

# Set Twitter Authentication models:
TWITTER_AUTH = tweepy.OAuthHandler(getenv('TWITTER_KEY'), 
                                   getenv('TWITTER_SECRET'))
TWITTER_AUTH.set_access_token(getenv('TWITTER_TOKEN'), 
                              getenv('TWITTER_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)

# Load SpaCy pre-trained med English Language model
#   disabling the tagger and parser will help to speed up the process some.:
nlp = spacy.load('spacy_sm_model')


def vectorize_tweet(nlp, tweet_text):
    '''
    This function returns the SpaCy embeddings for an imput text.
    '''
    return list(nlp(tweet_text).vector)

def add_user_tweepy(username):
    '''
    Add a user and their tweets to the database.
    '''
    try:
        # Gets the user info from tweepy:
        twitter_user = TWITTER.get_user(username)

        # Add the user to User table (ckecks if existing):
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id,
                        username=username,
                        followers=twitter_user.followers_count))
        DB.session.add(db_user)

        # Get tweets while ignoring re-tweets and replies:
        tweets = twitter_user.timeline(count=200,
                                       exclude_replies=True,
                                       include_rts=False,
                                       tweet_mode='extended',
                                       since_id=db_user.newest_tweet_id) 
        print(f'Total Tweets collected for {username}: {len(tweets)}')
        
        # Add newest_tweet_id to the User table:
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        
        # Iterate over the tweets, get embedding and add to Tweet table:
        for tweet in tweets:
            # Get an example basilica embedding and add to Tweet table:
            embedding = vectorize_tweet(nlp, tweet.full_text)
            # Add tweet info to the Tweet table:
            db_tweet = Tweet(id=tweet.id,
                             tweet=tweet.full_text[:300],  # [:300] limits to 300 characters
                             embedding=embedding)
            db_user.tweet.append(db_tweet)
            DB.session.add(db_tweet)
    
    except Exception as e:
        print(f'Error processing {username}: {e}')
        raise e

    else:
        print('Successfully saved tweets to DB!')
        # If no errors occur then commit the records:
        DB.session.commit()

def add_user_history(username):
    '''Add max tweet history (API limit of 3200) to database'''
    try:
        # Get user info from tweepy
        twitter_user = TWITTER.get_user(username)
        # Add to User table (or check if existing)
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id,
                        username=username,
                        followers=twitter_user.followers_count))
        DB.session.add(db_user)
        # Get tweets ignoring re-tweets and replies
        tweets = twitter_user.timeline(count=200, 
                                       exclude_replies=True, 
                                       include_rts=False, 
                                       tweet_mode='extended')
        oldest_max_id = tweets[-1].id - 1
        tweet_history = []
        tweet_history += tweets
        # Add newest_tweet_id to the User table
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        # Continue to collect tweets using max_id and update until 3200 tweet max
        while True:
            tweets = twitter_user.timeline(count=200,
                                        exclude_replies=True,
                                        include_rts=False,
                                        tweet_mode='extended',
                                        max_id=oldest_max_id)
            if len(tweets) == 0:
                break
            oldest_max_id = tweets[-1].id - 1
            tweet_history += tweets 
        print(f'Total Tweets collected for {username}: {len(tweet_history)}')
        # Loop over tweets, get embedding and add to Tweet table
        for tweet in tweet_history:
            # Get an examble basilica embedding for first tweet
            embedding = vectorize_tweet(nlp, tweet.full_text)
            # Add tweet info to Tweet table
            db_tweet = Tweet(id=tweet.id,
                             tweet=tweet.full_text[:300],
                             embedding=embedding)
            db_user.tweet.append(db_tweet)
            DB.session.add(db_tweet)
    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        raise e
    else:
        # If no errors happend than commit the records
        DB.session.commit()
        print('Successfully saved tweets to DB!')

def update_all_users():
    '''This function will update tweets for all users.'''
    for user in User.query.all():
        add_user_tweepy(user.username)

# Close down the session:
# DB.session.close()