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
from Lesk import simplifiedLesk

def depth(sense):
    root = wordnet.synset('entity.n.01')
    i = 0
    path = []
    path.append(sense)
    hypernym = sense.hypernyms()[0]
    path.append(hypernym)
    while hypernym != root:
        hypernym = hypernym.hypernyms()[0]
        path.append(hypernym)
        i += 1
    return i, path

sense = simplifiedLesk('bank', 'financial')
print(depth(sense))
