# LDA Algorithm
# This is a demo on how to use gensim's built in LDA algorithm in order to do a topic modelling task on a dataset containing game descriptions taken from Steam.

from nltk.corpus import stopwords

if __name__ == "__main__":
    PATH = './Parte3-DiCaro/games.csv'
    load_csv(PATH)