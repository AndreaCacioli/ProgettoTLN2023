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
        synsets.append(synset)
    ret = []
    for i in range(len(synsets)):
        ret.append((synsets[i], answers[i], time_diffs[i]))
    global MIN
    global MAX
    MIN = min(time_diffs)
    MAX = max(time_diffs)
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


def compute_score(synset_tuple):
    threshold = 0.6
    result = synset_tuple[1]
    time_diff = synset_tuple[2]
    starting_score = 1 if result == "basic" else 0
    certainty = 1 - ((time_diff - MIN) / (MAX - MIN))
    if certainty > threshold:
        return starting_score
    if starting_score == 1:
        return certainty
    else:
        return 1 - certainty


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
    s = []
    for synset_tuple in synsets_with_judgement:
        s.append(synset_tuple[0])

    stories_preprocessed = read_bed_time_stories(BEDTIME_DIR)
    basic_senses = get_senses(stories_preprocessed)
    basic_senses_set = set([])
    for l in basic_senses:
        basic_senses_set = basic_senses_set.union(set(l))

    abstracts_preprocessed = get_abstracts_preprocessed(RESEARCH_ABSTRACTS_PATH)
    abstracts_senses = get_senses(abstracts_preprocessed)
    advanced_senses_set = set([])
    for l in abstracts_senses:
        advanced_senses_set = advanced_senses_set.union(set(l))

    scores = []

    for synset in synsets:
        # if it is in the json file we return its score
        if synset in s:
            index = s.index(synset)
            synset_tuple = synsets_with_judgement[index]
            scores.append(compute_score(synset_tuple))
        # if it is in a children story it is basic
        elif synset in basic_senses_set:
            scores.append(1)
        # if it is not in a children strory but it is in researches abstracts, then it is advanced
        elif synset in advanced_senses_set:
            scores.append(0)
        # if it is neither of the previous cases, we see how far it is from the synsets we have available
        else:
            scores.append(distance_score(synset, basic_senses_set, advanced_senses_set))
    return scores


def distance_score(synset, basic_senses_set, advanced_senses_set):
    PARAMETER = 0.3
    current_set = set([synset])
    i = 0
    while (
        len(current_set.intersection(basic_senses_set)) == 0
        and len(current_set.intersection(advanced_senses_set)) == 0
    ):
        current_set = expand(current_set)
        i += 1
    starting_score = (
        1
        if len(current_set.intersection(basic_senses_set))
        >= len(current_set.intersection(advanced_senses_set))
        else 0
    )
    final_score = starting_score / i if starting_score == 1 else 1 - (1 / i)
    return final_score


def expand(toBeExpanded):
    for sense in toBeExpanded:
        toBeExpanded = toBeExpanded.union(set(sense.hypernyms()))
        toBeExpanded = toBeExpanded.union(set(sense.instance_hypernyms()))
        toBeExpanded = toBeExpanded.union(set(sense.hyponyms()))
        toBeExpanded = toBeExpanded.union(set(sense.instance_hyponyms()))
    return toBeExpanded


if __name__ == "__main__":
    synsets = []
    synsets.append(wn.synset("dog.n.01"))
    synsets.append(wn.synset("union_shop.n.01"))
    synsets.append(wn.synset("weeder.n.01"))
    synsets.append(wn.synset("glow.n.05"))
    synsets.append(wn.synset("word.n.01"))
    synsets.append(wn.synset("bird.n.01"))
    synsets.append(wn.synset("wall.n.02"))
    synsets.append(wn.synset("atrocity.n.01"))
    synsets.append(wn.synset("largeness.n.01"))
    synsets.append(wn.synset("tree.n.01"))
    synsets.append(wn.synset("tree.n.02"))
    synsets.append(wn.synset("catamaran.n.01"))
    synsets.append(wn.synset("cooker.n.01"))
    synsets.append(wn.synset("fan.n.01"))  # Device for moving air
    synsets.append(wn.synset("fan.n.02"))  # Devout sport team lover
    synsets.append(wn.synset("elk.n.01"))
    synsets.append(wn.synset("growth.n.01"))
    scores = get_basicness_score(synsets)
    for synset, score in zip(synsets, scores):
        print(f"The synset: {synset} | {synset.definition()}\nhas a score of: {score}")
