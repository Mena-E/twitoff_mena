"""Retrieve tweets, and users then creates embeddings and populate DB"""
from os import getenv
import tweepy
import spacy
from .models import DB, Tweet, User

TWITTER_AUTH = tweepy.OAuthHandler(
    getenv("TWITTER_API_KEY"),
    getenv("TWITTER_API_KEY_SECRET")
)
TWITTER = tweepy.API(TWITTER_AUTH)

# nlp model
nlp = spacy.load("my_model")

def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


def add_or_update_user(username):
    """
    Gets twitter user and tweets from twitter DB
    Gets user by "username" parameter.
    """
    try:
        # Gets back twitter user object
        twitter_user = TWITTER.get_user(username)
        # Either updates or adds user to our DB
        db_user = (User.query.get(twitter_user.id)) or User(
            id=twitter_user.id, name=username)
        DB.session.add(db_user)

        # Getting tweets from "twitter_user"
        tweets = twitter_user.timeline(
            count=200, 
            exclude_replies=True, 
            include_rts=False,
            tweet_mode="Extended",
            since_id=db_user.newest_tweet_id
        )

        if tweets:
            db_user.newest_tweet_id = tweets[0].id 

        # tweets is a list of tweet objects
        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet.text)
            db_tweet = Tweet(id=tweet.id, text=tweet.text,
                        vect=tweet_vector)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

        DB.session.commit()

    except Exception as e:
        print("Error processing{}: {}".format(username, e))
        raise e

    else:
        DB.session.commit()
