import csv
from nltk.corpus import wordnet
import spacy

def get_dictionary():
    semantic_types_path = "./Parte3-DiCaro/csi_inventory_semantictypes.tsv"
    dictionary = {}
    with open(semantic_types_path) as file:
        tsv_file = csv.reader(file, delimiter="\t")
        for line in list(tsv_file)[0:]:
            pos = line[0][-1]
            id = int(line[0][3:-1])
            synset = wordnet.synset_from_pos_and_offset(pos,id)
            try:
                dictionary[synset] = (line[1], line[2])
            except:
                dictionary[synset] = (line[1])
    print("Acquired dictionary")
    return dictionary

CORPUS_PATH = "./Parte3-DiCaro/wiki_movie_plots_deduped.csv"

def print_token(token):
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)

if __name__ == "__main__":
    strings = []
    TARGET = 'see'
    with open(CORPUS_PATH) as file:
        csv_file = csv.reader(file)
        for line in list(csv_file)[1:]:
            strings.append(line[-1])
        
    nlp = spacy.load("en_core_web_sm")
    for i,s in enumerate(strings[0:2]):
        doc = nlp(s)
        print(f"SENTENCE {i}")
        for token in doc:
            print_token(token)
        print("-----------------")