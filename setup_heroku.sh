#!/bin/bash

echo "script that sets up a python twitter bot on heroku.
BUT FIRST!
0. make sure you have git installed
1. make sure you have a requirements.txt file with your dependencies
2. make sure you have the API credentials for your bot
press ctrl-c now if you need to do any of these things!"

echo "let's get your bot up and running!"
read -p "first, what is the name of the twitter bot you want to create? " name

echo -e "\ninitializing git repo"
git init

echo -e "\nsetting up your bot on heroku"
while ! heroku create $name; do
    echo "looks like that name is taken :("
    read -p "try another name: " name
done

echo -e "\nhurray, hopefully that worked.\n"
echo -e "now we're gonna need your bot's credentials.\n"
if [-z $APP_KEY];then
    read -p "enter the APP KEY: " TWITTERBOT_APP_KEY

if [-z $APP_SECRET];then
    read -p "enter the APP SECRET: " TWITTERBOT_APP_SECRET

if [-z $OAUTH_TOKEN];then
    read -p "enter the OAUTH TOKEN: " TWITTERBOT_OAUTH_TOKEN

if [-z $OAUTH_TOKEN_SECRET];then
    read -p "almost done! enter the OAUTH TOKEN SECRET: " TWITTERBOT_OAUTH_TOKEN_SECRET

echo -e "\nsetting heroku config variables"

heroku config:set APP_KEY=$TWITTERBOT_APP_KEY APP_SECRET=$TWITTERBOT_APP_SECRET OAUTH_TOKEN=$TWITTERBOT_OAUTH_TOKEN OAUTH_TOKEN_SECRET=$TWITTERBOT_OAUTH_TOKEN_SECRET

echo -e "\ncreating the procfile\n"
read -p "enter the name of the script that runs your bot (include the .py): " script
echo ""
cat <<EOF > Procfile
worker: python $script
EOF

echo -e "\npushing to heroku\n"
git add .
git commit -m 'added all files'
git push heroku master
heroku ps:scale worker=1

echo -e "done! your bot should now be running on heroku.\n type heroku logs --tail to make sure."
