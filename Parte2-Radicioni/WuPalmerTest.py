from WuPalmer import WuPalmerSimilarity
from csv import parse
from Lesk import simplifiedLesk
from termcolor import cprint
from scipy import stats

entries = parse("./Parte2-Radicioni/WordSim353.csv")

var1 = []
var2 = []

for entry in entries:
    try:
        sense1 = simplifiedLesk(entry[0], entry[1])
        sense2 = simplifiedLesk(entry[1], entry[0])
    except:
        print(
            f"Skipping words {entry[0]}, {entry[1]} because they are not considered nouns"
        )
        continue
    print(f"Working on ", end="")
    cprint(f"{entry[0]}", "red", end="")
    print(f", ", end="")
    cprint(f"{entry[1]}", "red", end="")
    print()
    wu = WuPalmerSimilarity(sense1, sense2)
    cprint(f"Wu & Palmer Similarity index is {wu}", "green")
    var1.append(entry[2])
    var2.append(wu)

print()
cprint("\t\tPEARSON CORRELATION", "magenta")
res = stats.pearsonr(var1, var2)
print(res)
print()

cprint("\t\tSPEARMAN CORRELATION", "magenta")
res = stats.spearmanr(var1, var2)
print(res)
print()
