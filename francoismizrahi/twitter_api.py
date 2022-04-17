from authentification import Bearer_Token
from tweepy import Client
import pandas as pd

# create your client 
client = Client(bearer_token=Bearer_Token)

# query to search for tweets
query = "#covid19 lang:en -is:retweet"
# your start and end time for fetching tweets
# start_time = "2021-12-10T00:00:00Z"
# end_time = "2021-12-14T00:00:00Z"
# get tweets from the API
tweets = client.search_recent_tweets(query=query,
                                     tweet_fields = ["created_at", "text", "source"],
                                     user_fields = ["name", "username", "location", "verified", "description"],
                                     max_results = 10,
                                     expansions='author_id'
                                     )

# create a list of records
tweet_info_ls = []
# iterate over each tweet and corresponding user details
for tweet, user in zip(tweets.data, tweets.includes['users']):
    tweet_info = {
        'created_at': tweet.created_at,
        'text': tweet.text,
        'source': tweet.source,
        'name': user.name,
        'username': user.username,
        'location': user.location,
        'verified': user.verified,
        'description': user.description
    }
    tweet_info_ls.append(tweet_info)
# create dataframe from the extracted records
tweets_df = pd.DataFrame(tweet_info_ls)
# display the dataframe
print(tweets_df.head())