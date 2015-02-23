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


def get_tweets(username):
    '''(str) -> list of tweets,
    fetches last 3200 tweets from specified user'''
    try:
        tweets = []
        max_id = None
        for _ in range(16):
            if max_id is None:
                user_timeline = twitter.get_user_timeline(
                    screen_name=username, count=200,
                    include_rts=False, exclude_replies=True)
            else:
                user_timeline = twitter.get_user_timeline(
                    screen_name=username, count=200,
                    include_rts=False, exclude_replies=True,
                    max_id=max_id)
            new_tweets = [user_timeline[i]['text']
                      for i in range(len(user_timeline))]
            if len(new_tweets) == 0:
                return tweets
            tweets += new_tweets
            max_id = min([user_timeline[i]['id']
                          for i in range(len(user_timeline))])
            max_id -= 1  # max_id is inclusive, so sub 1 to avoid repeats.

        return tweets

    except TwythonError as e:
        print e
        return e


def generate_status(tweet_list):
    '''(list) -> str,
    returns markov-generated status'''
    tweet_text = ' '.join(tweet_list)
    try:
        mc = MarkovGenerator(tweet_text, 90, tokenize_fun=twitter_tokenize)
        status = mc.generate_words().lower()
        return status
    except ValueError as e:
        print e
        pass


def ebook():
    '''posts generated status to twitter'''
    status = generate_status(get_tweets(user))
    try:
        twitter.update_status(status=status)
        print time.strftime('[%y-%m-%dT%H:%M:%S] {}').format(status)
        time.sleep(minimum_interval -
                   log(random()) * (average_interval - minimum_interval))
    except TwythonError as e:
        print e
        pass

if __name__ == '__main__':
    while True:
        ebook()
