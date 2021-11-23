from os import sep
from typing import Counter
import streamlit as st
import tweepy,sys
import time
import pandas as pd
import tweepy
from tweepy import API
from datetime import date
import random
from apps import preprocessing


from tweepy import tweet
from tweepy.models import User

#keyTwitterAPI
consumer_key= 'XTJX5kLme0sCCRukxee8qcTQX'
consumer_secret= 'bOS19bzKauIJGYDaPRoVfCdXlUAeM0xSLq2bfhK98eSxunz0ue'
access_token= '1012904378-AwoYi38Htqx2g0NZ2ZJrzTFnT3VeezVBTCCrDrZ'
access_token_secret= 'iAQmRtBgNci9J2YdImH7NXx7DoD5hPewwU8VYxhUFdClM'

#authorization
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, host='api.twitter.com', wait_on_rate_limit= True)

#totalTweets = 100
tweetsPerQry = 100
rand = str(random.randint(1,200))

def app():
    st.title("Search Entry")
    st.subheader("This will allow you to see the results based on crawled tweets from Twitter on 7 days back")
    userName = st.sidebar.text_input("Please Enter Your Full Name:", max_chars=30)
    keyWord = st.sidebar.text_input("Keyword:", max_chars=100)
    totalTweets = st.sidebar.number_input("How many tweets you want to be analyzed?", max_value=100, value=100, step=1)  #def 15 max 100
    #untilDate = st.sidebar.date_input("Until date:") #yyyy-mm-dd

    if st.sidebar.button("Analyze"):
        if len(userName) > 0 and len(keyWord) > 0 and totalTweets >0:
            if totalTweets > 100:
                st.sidebar.info("Sorry, this application has a limitation to analyze up to 100 tweets")
            elif totalTweets < 15:
                st.sidebar.info("Number of tweets that you may analyzed is from 15-100 tweets. Please input between 15-100")
            else:    
                ok = get_data(keyWord, totalTweets)       
                #callpreprocessing
                st.dataframe(ok, width=1000, height=1024)
                st.dataframe(preprocessing.fxprocessing(ok), width=1000, height=1024)
                        
        else:
            if len(userName) == 0:
                st.sidebar.info("Please enter your full name first")
            elif len(keyWord) == 0:
                st.sidebar.info("Please enter name of the university you want to look for")
            elif totalTweets == 0:
                st.sidebar.info("Please input the number of tweets you want to be analyzed (default = 100, max = 100)")
            else:
                e = RuntimeError('This is an exception of type RuntimeError')
                st.exception(e)    


def get_data(keyWord, totalTweets):
        if(not api):
            sys.exit('Failed Authentication, please re-check your "Consumer Key" & "Consumer Secret"')

        sinceId, max_id, tweetCount = None, -1, 1

        print("Start crawling max (0) tweets".format(totalTweets))
        #with open(fName, 'w') as f:
        while tweetCount < totalTweets:
            try:
                if(max_id<=0):
                    if(not sinceId):
                        new_tweets = api.search_tweets(q=keyWord, count = tweetsPerQry, lang='id')
                    else:
                        new_tweets = api.search_tweets(q=keyWord, count = tweetsPerQry, sinceId=sinceId, lang='id')
                else:
                    if(not sinceId):
                        new_tweets = api.search_tweets(q=keyWord, count = tweetsPerQry, max_id= str(max_id-1), lang='id')
                    else:
                        new_tweets = api.search_tweets(q=keyWord, count = tweetsPerQry, max_id= str(max_id-1), sinceId=sinceId, lang='id')
                if not new_tweets:
                    print('No more Tweets found in Query ="{0}"'.format(keyWord));break
       
                for tweet in new_tweets:
                    tweets_list = [[tweet.created_at, tweet.user.screen_name, tweet.user.location, tweet.text] for tweet in new_tweets]
                    tweets_univ = pd.DataFrame(tweets_list)
                    tweets_univ.columns = ["datetime", "username", "location", "tweet"]       
                    
                    #kalo mau di download as csv
                    filecsv = tweets_univ.to_csv(keyWord+'File'+rand+'.csv', encoding="utf8") 
                    #ini kalo pake json
                    #fName.write(jsonpickle.encode(tweet._json, unpicklable=False)+'\n')
                tweetCount += len(new_tweets)
                sys.stdout.write("\r");sys.stdout.write("Total Tweets saved: %.0f" %tweetCount);sys.stdout.flush()
                max_id=new_tweets[-1].id
                #st.dataframe(tweets_univ)
                df = pd.DataFrame(tweets_univ['tweet'])               
                remove_duplicate = pd.DataFrame(df).drop_duplicates(keep='first')
                
                #print(remove_duplicate)
                #showTweets = st.dataframe(remove_duplicate)
                #print(showTweets)
                return remove_duplicate

            except tweepy.TweepyException as e:
                print("some error: " + str(e));break
                #print('\nFinish! {0} tweets saved in {1}"'.format(tweetCount, fName))

    
