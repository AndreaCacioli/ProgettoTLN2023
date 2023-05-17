from distance import LeacockChodorow
from Tester import test
from nltk.corpus import wordnet

test(LeacockChodorow, "Leacock and Chodorow index", wordnet.lch_similarity)
