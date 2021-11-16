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
# import twitter
import boto3
from botocore.exceptions import ClientError
import os
import logging
import datetime as dt

def twitter_APIAuth():
    consumer_key = '7Y8QH399EU6qzrBWkKh3J8mc4'
    consumer_secret = 'SQmV9dc8XpirXpcDKD7y54RmruGqp8gN5aFzcD3YOK93LpSkC6'
    access_token = '795376566-mU7efJXdyckPPum8pZVDQ4CylA23ErVTBpQ8yMTI'
    access_token_secret = 'S2qdHOiD5tX4p1wigzJMkaV1dAKN6tzicJxvzm2RodGDu'
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth


class getTweets(object):
    
    def __init__(self):
        self.api = tw.API(twitter_APIAuth(), wait_on_rate_limit=True)
        print(self.api)
        self.search_words = None
        self.date_since = None
        self.date_until = None

    def enterSearchCriteria(self,search_words,date_since,date_until):

        # Define the search term and the date_since date as variables
        self.search_words = search_words
        self.date_since = date_since
        self.date_until = date_until
        print(self.search_words)
        print(self.date_since)
        print(self.date_until)

    def S3Connect(self):

        pass

    def searchTweets(self):

        # Collect tweets

        tweets = tw.Cursor(self.api.search_tweets,
                        q=self.search_words,
                        lang="en",
                        tweet_mode="extended",
                        since=self.date_since,
                        until=self.date_until)

        # print(tweets)

        tweets_Crypto = pd.DataFrame(columns = ['text','favourites_count', 'retweet_count','statuses_count','created_at','followers_count','friends_count','listed_count','verified'])
        
        # print(tweets_Crypto)
        
        i = 0

        for tweet in tweets.items(100):
            # print(tweet)
            tweets_Crypto.loc[i,'text'] = tweet._json['full_text']
            # print(tweet._json['full_text'])
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
            if i%10 == 0:
                tweets_Crypto['created_at'] = tweets_Crypto['created_at'].apply(lambda a: pd.to_datetime(a)) 
                tweets_Crypto.to_csv('CheckPointTweets.csv')
                # tweets_Crypto.head()

                self.upload_file('CheckPointTweets.csv','twitterdatacrypto')
        
        return tweets_Crypto

    def upload_file(self,file_name, bucket, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        AWS_ACCESS_KEY_ID = 'AKIAZRVF4KZBP3TR5F4P'
        AWS_SECRET_ACCESS_KEY = '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'

        # conn = boto3.conne(AWS_ACCESS_KEY_ID,
        # AWS_SECRET_ACCESS_KEY)

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        # Upload the file
        s3_client = boto3.resource('s3',AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)
        try:
            response = s3_client.Bucket(bucket).put_object(Key = 'checkpoint.csv',Body=file_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True


