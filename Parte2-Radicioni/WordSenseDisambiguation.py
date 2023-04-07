from csv import parse
from Lesk import simplifiedLesk
from nltk.corpus import wordnet

entries = parse("./Parte2-Radicioni/WordSim353.csv")

word1 = "hoop"
word2 = "basketball"

simplifiedLesk(word1, [word2])
