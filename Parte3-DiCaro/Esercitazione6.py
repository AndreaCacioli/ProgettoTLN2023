# Basicness sui synset di wordnet
# By using a crowdsourced dataset of senses cathegorised into two groups: basic and advanced we can determine if wordnet synsets are basic and advanced.
# Another dataset of bedtime stories is used to help us classify basic words
# while yet another dataset of scientific articles which is likely to contain words that are not used in bed-time stories helps us identify a advanced terms/senses.

import json
import os
from Esercitazione5 import preprocess
from nltk.wsd import lesk
import pandas


def read_json_file(path):
    file = open(path)
    lines = file.readlines()
    string = "".join(lines)
    data = json.loads(string)
    return data


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


if __name__ == "__main__":
    print("Collecting Data from the json dataset...")
    PATH = "./Parte3-DiCaro/BasicAdvanced.json"
    BEDTIME_DIR = "./Parte3-DiCaro/Bed Time Stories"
    RESEARCH_ABSTRACTS_PATH = "./Parte3-DiCaro/Abstracts/ResearchAbstracts.csv"

    data = read_json_file(PATH)
    synsets_strings = data["dataset"]
    answers = data["answers"]
    time_diffs = data["timeDiffs"]
    for i in range(5):
        print(synsets_strings[i])
        print(answers[i])
        print(time_diffs[i])

    print()
    stories_preprocessed = read_bed_time_stories(BEDTIME_DIR)
    basic_senses = get_senses(stories_preprocessed)
    for i in range(3):
        print(stories_preprocessed[i][:20])
    for i in range(3):
        print(basic_senses[i][:10])

    print()
    abstracts_strings = pandas.read_csv(RESEARCH_ABSTRACTS_PATH)
    abstracts = abstracts_strings.loc[:, "ABSTRACT"].tolist()
    abstracts_preprocessed = preprocess(abstracts)
    abstracts_senses = get_senses(abstracts_preprocessed)
    for i in range(3):
        print(abstracts_preprocessed[i][:20])
    for i in range(3):
        print(abstracts_senses[i][:10])
