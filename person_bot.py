from twython import Twython, TwythonError
from markov import MarkovGenerator
import os, time

APP_KEY = os.getenv('APP_KEY')
APP_SECRET = os.getenv('APP_SECRET')
OAUTH_TOKEN = os.getenv('OAUTH_TOKEN')
OAUTH_TOKEN_SECRET = os.getenv('OAUTH_TOKEN_SECRET')

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
user = '' #add twitter handle of user you want to ebook, edit!

def get_tweets(username):
	try:
		user_timeline = twitter.get_user_timeline(screen_name=username, count=200, include_rts=False, exclude_replies=True)
		tweets = [user_timeline[i]['text'] for i in range(len(user_timeline) - 1)]
		return tweets #tweet_list for generate_status function
	except TwythonError as e:
		return e

def generate_status(tweet_list):
	tweet_text = ' '.join(tweet_list)
	try:
		mc = MarkovGenerator(tweet_text, 90)
		status = mc.generate_words()
		return status
	except ValueError:
		pass

def ebook():
	status = generate_status(get_tweets(user))
	try:
		twitter.update_status(status=status)
		print status
		time.sleep(7200) #seconds you want your bot to wait between tweets, edit!
	except TwythonError as e:
		print e
		pass

if __name__ == '__main__':
	while  True:
		ebook()
