from nltk.corpus import semcor
from nltk.corpus import wordnet

def getSynset(elem):
    lemma = elem.label()
    synset = lemma.synset()
    return synset

def getSqueezedString(sentence):
    string = ''
    for word in sentence:
        string = string + word
    return string

def getTaggedElements(sentence):
    sentence = getSqueezedString(sentence)
    tree = semcor.tagged_chunks(tag="both")
    leavesString = ''
    taggedElements = []
    i = 0
    while leavesString != sentence:
        elem = tree[i]
        leavesString += getSqueezedString(elem.leaves())
        taggedElements.append(elem)
        i += 1
        if isEndingElement(elem):
            if leavesString == sentence:
                return taggedElements
            leavesString = ''
            continue
    return None
        


def isEndingElement(elem):
    return elem.label() is None and elem.leaves()[0] == '.'

# TODO figure out why 23 crashes
N = 22

if __name__ == "__main__":
    for sentence in semcor.sents()[0:N]:
        elems = getTaggedElements(sentence)
        print(elems)
        print()
