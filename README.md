# ebook_your_friends

A Python script (person_bot.py) that uses the Twython Twitter API wrapper to read tweets from a user's timeline and post Markov-generated tweets to a bot account, a Markov text generator (markov.py) to generate tweets, and a shell script (setup_heroku.sh) to get the bot automatically tweeting on Heroku.

# usage

If you just want to make a single "ebook" account for yourself or a friend, follow these instructions:

1. Clone the repo
2. Edit person_bot.py with the twitter handle (do not include the "@") of the person you want to make a bot of
3. Setup a new Twitter account for your bot
4. Go to [apps.twitter.com](https://apps.twitter.com/), create a new application, and grab its API credentials
5. run ```source setup_heroku.sh``` and follow the prompts (make sure you have a virtualenv set up, git installed, and a Heroku account)

Have fun (◡ ‿ ◡ ✿)
