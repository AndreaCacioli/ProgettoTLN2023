# Text Segmentation
# We need to write a program that differentiates between different topics written in the same file
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import itertools


def read_file(path):
    separations = 0
    sentences = ""
    with open(path) as file:
        lines = file.readlines()
        for line in lines:
            if "---" in line:
                separations += 1
            else:
                sentences += line
    return sentences, separations


def preprocess(string):
    tokenizer = RegexpTokenizer(r"\w+")
    words = tokenizer.tokenize(string)
    stop_words = set(stopwords.words("english"))
    ret = []
    for word in words:
        if word not in stop_words:
            ret.append(word)
    return ret


def basic_strategy(words, separations):
    size = len(words)
    list = [0] * size
    for i in range(separations):
        list[i] = 1
    combs = itertools.combinations(list, size)
    for comb in combs:
        print(comb)
    return combs


PATH = "./Parte3-DiCaro/TextSegmentation.txt"

if __name__ == "__main__":
    sentences, separations = read_file(PATH)
    words = preprocess(sentences)
    size = len(words)
    print(f"Working on a size of {size}")
    print(basic_strategy(words, separations))
