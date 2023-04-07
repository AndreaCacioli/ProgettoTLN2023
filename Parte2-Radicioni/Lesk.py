from nltk.corpus import wordnet


def simplifiedLesk(word, context):
    maxOverlap = 0
    for synset in wordnet.synsets(word):
        definition = synset.definition()
        examples = synset.examples()
        bagOfWords = getBagOfWords(definition, examples)
        contextSet = set(context)
        if len(contextSet.intersection(bagOfWords)) > maxOverlap:
            bestSense = synset
    return bestSense


def getBagOfWords(definition, examples):
    bag = set(definition.split())
    for example in examples:
        exampleSet = set(example.split())
        bag = bag.union(exampleSet)
    return bag
