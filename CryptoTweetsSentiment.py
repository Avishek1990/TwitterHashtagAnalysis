# import libraries

# import sys
# import subprocess

# # implement pip as a subprocess:
# subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tweepy'])
# subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'twitter'])
# subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])
# subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy'])

import os
import tweepy as tw
import pandas as pd
import json
import warnings
warnings.simplefilter('ignore')
import twitter
import datetime as dt

def twitter_APIAuth():
    consumer_key = '7Y8QH399EU6qzrBWkKh3J8mc4'
    consumer_secret = 'SQmV9dc8XpirXpcDKD7y54RmruGqp8gN5aFzcD3YOK93LpSkC6'
    access_token = '795376566-mU7efJXdyckPPum8pZVDQ4CylA23ErVTBpQ8yMTI'
    access_token_secret = 'S2qdHOiD5tX4p1wigzJMkaV1dAKN6tzicJxvzm2RodGDu'
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth

api = tw.API(twitter_APIAuth(), wait_on_rate_limit=True)

# Define the search term and the date_since date as variables
search_words = "bitcoin"
date_since = "2021-11-11"
date_until = "2021-11-12"

# Collect tweets

try: 
    tweets_Crypto = pd.read_csv('CheckPointTweets.csv')
    date_since_ = pd.to_datetime(tweets_Crypto.sort_values('created_at',ascending = True)['created_at'][0])
    tweets = tw.Cursor(api.search_tweets,
              q=search_words,
              lang="en",
              since=date_since,
              until=date_until)
    i = tweets_Crypto.shape[0]
    print(i)
except FileNotFoundError:

    tweets = tw.Cursor(api.search_tweets,
              q=search_words,
              lang="en",
              since=date_since,
              until=date_until)

    tweets_Crypto = pd.DataFrame(columns = ['text','favourites_count', 'retweet_count','statuses_count','created_at','followers_count','friends_count','listed_count','verified'])
    i = 0
# tweets = tw.Cursor(api.search_tweets,
#               q=search_words,
#               lang="en",
#               since=date_since)

# tweets_Crypto = pd.DataFrame(columns = ['text','favourites_count', 'retweet_count','statuses_count','created_at','followers_count','friends_count','listed_count','verified'])
# i = 0
# tweets



date_check = False
for tweet in tweets.items():
    if date_check == False:
        if tweet.created_at <= date_since_:
            date_check == True
   
    if date_check == True:

        tweets_Crypto.loc[i,'text'] = tweet.text
        tweets_Crypto.loc[i,'favourites_count'] = tweet.user.favourites_count
        tweets_Crypto.loc[i,'retweet_count'] = tweet.retweet_count
        tweets_Crypto.loc[i,'statuses_count'] = tweet.user.statuses_count
        tweets_Crypto.loc[i,'created_at'] = tweet.created_at
        # print(tweet.created_at)
        # print(pd.to_datetime(tweet.created_at).date())
        tweets_Crypto.loc[i,'followers_count'] = tweet.user.followers_count
        tweets_Crypto.loc[i,'friends_count'] = tweet.user.friends_count
        tweets_Crypto.loc[i,'listed_count'] = tweet.user.listed_count
        tweets_Crypto.loc[i,'verified'] = tweet.user.verified
        # print(tweets_Crypto)
        # print(json.loads(tweet.Status.json))
        print(i,end='\r')
        i+=1
        if i%1000 == 0:
            tweets_Crypto['created_at'] = tweets_Crypto['created_at'].apply(lambda a: pd.to_datetime(a)) 
            tweets_Crypto.to_csv('CheckPointTweets.csv')
            # tweets_Crypto.head()
