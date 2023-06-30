# LDA Algorithm
# This is a demo on how to use gensim's built in LDA algorithm in order to do a topic modelling task on a dataset containing game descriptions taken from Steam.

from nltk.corpus import stopwords
import pandas
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer


def preprocess(data):
    lowers = []
    for sentence in data:
        try:
            lowers.append(sentence.lower())
        except:
            continue
    tokenizer = RegexpTokenizer(r"\b[^\d\W]+\b")
    tokenized_sentences = []
    for lower_sentence in lowers:
        tokens = tokenizer.tokenize(lower_sentence)
        tokenized_sentences.append(tokens)

    no_stopwords_sentences = []
    stop_words = set(stopwords.words("english"))
    for sentence in tokenized_sentences:
        filtered = []
        for token in sentence:
            if token not in stop_words:
                filtered.append(token)
        no_stopwords_sentences.append(filtered)

    ret = []
    lemmatizer = WordNetLemmatizer()
    for sentence in no_stopwords_sentences:
        lemmas = []
        for token in sentence:
            lemmas.append(lemmatizer.lemmatize(token))
        ret.append(lemmas)

    return ret


if __name__ == "__main__":
    PATH = "./Parte3-DiCaro/games.csv"
    df = pandas.read_csv(PATH)
    texts = df.loc[:, "About the game"].tolist()
    texts = preprocess(texts[:100])
    for i in range(20):
        print(texts[i][:10])
