############################################################################################################
# The Wu & Palmer similarity index:
#
# f(s1, s2) = ( 2 * depth(LCS) ) / ( depth(s1) + depth(s2) )
# s1 and s2 are the two senses we are analysing
# LCS is the Lowest Common Subsumer - The first sense we encounter when going "up" (hypernymy) the
#   tree
# The depth is the "distance" in terms of steps required to reach a sense starting from the sense
#   of the word 'entity'
#
############################################################################################################

from nltk.corpus import wordnet


def WuPalmerSimilarity(sense1, sense2):
    return (2 * depth(LCS(sense1, sense2))) / (depth(sense1) + depth(sense2))


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


def LCS(sense1, sense2):
    set1 = set([sense1])
    set2 = set([sense2])
    while len(set1.intersection(set2)) == 0:
        set1 = expand(set1)
        set2 = expand(set2)
    return maxDepth(set1.intersection(set2))


def expand(toBeExpanded):
    for sense in toBeExpanded:
        toBeExpanded = toBeExpanded.union(set(sense.hypernyms()))
        toBeExpanded = toBeExpanded.union(set(sense.instance_hypernyms()))
    return toBeExpanded


def maxDepth(list):
    maxDepth = 0
    maxElement = None
    for element in list:
        try:
            if depth(element) > maxDepth:
                maxElement = element
                maxDepth = depth(element)
        except:
            continue
    return maxElement
