from csv import parse
from scipy import stats
from Lesk import simplifiedLesk
from termcolor import cprint

results_list = []


def test(f, description, targetFunction=None):
    var1 = []
    var2 = []
    exacts = []
    entries = parse("./Parte2-Radicioni/WordSim353.csv")
    i = 0
    for entry in entries:
        i += 1
        print(i / len(entries) * 100)
        try:
            sense1 = simplifiedLesk(entry[0], [entry[1]])
            sense2 = simplifiedLesk(entry[1], [entry[0]])
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
        result = f(sense1, sense2)
        cprint(f"{description} is {result}", "green")
        if targetFunction is not None:
            exact = targetFunction(sense1, sense2)
            cprint(f"Target Function {exact}", "magenta")
            exacts.append(exact)

        var1.append(entry[2])
        var2.append(result)

    if targetFunction is not None:
        print()
        cprint("\t\tACCURACY", "magenta")
        corrects = 0
        for exact, result in zip(exacts, var2):
            if exact == result:
                corrects += 1
        print(corrects / len(exacts) * 100)
        print()

    print()
    cprint("\t\tPEARSON CORRELATION", "magenta")
    res = stats.pearsonr(var1, var2)
    print(res)
    print()

    cprint("\t\tSPEARMAN CORRELATION", "magenta")
    res = stats.spearmanr(var1, var2)
    print(res)
    print()
    return var1, var2
