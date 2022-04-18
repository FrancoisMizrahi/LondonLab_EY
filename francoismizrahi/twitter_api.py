from authentification import Bearer_Token
from tweepy import Client
from datetime import date, timedelta


class Twitter_api:

    def __init__(self):
        self.Bearer_Token = Bearer_Token
    
    def get_tweets(self, keyword, max_results=100):
        # create your client 
        client = Client(bearer_token=self.Bearer_Token)

        # query to search for tweets
        query = f"{keyword} lang:en"

        # your start and end time for fetching tweets
        start_time = date.today() - timedelta(days=1)
        start_time = f"{start_time.strftime('%Y-%m-%d')}T00:00:00Z"

        # get tweets from the API
        tweets = client.search_recent_tweets(query=query,
                                            start_time = start_time,
                                            tweet_fields = ["created_at", "text", "source"],
                                            user_fields = ["name", "username", "location", "verified", "description"],
                                            max_results = max_results, # Between 10 and 100
                                            expansions='author_id'
                                            )
        return tweets

if __name__ == '__main__':
    twitter_api = Twitter_api()
    tweets = twitter_api.get_tweets(keyword= "covid", max_results=10)
    for tweet in tweets.data:
        print("\n###################\n")
        print(tweet["text"])