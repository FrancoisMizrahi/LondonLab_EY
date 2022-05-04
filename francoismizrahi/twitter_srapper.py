import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime, timedelta
import time

def twitter_scapper(keyword, since, until):
    tweets_list = []
    print(f"{keyword} since:{since} until:{until}")
    tweets = sntwitter.TwitterSearchScraper(f"{keyword} lang:en since:{since} until:{until}")
    for i,tweet in enumerate(tweets.get_items()):
        print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
        print(tweet.date)
        print(tweet.content)
        tweets_list.append([tweet.date, tweet.id, tweet.content])
    df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Text'])
    df.to_csv(f"data/tweets/eng_{keyword}_{since}_{until}.csv")

def seg_date(keyword, since, until):
    d_since = pd.to_datetime(since, format='%Y-%m-%d')
    d_until = pd.to_datetime(until, format='%Y-%m-%d')
    num_days = (d_until-d_since).days
    while num_days > 30:
        start = time.time()
        print(f"{num_days} days remaining")
        until = d_since + timedelta(days=30)
        twitter_scapper(keyword, d_since.strftime('%Y-%m-%d'), until.strftime('%Y-%m-%d'))
        d_since = until
        num_days = (d_until-d_since).days
        end = time.time()
        print((end - start)/60)
    start = time.time()
    print(f"{num_days} days remaining")
    twitter_scapper(keyword, d_since.strftime('%Y-%m-%d'), d_until.strftime('%Y-%m-%d'))
    d_since = until
    num_days = (d_until-d_since).days
    end = time.time()
    print((end - start)/60)


if __name__ == '__main__':
    seg_date("facebook data", "2018-04-01", "2018-06-01")