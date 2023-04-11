from nltk.corpus import wordnet


def simplifiedLesk(word, context):
    maxOverlap = 0
    bestSense = None
    for synset in wordnet.synsets(word):
        definition = synset.definition()
        examples = synset.examples()
        bagOfWords = getBagOfWords(definition, examples)
        contextSet = set([context])
        if len(contextSet.intersection(bagOfWords)) > maxOverlap:
            bestSense = synset
    if bestSense is None:
        bestSense = wordnet.synset(f'{word}.n.01')
    return bestSense


def getBagOfWords(definition, examples):
    bag = set(definition.split())
    for example in examples:
        exampleSet = set(example.split())
        bag = bag.union(exampleSet)
    clean(bag)
    return bag

def clean(bag):
    for word in bag:
        if '(' in word or ')' in word:
            bag.remove(word)
            word = word.replace('(', '')
            word = word.replace(')', '')
            bag.add(word)