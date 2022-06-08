import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime, timedelta

from nltk.corpus import stopwords
from  nltk.stem import SnowballStemmer
import re

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential, load_model # Add 'load_model'
from joblib import dump, load # For reading the Tokenizer Pickle
import time

import os
from colorama import Fore
import platform
import requests
import time

model = load_model("data/model.h5")
tokenizer = load("data/tokenizer.pkl")

def yesterday_twitter_scapper(keyword):
    since = datetime.today() - timedelta(days=1)
    until = datetime.today()
    tweets_list = []
    print(f"{keyword} since:{since} until:{until}")
    tweets = sntwitter.TwitterSearchScraper(f"{keyword} lang:en since:{since.strftime('%Y-%m-%d')} until:{until.strftime('%Y-%m-%d')}")
    for i,tweet in enumerate(tweets.get_items()):
        tweets_list.append([tweet.date, tweet.id, tweet.content])
    return pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Text'])


def preprocess(text):
    text_cleaning_regex = "\r@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"
    stop_words = stopwords.words("english")
    text = re.sub(text_cleaning_regex, ' ', str(text).lower()).strip()
    tokens = []
    for token in text.split():
        if token not in stop_words:
            tokens.append(token)
    return " ".join(tokens)


def apply_preprocessing(df_series):
    df_series = df_series.apply(lambda x: preprocess(x))
    return df_series


def decode_sentiment(score):
    thresholds = (0.4, 0.7)
    label = "NEUTRAL"
    if score <= thresholds[0]:
        label = "NEGATIVE" 
    elif score >= thresholds[1]:
        label = "POSITIVE"
    return label


def make_prediction(text): 
    # Tokenize text
    x_test = pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=300)
    # Predict
    score = model.predict([x_test])[0]
    # Decode sentiment
    label = decode_sentiment(score)
    return {"label": label, "score": float(score)}


def apply_prediction(df_series):
    df_series = df_series.apply(lambda x: make_prediction(x))
    return df_series


def run_all(keyword):
    text = yesterday_twitter_scapper(keyword)
    text["clean_text"] = apply_preprocessing(text.Text)
    prediction = apply_prediction(text.clean_text)
    text["score"] = prediction.apply(lambda x: x["score"])
    text["label"] = prediction.apply(lambda x: x["label"])
    return text

def get_stats(text):
    result = {}
    result["neutral"] =  text[text['label'] == "NEUTRAL"]['label'].count()
    result["positive"] =  text[text['label'] == "POSITIVE"]['label'].count()
    result["negative"] =  text[text['label'] == "NEGATIVE"]['label'].count()
    result["mean_score"] = text['score'].mean()
    result["mean_label"] = decode_sentiment(result["mean_score"])
    return result


def unlimited(phone_num, msg):
    resp = requests.post('https://textbelt.com/text', {
    'phone': phone_num,
    'message': msg,
    'key': 'b1ab45b669921f880e5eea9540bfc72387fdbaa6WHDM60cY1xmLCzynUKSblYFhi',
    })
    print(resp.json())


if __name__ == '__main__':
    result = run_all("facebook data")
    stats = get_stats(result)
    sms_text = f"Hi, Yesterday the overall sentiment on twitter for Facebook data was {stats['mean_label']}, with an average sentiment score of {round(stats['mean_score'], 2)}. We found {stats['neutral']} neutral tweets, {stats['positive']} positive tweets and {stats['negative']} negative tweets. Group A7"
    # unlimited("+447428749957", sms_text)
    # unlimited("+447722128924", sms_text)

