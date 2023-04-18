from nltk.corpus import semcor
from nltk.corpus import wordnet
import random
from Lesk import simplifiedLesk

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
total_tested_sentences = 0
i = 0
sents = semcor.sents()

if __name__ == "__main__":
    while(total_tested_sentences < 50):
        sentence = sents[i]
        i += 1
        elems = getTaggedElements(sentence)
        if elems is not None:
            trovato = False
            while not trovato:
                randElement = random.choice(elems)
                try:
                    synset = getSynset(randElement)
                    if synset.pos() == wordnet.NOUN:
                        trovato = True
                except:
                    continue
            # We have the synset, let's try disambiguating it with close words
            span = 3 # 3 words left and 3 words right (when possible)
            termine = randElement.leaves()[0]
            print(termine)
            print(sentence)
            index = sentence.index(termine)
            print(f"Trovato {termine} index: {index}")
            context = sentence[max(0, index - span): min(len(sentence)-1, index + span)]
            disambiguation = simplifiedLesk(termine, context)
            total_tested_sentences +=1
            print(f"Succeded: {synset == disambiguation}")
            