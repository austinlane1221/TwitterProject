from tweepy import API
from tweepy import Cursor
import tweepy
#Streaming tweets from twitter using tweepy
from tweepy.streaming import StreamListener
#import Oauthhandler because it authenticates the credentials
from tweepy import OAuthHandler
from tweepy import Stream

#importing packages so that I can analyze tweet data
import numpy as np
import pandas as pd

#importing matplotlib to visualize data
import matplotlib.pyplot as plt

#credentials file that has all of my tokens in it
import credentials

#Twitter Client class
#This class allows you to obtain tweets from either a user if you specify that, or your timeline if nothing is specified
class TwitterClient():
    def __init__(self, twitter_user = None):
        self.auth = Authenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    #A function that gets the twitter api so that you can interface with it
    def get_api(self):
        return self.twitter_client

    #A function that gets tweets and sets a limit on how many tweets you can see
    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id = self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friends = []
        for friend in Cursor(self.twitter_client.friends).items(num_friends):
            friends.append(friend)
        return friends

class Authenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
        auth.set_access_token(credentials.access_token, credentials.access_token_secret)
        return auth

class Streamer():

    #This class is responsible for streaming live tweets from twitter
    def __init__(self):
        self.twitter_authenticator = Authenticator()

    #This definition is responsible for authenticating and creating a stream
    def Streamed_Tweets(self, fetched_tweets_filename, hastaged_list): 
        
        listener = TwitterListener()
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)
        #filtering tweets to get data with keywords
        stream.filter(track = hashtaged_list)

class TwitterListener(StreamListener):

    #A listener class that prints tweets to stdout
    def __init__(self):
        self.fetched_tweets_filename = fetched_tweets_filename
    #on_data takes in data from the StreamListener class and allows us to do what we want
    #with the data
    def on_data(self,data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print('Error on_data %s' % str(e))
        return True
            
    #on_error a method that is overided if an error occurs, it also boots you if you reach this error
    #so you dont get kicked form the twitter API
    def on_error(self, status):
        if status == 420:
            return False
        print(status)

class TweetAnalysis():
    #A function that analyzes and categorizes data from twitter
    def tweets_to_dataframe(self, tweets):
        #making an object that takes in all the tweets data and puts them in a list
        df = pd.DataFrame(data = [tweet.text for tweet in tweets], columns = ['Tweets'])
        df['tweet id'] = np.array([tweet.id for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        df['favorites'] = np.array([tweet.favorite_count for tweet in tweets])
        df['Date'] = np.array([tweet.created_at for tweet in tweets])
        df['replies'] = np.array([tweet.in_reply_to_screen_name for tweet in tweets])
        return df

if __name__ == '__main__':
    
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalysis()
    api = twitter_client.get_api()

    tweets = api.user_timeline(screen_name = "AndrewYNg", count = 4)
    df = tweet_analyzer.tweets_to_dataframe(tweets)

    #print(np.max(df['favorites']))
    #print(np.max(df['retweets']))

    #making a time series of retweets and favorites
    time_favorites = pd.Series(data = df['favorites'].values, index = df['Date'])
    time_favorites.plot(figsize = (16, 4), color = 'r')
    plt.show()

    #print(dir(tweets[0]))

    print(df.head())
    
