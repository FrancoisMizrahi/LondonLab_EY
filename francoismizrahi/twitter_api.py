from authentification import API_Key, API_Key_Secret, Bearer_Token, Access_Token, Access_Token_Secret
from tweepy import OAuthHandler, API, Cursor
import pandas as pd
import csv
import re 
import string
import preprocessor as p
  
auth = OAuthHandler(API_Key, API_Key_Secret)
auth.set_access_token(Access_Token, Access_Token_Secret)
 
api = API(auth,wait_on_rate_limit=True)
 
search_words = "Nasa"      # enter your words
new_search = search_words + " -filter:retweets"
 
for tweet in Cursor(api.search_tweets,q=new_search,count=100,lang="en",since_id=0).items():
    print(tweet.text)