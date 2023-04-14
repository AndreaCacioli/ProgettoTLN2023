from distance import LeacockChodorow, index
from Tester import test
from nltk.corpus import wordnet

#test(index, "Semantic distance")

test(LeacockChodorow, "Leacock and Chodorow index", wordnet.lch_similarity)
