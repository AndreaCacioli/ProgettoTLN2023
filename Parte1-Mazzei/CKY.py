def parse(string, grammar):
    print("\n\tProcessing the string: \t" + string)
    print("\n")
    words = string.split()
    n = len(words)

    table = getSetMatrix(n, n)
    for j in range(1, n):
        word = words[j]
        word = cleanWord(word)
        print(f"Working on word \t {word}")
        for rule in grammar.productions():
            rightHandSide = rhs(rule)
            if word in rightHandSide:
                table[j - 1][j] = table[j - 1][j] | {rule.lhs()}
        for i in range(j - 2, -1, -1):
            for k in range(i + 1, j):
                for rule in grammar.productions():
                    # TODO
                    # Add the proper if statement
                    if rule.is_lexical():
                        print(rule)
                        head = lhs(rule)
                        table[i][j] = table[i][j] | {head}
                print(f"k = {k}")
    return table


def getSetMatrix(rows, cols):
    table = [[set() for _ in range(cols)]] * rows
    for i in range(rows):
        for j in range(cols):
            table[i][j] = set()
    return table


def cleanWord(word):
    word = word.strip()
    word = word.lower()
    return word


def lhs(rule):
    return rule.lhs().symbol()


def rhs(rule):
    ret = []
    rhs = list(rule.rhs())
    for word in rhs:
        ret.append(word.symbol())
    return ret
