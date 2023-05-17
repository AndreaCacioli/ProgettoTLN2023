from nltk.corpus import semcor
from Lesk import simplifiedLesk
from random import choice


def getSynset(elem):
    lemma = elem.label()
    synset = lemma.synset()
    return synset


def filter_by_pos(array, pos="N"):
    ret = []
    for item in array:
        if item.pos() == pos:
            ret.append(item)
    return ret


if __name__ == "__main__":
    tagged_sents = semcor.tagged_sents(tag="both")
    for i in range(len(tagged_sents)):
        tagged_sent = tagged_sents[i]
        # filter nouns
        nouns = filter_by_pos(array=tagged_sent, pos="N")
        print(nouns)
