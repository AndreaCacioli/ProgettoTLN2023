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



if __name__ == "__main__":
    definitions_path = './Parte3-DiCaro/TLN-definitions-23.tsv'
    minimum_definition_length = 1
    lemmatizer = WordNetLemmatizer()
    door_definitions = []
    ladybug_definitions = []
    pain_definitions = []
    blurriness_definitions = []

    with open(definitions_path) as file:
        tsv_file = csv.reader(file, delimiter="\t")
        for line in list(tsv_file)[1:]:
            filter_definition_by_size(door_definitions, line[1], minimum_definition_length)
            filter_definition_by_size(ladybug_definitions, line[2], minimum_definition_length)
            filter_definition_by_size(pain_definitions, line[3], minimum_definition_length)
            filter_definition_by_size(blurriness_definitions, line[4], minimum_definition_length)

    door_nouns_frequency = get_noun_occurrencies(door_definitions)
    ladybug_nouns_frequency = get_noun_occurrencies(ladybug_definitions)
    pain_nouns_frequency = get_noun_occurrencies(pain_definitions)
    blurriness_nouns_frequency = get_noun_occurrencies(blurriness_definitions)

    door_genuses = list({k: v for k, v in sorted(door_nouns_frequency.items(), key=lambda item: item[1], reverse = True)})
    ladybug_genuses = list({k: v for k, v in sorted(ladybug_nouns_frequency.items(), key=lambda item: item[1], reverse = True)})
    pain_genuses = list({k: v for k, v in sorted(pain_nouns_frequency.items(), key=lambda item: item[1], reverse = True)})
    blurriness_genuses = list({k: v for k, v in sorted(blurriness_nouns_frequency.items(), key=lambda item: item[1], reverse = True)})

    X = 5 # Il numero dei possibili genus da considerare. Gli X termini piú ricorrenti nelle definizioni
    door_genuses = door_genuses[:X]
    ladybug_genuses = ladybug_genuses[:X]
    pain_genuses = pain_genuses[:X]
    blurriness_genuses = blurriness_genuses[:X]

    MIN_PROF = 4 # la profonditá minima che deve avere un synset per poter essere considerato, se é meno profondo, ci rallenta troppo la ricerca.

    # Ora posso prendere i synset dei vari genus
    door_genuses_synsets = get_synsets_synset_with_min_prof(door_genuses, MIN_PROF)
    print(door_genuses_synsets)