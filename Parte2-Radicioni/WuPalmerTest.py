from WuPalmer import WuPalmerSimilarity
from Tester import test
from nltk.corpus import wordnet

test(WuPalmerSimilarity, "Wu and Palmer Similarity index", wordnet.wup_similarity)
