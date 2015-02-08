# ebook_your_friends

A Python script (person_bot.py) that uses the Twython Twitter API wrapper to read tweets from a user's timeline and post Markov-generated tweets to a bot account, a Markov text generator (markov.py) to generate tweets, and a shell script (setup_heroku.sh) to get the bot automatically tweeting on Heroku.

## requirements
- Twython
- ntlk

## usage

If you just want to make a single "ebook" account for yourself or a friend, follow these instructions. For a more detailed tutorial on making Twitter bots using this repo, read [this blog post](http://programmingforwitches.tumblr.com/post/110169568366/ebook-your-friends).

1. Clone the repo and install requirements using pip: ```pip install -r requirements.txt```
2. Edit person_bot.py with the twitter handle (do not include the "@") of the person you want to make a bot of
3. Setup a new Twitter account for your bot
4. Go to [apps.twitter.com](https://apps.twitter.com/), create a new application, and grab its API credentials
5. Set your API credentials as environment variables (APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET). You can then check out some sample tweets from your bot in the Python repl by importing person_bot and running: ```generate_status(get_tweets(user))```
6. ```source setup_heroku.sh``` and follow the prompts to get your bot tweeting automatically with Heroku (make sure you have git installed and a Heroku account)

Have fun (◡ ‿ ◡ ✿)
