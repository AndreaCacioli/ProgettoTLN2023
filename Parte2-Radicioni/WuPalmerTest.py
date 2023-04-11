from WuPalmer import WuPalmerSimilarity
from csv import parse
from Lesk import simplifiedLesk
from termcolor import cprint

entries = parse("./Parte2-Radicioni/WordSim353.csv")


for entry in entries:
    try:
        sense1 = simplifiedLesk(entry[0], entry[1])
        sense2 = simplifiedLesk(entry[1], entry[0])
    except:
        print(f'Skipping words {entry[0]}, {entry[1]} because they are not considered nouns')
        continue
    print(f'Working on ', end = '')
    cprint(f'{entry[0]}','red', end = '')
    print(f', ', end = '')
    cprint(f'{entry[1]}','red', end = '')
    print()
    wu = WuPalmerSimilarity(sense1, sense2)
    cprint(f'Wu & Palmer Similarity index is {wu}','green')

    
    