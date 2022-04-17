from authentification import Bearer_Token
from tweepy import Client
from datetime import date, timedelta

# create your client 
client = Client(bearer_token=Bearer_Token)

# query to search for tweets
keyword = "covid19"
query = f"{keyword} lang:en"

# your start and end time for fetching tweets
start_time = date.today() - timedelta(days=1)
start_time = f"{start_time.strftime('%Y-%m-%d')}T00:00:00Z"

# get tweets from the API
tweets = client.search_recent_tweets(query=query,
                                    start_time = start_time,
                                    tweet_fields = ["created_at", "text", "source"],
                                    user_fields = ["name", "username", "location", "verified", "description"],
                                    max_results = 100, # Between 10 and 100
                                    expansions='author_id'
                                    )

for tweet in tweets.data:
    print("\n###################\n")
    print(tweet["text"])