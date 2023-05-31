# Definitions

# L'obiettivo è quello di cercare per ogni definizione il set dei genus, ovvero un supertipo dell'oggetto definito. Sono i sostantivi più frequenti nelle varie definizioni del corpus. Una volta fatto ciò, scelgo il genus più preciso (in funzione di un punteggio di similarità fra la sua descrizione e la definizione con cui voglio disambiguare), mi posiziono sul suo nodo dell'albero di wordnet, e controllo nei suoi figli (tutti) quale abbia la definizione più vicina al set di parole che ho nella mia definizione dell'oggetto che cerco.
# Scelgo come parola il genus con punteggio migliore.

from nltk.corpus import wordnet
from nltk import word_tokenize
import nltk
import csv
import numpy as np
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def get_specific_synsets(synsets):
    ret = []
    for synset, depth in synsets:
        differentia = expand(synset)
        ret.extend(differentia)
    return ret
    

def expand(synset):
    hyponims = synset.hyponyms()
    if len(hyponims) == 0:
            return [synset]
    else:
        senses = []
        for hyponim in hyponims:
            for sense in expand(hyponim):
                senses.append(sense)
        return senses


def depth(sense):
    root = wordnet.synset("entity.n.01")
    if sense == root:
        return 1
    i = 1
    if len(sense.hypernyms()) == 0:
        hypernym = sense.instance_hypernyms()[0]
    else:
        hypernym = sense.hypernyms()[0]
    while hypernym != root:
        hypernym = hypernym.hypernyms()[0]
        i += 1
    return i + 1

def filter_definition_by_size(collection, definition, minimum_length):
    if len(definition.split()) > minimum_length:
        collection.append(definition)
    return collection

# Restituisce un dizionario con key un nome che appare in una definizione e value il numero di volte in cui appare
def get_noun_occurrencies(collection):
    nouns = []
    for definition in collection:
        tokens = word_tokenize(definition)
        tags = nltk.pos_tag(tokens, tagset='universal')
        nouns.append([x for ii, x in enumerate(tokens) if tags[ii][1] == 'NOUN'])
    
    nounset = {}
    for i in range(len(nouns)):
        for j in range(len(nouns[i])):
            try:
                nounset[nouns[i][j]] += 1
            except:
                nounset[nouns[i][j]] = 1
            
    return nounset

def get_synsets_synset_with_min_prof(terms, minProf):
    ret = []
    for term in terms:
        synsets = wordnet.synsets(term, wordnet.NOUN)
        for synset in synsets:
            syndepth = depth(synset)
            if syndepth >= minProf:
                ret.append((synset, syndepth))
    return ret

def clean(bag):
    temp = list(bag)
    for word in temp:
        if "(" in word or ")" in word:
            word = word.replace("(", "")
            word = word.replace(")", "")
            word = word.strip()
    bag = set(temp)

def get_bag_of_words_from_synset(synset):
    definition = synset.definition()
    examples = synset.examples()
    bag = set(definition.split())
    for example in examples:
        exampleSet = set(example.split())
        bag = bag.union(exampleSet)
    clean(bag)
    return bag

def get_bag_of_words_from_collection(definitions):
    ret = set([])
    for definition in definitions:
        ret = ret.union(set(definition.split()))
    return ret

def get_score(synset, bag_of_words):
    s1 = get_bag_of_words_from_synset(synset)
    return len(s1.intersection(bag_of_words))

def get_scores(synsets, bag_of_words):
    ret = {}
    for synset in synsets:
        score = get_score(synset, bag_of_words)
        ret[synset] = score
    return ret

def sort_dictionary_by_value(dictionary):
    return list({k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse = True)})


def guess_by_definitions(definitions, X = 5, MIN_PROF = 4, SHOW = 10):
    nouns = get_noun_occurrencies(definitions)
    sorted_nouns = sort_dictionary_by_value(nouns)
    genuses = sorted_nouns[:X]
    genuses_synsets = get_synsets_synset_with_min_prof(genuses, MIN_PROF)
    differentia = get_specific_synsets(genuses_synsets)
    bag_of_words = get_bag_of_words_from_collection(definitions)
    scores = get_scores(differentia, bag_of_words)
    scores_keys = sort_dictionary_by_value(scores)
    ret = []
    for i in range(SHOW):
        ret.append((scores_keys[i], scores[scores_keys[i]]))
    return ret

if __name__ == "__main__":
    definitions_path = './Parte3-DiCaro/TLN-definitions-23.tsv'
    minimum_definition_length = 9
    lemmatizer = WordNetLemmatizer()
    door_definitions = []
    ladybug_definitions = []
    pain_definitions = []
    blurriness_definitions = []
    definitions = [door_definitions, ladybug_definitions, pain_definitions, blurriness_definitions]

    with open(definitions_path) as file:
        tsv_file = csv.reader(file, delimiter="\t")
        for line in list(tsv_file)[1:]:
            filter_definition_by_size(door_definitions, line[1], minimum_definition_length)
            filter_definition_by_size(ladybug_definitions, line[2], minimum_definition_length)
            filter_definition_by_size(pain_definitions, line[3], minimum_definition_length)
            filter_definition_by_size(blurriness_definitions, line[4], minimum_definition_length)

    print("Guessing:\tDoor, ladybug, pain, blurriness")
    for definition_collection in definitions:
        for guess in guess_by_definitions(definition_collection):
            print(guess)
        print()

    