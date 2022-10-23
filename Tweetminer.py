"""
Script for downloading tweets from Twitter API

It downloads tweets by specified users as well as tweets tweets from the last 7 days that contain specified keywords.
The specified users are @USCGSoutheast, @SARwatchMED and @InfoMigrants
"""

import pandas as pd
from configparser import ConfigParser
from tweepy import OAuthHandler, API, Cursor

# read tokens and keys (requires Elevated Access for twitter api)
config = ConfigParser()
config.read('config.ini')

token = config['twdl']['token']
token_secret = config['twdl']['token_secret']
api_key = config['twdl']['api_key']
api_key_secret = config['twdl']['api_key_secret']

auth = OAuthHandler(api_key, api_key_secret)
auth.set_access_token(token, token_secret)

# initialize api
api = API(auth)

# download tweets by specified users
uscg_tweets = Cursor(
    api.user_timeline,
    screen_name = 'USCGSoutheast',
    count = 200,
    tweet_mode = 'extended'
    ).items(1000)

sarwatch_tweets = Cursor(
    api.user_timeline,
    screen_name = 'SARwatchMED',
    count = 200,
    tweet_mode = 'extended'
    ).items(1000)

infomig_tweets = Cursor(
    api.user_timeline,
    screen_name = 'InfoMigrants',
    count = 200,
    tweet_mode = 'extended'
    ).items(1000)

columns = ['User', 'Tweet', 'Date']
data = []

# tweets from last week
last_week = []

lw_tweets = Cursor(
    api.search_tweets,
    q = 'migrants missing dead',
    count = 200,
    tweet_mode = 'extended'
    ).items(1000)

# add tweets to list
for tweet in lw_tweets:
    last_week.append([tweet.user.screen_name, tweet.full_text, tweet.created_at])

df = pd.DataFrame(
    last_week,
    columns = columns
    )
# save to csv
df.to_csv('last_week.csv', index = False)
print(df.head())

for tweet in uscg_tweets:
    data.append([tweet.user.screen_name, tweet.full_text, tweet.created_at])

df1 = pd.DataFrame(
    data, 
    columns = columns
    )

print(df1.head())
df1.to_csv('uscg.csv', index = False)
data = []

for tweet in sarwatch_tweets:
    data.append([tweet.user.screen_name, tweet.full_text, tweet.created_at])

df2 = pd.DataFrame(data, columns = columns)
print(df2.head())
df2.to_csv('sarw.csv', index = False)
data = []

for tweet in infomig_tweets:
    data.append([tweet.user.screen_name, tweet.full_text, tweet.created_at])

df3 = pd.DataFrame(data, columns = columns)
print(df3.head())
df3.to_csv('info.csv', index = False)
