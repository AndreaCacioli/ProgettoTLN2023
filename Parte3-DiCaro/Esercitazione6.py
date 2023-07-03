# Basicness sui synset di wordnet
# By using a crowdsourced dataset of senses cathegorised into two groups: basic and advanced we can determine if wordnet synsets are basic and advanced.
# Another dataset of bedtime stories is used to help us classify basic words
# while yet another dataset of scientific articles which is likely to contain words that are not used in bed-time stories helps us identify a advanced terms/senses.

import json


def read_json_file(path):
    file = open(path)
    lines = file.readlines()
    string = "".join(lines)
    data = json.loads(string)
    return data


if __name__ == "__main__":
    print("Collecting Data from the json dataset...")
    PATH = "./Parte3-DiCaro/BasicAdvanced.json"
    data = read_json_file(PATH)
    synsets_strings = data["dataset"]
    answers = data["answers"]
    time_diffs = data["timeDiffs"]
    for i in range(10):
        print(synsets_strings[i])
        print(answers[i])
        print(time_diffs[i])
