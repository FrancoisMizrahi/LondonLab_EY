import text_preprocessing
import sentiment_analysis

import pandas as pd
import time
import glob
import os


def clean_tweets(series):
    preprocessing = text_preprocessing.TextPreprocessing()
    return preprocessing.apply_preprocessing(series)

def get_sentiments(series):
    start = time.time()
    sent_analysis = sentiment_analysis.SentimentAnalysis()
    result = series.apply(lambda x: sent_analysis.predict(x))
    end = time.time()
    print(f"Finished in: {str((end - start)/60)} minutes")
    return result

# # setting the path for joining multiple files
# files = os.path.join("/Users/francoismizrahi/Documents/LBS/Courses/London Lab/data/tweets/", "eng_facebook_data*.csv")
# files = glob.glob(files)

# for file in files:
#     print(file)
#     df = pd.read_csv(file)
#     print(f"Number of tweets to process: {len(df)}")
#     df.Text = clean_tweets(df.Text)
#     Sent = get_sentiments(df.Text)
#     df["label"] = Sent.apply(lambda x: x["label"])
#     df["score"] = Sent.apply(lambda x: x["score"])
#     df["elapsed_time"] = Sent.apply(lambda x: x["elapsed_time"])
#     df.to_csv(f"data/clean_tweets/clean_{file[-43:]}")


df = pd.read_csv("/Users/francoismizrahi/Documents/LBS/Courses/London Lab/data/tweets/eng_facebook_data_2018-01-01_2018-01-31.csv",
    lineterminator='\n')
print(f"Number of tweets to process: {len(df)}")
df.Text = clean_tweets(df.Text)
Sent = get_sentiments(df.Text)
df["label"] = Sent.apply(lambda x: x["label"])
df["score"] = Sent.apply(lambda x: x["score"])
df["elapsed_time"] = Sent.apply(lambda x: x["elapsed_time"])
df.to_csv(f"data/clean_tweets/clean_eng_facebook_data_2018-01-01_2018-01-31.csv")
