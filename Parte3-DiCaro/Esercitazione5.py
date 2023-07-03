# LDA Algorithm
# This is a demo on how to use gensim's built in LDA algorithm in order to do a topic modelling task on a dataset containing game descriptions taken from Steam.

from nltk.corpus import stopwords
import pandas
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from gensim import corpora
import gensim
import pyLDAvis.gensim
import pyLDAvis
from progress_bar import InitBar


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
    print("Preprocessing...")
    texts = preprocess(texts)
    print("Calculating the dictionary...")
    dictionary = corpora.Dictionary(texts)
    pbar = InitBar("Calculating the term-document matrix")
    corpus = []
    for i, text in enumerate(texts):
        corpus.append(dictionary.doc2bow(text))
        pbar(i / len(texts) * 100)

    for i in range(20):
        print(texts[i][:10])
        print(corpus[i][:10])
    print("calculating the model...")
    model = gensim.models.ldamodel.LdaModel(
        corpus, num_topics=7, id2word=dictionary, passes=20
    )
    vis = pyLDAvis.gensim.prepare(model, corpus, dictionary)
    pyLDAvis.save_html(vis, "out.html")
