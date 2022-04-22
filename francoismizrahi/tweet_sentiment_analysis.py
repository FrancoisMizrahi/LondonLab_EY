import twitter_api
import text_preprocessing
import sentiment_analysis


# comments

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
    keyword = input("Enter your keyword: ")
    max_results = input("How many Tweets do you want? (Between 10 and 100): ")
    print("Starting...")
    t = TweetsSentimentAnalysis(keyword=keyword, max_results=max_results)
    sentiments = t.get_tweets_sentiment_analysis()
    
    num_sentiments = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0}
    scores = []
    for result in sentiments:

        scores.append(float(result['score']))

        if result['label'] == 'POSITIVE':
            num_sentiments['POSITIVE'] += 1
        elif result['label'] == 'NEGATIVE':
            num_sentiments['NEGATIVE'] += 1
        else:
            num_sentiments['NEUTRAL'] += 1

    print("Results:")
    print(f"We found {num_sentiments['POSITIVE']} Positive Tweets")
    print(f"We found {num_sentiments['NEGATIVE']} Negative Tweets")
    print(f"We found {num_sentiments['NEUTRAL']} Neutral Tweets")
    print(f"The average sentiment score was {sum(scores) / len(scores)}. (1: Perfect positif, 0: Perfect Negatif)")