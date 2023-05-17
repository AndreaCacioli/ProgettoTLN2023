from nltk.corpus import wordnet


def simplifiedLesk(word, context):
    maxOverlap = 0
    bestSense = None
    synsets = wordnet.synsets(word, wordnet.NOUN)
    if len(synsets) == 1:
        return synsets[0]
    if len(synsets) == 0:
        raise ValueError(f"There is no Noun synset in wordnet for {word}")
    for synset in synsets:
        definition = synset.definition()
        examples = synset.examples()
        bagOfWords = getBagOfWords(definition, examples)
        contextSet = set(context)
        if len(contextSet.intersection(bagOfWords)) > maxOverlap:
            bestSense = synset
    if bestSense is None:
        bestSense = synsets[0]
    return bestSense


def getBagOfWords(definition, examples):
    bag = set(definition.split())
    for example in examples:
        exampleSet = set(example.split())
        bag = bag.union(exampleSet)
    clean(bag)
    return bag


def clean(bag):
    temp = list(bag)
    for word in temp:
        if "(" in word or ")" in word:
            word = word.replace("(", "")
            word = word.replace(")", "")
            word = word.strip()
    bag = set(temp)
