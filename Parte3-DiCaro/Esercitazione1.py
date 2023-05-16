# Siccome non siamo macchine e non possiamo comunicare con gli embedding, usiamo i dizionari.

# Task: Calcolare l'overlap lessicale tra le definizioni.
import csv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def clean_sentence(example_sent):
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(example_sent)
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    return filtered_sentence


def add_definition(l, d):
    if len(d.split()) > len_thresh:
        d = clean_sentence(d)
        l.append(d)
    return l


def get_mean_overlap(definitions):
    sum = 0
    count = 0
    for i in range(len(definitions)):
        for j in range(i, len(definitions)):
            overlap = len(set(definitions[i]).intersection(set(definitions[j])))
            sum += overlap
            count += 1
    return float(sum / count)


if __name__ == "__main__":
    len_thresh = 5
    door_definitions = []
    ladybug_definitions = []
    pain_definitions = []
    blurriness_definitions = []

    with open("./Parte3-DiCaro/TLN-definitions-23.tsv") as file:
        tsv_file = csv.reader(file, delimiter="\t")

        for line in list(tsv_file)[1:]:
            add_definition(door_definitions, line[1])
            add_definition(ladybug_definitions, line[2])
            add_definition(pain_definitions, line[3])
            add_definition(blurriness_definitions, line[4])

    print(
        f"The average overlap between door definitions is:\t{get_mean_overlap(door_definitions)}"
    )
    print(
        f"The average overlap between ladybug definitions is:\t{get_mean_overlap(ladybug_definitions)}"
    )
    print(
        f"The average overlap between pain definitions is:\t{get_mean_overlap(pain_definitions)}"
    )
    print(
        f"The average overlap between blurriness definitions is:\t{get_mean_overlap(blurriness_definitions)}"
    )
