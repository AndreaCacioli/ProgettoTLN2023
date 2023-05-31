import csv
from nltk.corpus import wordnet
from nltk.corpus import semcor
from nltk.tree import TreePrettyPrinter

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

def filter_by_pos(array, poses):
    ret = []
    for item in array:
        try:
            if item[0].label() in poses:
                ret.append(item)
        except:
            pass
    return ret

if __name__ == "__main__":

    tagged_sents = semcor.tagged_sents(tag="pos")
    TARGET = 'run'
    verbs = filter_by_pos(tagged_sents, ["VB"])
    dictionary = get_dictionary()