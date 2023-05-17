from nltk.corpus import semcor
from Lesk import simplifiedLesk
from random import choice


def getSynset(elem):
    lemma = elem.label()
    synset = lemma.synset()
    return synset


def filter_by_pos(array, poses):
    ret = []
    for item in array:
        try:
            if item[0].label() in poses:
                ret.append(item)
        except:
            pass
    return ret


def get_word(tree_element):
    return tree_element[0][0]


def get_words_from_elements(context):
    ret = []
    for tree_element in context:
        ret.append(get_word(tree_element))
    return ret


if __name__ == "__main__":
    tagged_sents = semcor.tagged_sents(tag="both")
    TEST_SIZE = 90
    points = 0
    i = 0
    sentences_tested = 0
    while sentences_tested < TEST_SIZE:
        try:
            tagged_sent = tagged_sents[i]
            i += 1
            # filter nouns
            nouns = filter_by_pos(array=tagged_sent, poses=["NN"])
            target_noun = choice(nouns)
            target_synset = getSynset(target_noun)
            nouns_and_verbs = filter_by_pos(array=tagged_sent, poses=["NN", "VB"])
            index = nouns_and_verbs.index(target_noun)
            WINDOW = 2
            context = nouns_and_verbs[
                max(0, index - WINDOW) : min(len(nouns_and_verbs), index + WINDOW)
            ]
            context = get_words_from_elements(context)
            try:
                synset = simplifiedLesk(get_word(target_noun), context)
                if synset == target_synset:
                    points += 1
            # Happens when there is no noun in wordnet for a given term
            # Probably due to version mismatch
            except:
                continue
            sentences_tested += 1
        except:
            continue
    print(
        f"Your algorithm disambiguated correctly a total of {points} out of {TEST_SIZE} tests"
    )
    acc = points / TEST_SIZE * 100
    print(f"The accuracy is {acc}%")
