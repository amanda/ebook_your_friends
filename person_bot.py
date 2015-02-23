from twython import Twython, TwythonError
from markov import MarkovGenerator, twitter_tokenize
from math import log
from random import random
import os
import time

APP_KEY = os.getenv('APP_KEY')
APP_SECRET = os.getenv('APP_SECRET')
OAUTH_TOKEN = os.getenv('OAUTH_TOKEN')
OAUTH_TOKEN_SECRET = os.getenv('OAUTH_TOKEN_SECRET')

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
user = ''  # add twitter handle of user you want to ebook, edit!

'''time between tweets in seconds
set a minimum because we don't want near-simultaneous tweets'''
minimum_interval = 300
average_interval = 7200


def tweets_from_timeline(timeline):
    '''timeline -> list of tweets
    '''
    return [timeline[i]['text']
            for i in range(len(timeline))]


def ids_from_timeline(timeline):
    '''timeline -> list of numbers
    '''
    return [timeline[i]['id']
            for i in range(len(timeline))]


def get_tweets(username):
    '''(str) -> (list of tweets, id of most recent tweet),
    fetches last 3200 tweets from specified user'''
    try:
        tweets = []
        since_id = None
        max_id = None
        for _ in range(16):
            if max_id is None:
                user_timeline = twitter.get_user_timeline(
                    screen_name=username, count=200,
                    include_rts=False, exclude_replies=True)
                since_id = max(ids_from_timeline(user_timeline))
            else:
                user_timeline = twitter.get_user_timeline(
                    screen_name=username, count=200,
                    include_rts=False, exclude_replies=True,
                    max_id=max_id)
            new_tweets = tweets_from_timeline(user_timeline)
            if len(new_tweets) == 0:
                return (tweets, since_id)
            tweets += new_tweets
            max_id = min(ids_from_timeline(user_timeline))
            max_id -= 1  # max_id is inclusive, so sub 1 to avoid repeats.
        return (tweets, since_id)
    except TwythonError as e:
        print e
        return e


def get_new_tweets(username, since_id):
    '''str, number -> list of tweets, number
    fetches any new tweets made after |since_id|'''
    try:
        user_timeline = twitter.get_user_timeline(
            screen_name=username, count=200,
            include_rts=False, exclude_replies=True,
            since_id=since_id)
        if len(user_timeline) == 0:
            return (None, None)
        tweets = tweets_from_timeline(user_timeline)
        since_id = max(ids_from_timeline(user_timeline))
        return (tweets, since_id)
    except TwythonError as e:
        print e
        return e


def post_tweet_from_generator(generator):
    '''generates a status, posts it to twitter and logs it'''
    status = generator.generate_words().lower()
    try:
        twitter.update_status(status=status)
        print time.strftime('[%y-%m-%dT%H:%M:%S] {}').encode('utf-8').format(status)
        time.sleep(minimum_interval -
                   log(random()) * (average_interval - minimum_interval))
    except TwythonError as e:
        print e
        pass

def ebook():
    '''the loop with all the action'''
    tweet_list, since_id = get_tweets(user)
    update_markov = True
    while True:
        if update_markov:
            tweet_text = ' '.join(tweet_list)
            mc = MarkovGenerator(tweet_text, 90, tokenize_fun=twitter_tokenize)
            update_markov = False

        post_tweet_from_generator(mc)

        # download new tweets
        new_tweet_list, new_since_id = get_new_tweets(user, since_id)
        if len(new_tweet_list) != 0:
            tweet_list += new_tweet_list
            since_id = new_since_id
            update_markov = True


if __name__ == "__main__":
    ebook()
