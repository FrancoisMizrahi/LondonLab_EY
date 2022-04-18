from nltk.corpus import stopwords
from  nltk.stem import SnowballStemmer
import re


class TextPreprocessing:

    def __init__(self):
        # Text Cleaning
        self.text_cleaning_regex = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"
        # Stop words are filler words that are not supposed to add values to the sentence
        self.stop_words = stopwords.words("english")
        # Stemmer allows to only go back to the root of the words
        self.stemmer = SnowballStemmer("english")

    def preprocess(self, text, stem = False, keep_stop_words = []):
        """
        Create a function to clean text
        We use the regular expression defined in settings
        We leave the option to use the stemmer or not
        """
        if keep_stop_words:
            for word in keep_stop_words:
                keep_stop_words.remove(word)

        text = re.sub(self.text_cleaning_regex, ' ', str(text).lower()).strip()
        tokens = []
        for token in text.split():
            if token not in self.stop_words:
                if stem:
                    tokens.append(self.stemmer.stem(token))
                else:
                    tokens.append(token)
        return " ".join(tokens)

    def apply_preprocessing(self, df, stem = False, keep_stop_words = []):
        df.text = df.text.apply(lambda x: self.preprocess(x, stem, keep_stop_words))
        return df

if __name__ == '__main__':
    preprocessing = TextPreprocessing()
    print(preprocessing.preprocess("@@ Hello word", stem = False, keep_stop_words = []))