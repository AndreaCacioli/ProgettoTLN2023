from csv import parse
from Lesk import simplifiedLesk
from termcolor import colored, cprint
from nltk.corpus import wordnet

entries = parse("./Parte2-Radicioni/WordSim353.csv")

word1 = "bank"
word2 = "river"

print()
w1Red = colored(word1, "red")
w2Green = colored(word2, "green")
print(f"Working on word {w1Red}, Synsets:")
for sense in wordnet.synsets(word1):
    print("----")
    print(sense.definition())
    print(sense.examples())
    print()

print(f"Working out the best sense of {w1Red} with {w2Green} as context...")
bestSense = simplifiedLesk(word1, [word2])

print()
cprint(f"The best sense is: {bestSense}", "green")
print(bestSense.definition())
print(bestSense.examples())
