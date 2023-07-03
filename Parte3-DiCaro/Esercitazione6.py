# Basicness sui synset di wordnet
# By using a crowdsourced dataset of senses cathegorised into two groups: basic and advanced we can determine if wordnet synsets are basic and advanced.
# Another dataset of bedtime stories is used to help us classify basic words
# while yet another dataset of scientific articles which is likely to contain words that are not used in bed-time stories helps us identify a advanced terms/senses.

import json
import os
from Esercitazione5 import preprocess
from nltk.wsd import lesk


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

    stories_preprocessed = []
    for story in stories_strings:
        story_preprocessed = preprocess([story])
        stories_preprocessed.append(story_preprocessed[0])
    return stories_preprocessed


def get_senses(stories):
    ret = []
    for story in stories:
        senses = []
        for term in story:
            sense = lesk(story, term)
            senses.append(sense)
        ret.append(senses)
    return ret

if __name__ == "__main__":
    print("Collecting Data from the json dataset...")
    PATH = "./Parte3-DiCaro/BasicAdvanced.json"
    BEDTIME_DIR = "./Parte3-DiCaro/Bed Time Stories"
    data = read_json_file(PATH)
    synsets_strings = data["dataset"]
    answers = data["answers"]
    time_diffs = data["timeDiffs"]
    for i in range(5):
        print(synsets_strings[i])
        print(answers[i])
        print(time_diffs[i])
    preprocessed_stories = read_bed_time_stories(BEDTIME_DIR)
    for i in range(3):
        print(preprocessed_stories[i][:20])
    basic_senses = get_senses(preprocessed_stories)
    for i in range(3):
        print(basic_senses[i][:10])
