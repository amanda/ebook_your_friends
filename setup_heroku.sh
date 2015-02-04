#!bin/bash

'''script that sets up a python twitter bot on heroku.
BUT FIRST!
0. make sure you have git installed
1. make sure you have a requirements.txt file with your dependencies
2. make sure you have the API credentials for your bot
press ctrl-c now if you need to do any of these things!'''

echo "let's get your bot up and running!"
read -p "first, what is the name of the twitter bot you want to create? " name
echo ""

echo "initializing git repo"
git init

echo ""
echo "setting up your bot on heroku"
while ! heroku create $name; do
    echo "looks like that name is taken :("
    read -p "try another name: " name
done

echo ""
echo "hurray, hopefully that worked."
echo ""
echo "now we're gonna need your bot's credentials."
echo ""
read -p "enter the APP KEY: " APP_KEY
read -p "enter the APP SECRET: " APP_SECRET
read -p "enter the OAUTH TOKEN: " OAUTH_TOKEN
read -p "almost done! enter the OAUTH TOKEN SECRET: " OAUTH_TOKEN_SECRET
echo ""
echo "setting heroku config variables"
export APP_KEY=$APP_KEY
export APP_SECRET=$APP_SECRET
export OAUTH_TOKEN=$OAUTH_TOKEN
export OAUTH_TOKEN_SECRET=$OAUTH_TOKEN_SECRET

heroku config:set APP_KEY=$APP_KEY APP_SECRET=$APP_SECRET OAUTH_TOKEN=$OAUTH_TOKEN OAUTH_TOKEN_SECRET=$OAUTH_TOKEN_SECRET

echo ""
echo "creating the procfile"
echo ""
read -p "enter the name of the script that runs your bot (include the .py): " script
echo ""
cat <<EOF > Procfile
worker: python $script
EOF

echo ""
echo "pushing to heroku"
echo ""
git add .
git commit -m 'added all files'
git push heroku master
heroku ps:scale worker=1

echo "done! your bot should now be running on heroku."
echo "type heroku logs --tail to make sure."
