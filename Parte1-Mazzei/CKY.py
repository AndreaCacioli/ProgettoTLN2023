def parse(string, grammar):
    print("\n\tProcessing the string: \t" + string)
    print("\n")
    words = string.split()
    n = len(words)

    table = getSetMatrix(n, n)
    for j in range(n):
        word = words[j]
        print(f"Working on word \t {word}")
        for rule in grammar.productions():
            rhs = list(rule.rhs())
            if word in rhs:
                print(rule)


def getSetMatrix(rows, cols):
    table = [[{} for _ in range(cols)]] * rows
    for i in range(rows):
        for j in range(cols):
            table[i][j] = {}
    return table
