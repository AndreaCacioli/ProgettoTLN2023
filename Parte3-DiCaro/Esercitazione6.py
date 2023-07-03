# Basicness sui synset di wordnet
# By using a crowdsourced dataset of senses cathegorised into two groups: basic and advanced we can determine if wordnet synsets are basic and advanced.
# Another dataset of bedtime stories is used to help us classify basic words
# while yet another dataset of scientific articles which is likely to contain words that are not used in bed-time stories helps us identify a advanced terms/senses.

import json
import os
from Esercitazione5 import preprocess
from nltk.wsd import lesk
from nltk.corpus import wordnet as wn
import pandas


def read_json_file(path):
    file = open(path)
    lines = file.readlines()
    string = "".join(lines)
    data = json.loads(string)
    synsets_strings = data["dataset"]
    answers = data["answers"]
    time_diffs = data["timeDiffs"]
    synsets = []
    for synset_string in synsets_strings:
        s = synset_string.split("(")
        s = s[1].split(")")[0]
        s = s[1 : len(s) - 1]
        synset = wn.synset(s)
        print(synset)
        synsets.append(synset)
    ret = []
    for i in range(len(synsets)):
        ret.append((synsets[i], answers[i], time_diffs[i]))
    return ret


def read_bed_time_stories(directory):
    paths = os.listdir(directory)
    stories_strings = []
    for path in paths:
        file = open(directory + "/" + path)
        lines = file.readlines()
        stories_strings.append("".join(lines))
    stories_preprocessed = preprocess(stories_strings)
    return stories_preprocessed


def get_senses(stories):
    ret = []
    for story in stories:
        senses = []
        for term in story:
            sense = lesk(story, term, pos="n")
            if sense is not None:
                senses.append(sense)
        ret.append(senses)
    return ret


def get_abstracts_preprocessed(path):
    abstracts_strings = pandas.read_csv(path)
    abstracts = abstracts_strings.loc[:, "ABSTRACT"].tolist()
    abstracts = abstracts[:500]
    abstracts_preprocessed = preprocess(abstracts)
    return abstracts_preprocessed


def get_basicness_score(synsets):
    """
    A simple function that returns a score in the interval [0:1] proportional to the basicness of a synset.
    A score of 0 means that the sense is *NOT* basic at all, while a score of 1 is a basic word

    :param ``synsets``: a list of WordNet synsets we want a basicness score of.
    :returns a list of scores relative to each synset of the list
    """
    PATH = "./Parte3-DiCaro/BasicAdvanced.json"
    BEDTIME_DIR = "./Parte3-DiCaro/Bed Time Stories"
    RESEARCH_ABSTRACTS_PATH = "./Parte3-DiCaro/Abstracts/ResearchAbstracts.csv"

    synsets_with_judgement = read_json_file(PATH)
    print(synsets_with_judgement)

    stories_preprocessed = read_bed_time_stories(BEDTIME_DIR)
    basic_senses = get_senses(stories_preprocessed)

    abstracts_preprocessed = get_abstracts_preprocessed(RESEARCH_ABSTRACTS_PATH)
    abstracts_senses = get_senses(abstracts_preprocessed)

    return 1


if __name__ == "__main__":
    synsets = []
    synsets.append(wn.synset("dog.n.01"))
    scores = get_basicness_score(synsets)
    print(scores)
