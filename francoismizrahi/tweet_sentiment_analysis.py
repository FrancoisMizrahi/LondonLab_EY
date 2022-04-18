# from francoismizrahi.twitter_api import TwitterApi
# from francoismizrahi.text_preprocessing import TextPreprocessing
# from francoismizrahi.sentiment_analysis import SentimentAnalysis


import twitter_api
import text_preprocessing
import sentiment_analysis


class TweetsSentimentAnalysis:

    def __init__(self, keyword="covid", max_results=10, stem=False, keep_stop_words=[], include_neutral=True):
        # Tweets
        self.TwitterApi = twitter_api.TwitterApi()
        self.keyword = keyword
        self.max_results = max_results

        # Processing
        self.TextPreprocessing = text_preprocessing.TextPreprocessing()
        self.stem = stem
        self.keep_stop_words = keep_stop_words

        # Sentiment Analysis
        self.SentimentAnalysis = sentiment_analysis.SentimentAnalysis()
        self.include_neutral = include_neutral
    
    def get_tweets_sentiment_analysis(self):
        print("Getting Tweets...")
        tweets = self.TwitterApi.get_tweets(self.keyword, self.max_results)
        sentiments = []
        print("Getting Sentiments...")
        for tweet in tweets.data:
            text = self.TextPreprocessing.preprocess(tweet["text"], self.stem, self.keep_stop_words)
            sentiment = self.SentimentAnalysis.predict(text, self.include_neutral)
            sentiments.append(sentiment)
        return sentiments

if __name__ == '__main__':
    print("Starting...")
    t = TweetsSentimentAnalysis(keyword="coca cola", max_results=20)
    sentiments = t.get_tweets_sentiment_analysis()
    print("Result:")
    print(sentiments)