from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential, load_model # Add 'load_model'
from joblib import dump, load # For reading the Tokenizer Pickle
import time

class SentimentAnalysis:

    def __init__(self):
        self.KERAS_MODEL = "data/model.h5"
        self.TOKENIZER_MODEL = "data/tokenizer.pkl"

        self.SEQUENCE_LENGTH = 300
        
        self.POSITIVE = "POSITIVE"
        self.NEGATIVE = "NEGATIVE"
        self.NEUTRAL = "NEUTRAL"
        
        self.SENTIMENT_THRESHOLDS = (0.4, 0.7)
        
        # Load the model and the tokenizer to make predictions
        self.model = load_model(self.KERAS_MODEL)
        self.tokenizer = load(self.TOKENIZER_MODEL)

        self.start_at = time.time()


    def decode_sentiment(self, score, include_neutral=True):
        if include_neutral:        
            label = self.NEUTRAL
            if score <= self.SENTIMENT_THRESHOLDS[0]:
                label = self.NEGATIVE
            elif score >= self.SENTIMENT_THRESHOLDS[1]:
                label = self.POSITIVE
            return label
        else:
            return self.NEGATIVE if score < 0.5 else self.POSITIVE

    def predict(self, text, include_neutral=True):
        # Tokenize text
        x_test = pad_sequences(self.tokenizer.texts_to_sequences([text]), maxlen=self.SEQUENCE_LENGTH)
        # Predict
        score = self.model.predict([x_test])[0]
        # Decode sentiment
        label = self.decode_sentiment(score, include_neutral=include_neutral)

        return {"label": label, "score": float(score), "elapsed_time": time.time()-self.start_at}


if __name__ == '__main__':
    sentiment_analysis = SentimentAnalysis()
    print(sentiment_analysis.predict("I love the music"))
    print(sentiment_analysis.predict("I hate the music"))

