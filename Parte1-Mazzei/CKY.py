from GraphNode import Node


def fillInDiagonal(grammar, word, wordNode, table, j):
    rightSons = []
    for rule in getMatchingRulesRHS(grammar, word):
        head = lhs(rule)
        ruleNode = Node(head)
        wordNode.addParent(ruleNode)
        table[j][j + 1] = table[j][j + 1] | set([ruleNode])
        rightSons.append(ruleNode)
    return rightSons


def parse(string, grammar):
    print("\n\tProcessing the string: \t" + string)
    words = string.split()
    n = len(words)
    table = getSetMatrix(n, n + 1)

    for j in range(0, n):
        word = words[j]
        word = cleanWord(word)
        wordNode = Node(word)

        rightSons = fillInDiagonal(grammar, word, wordNode, table, j)
        for i in range(j - 1, -1, -1):
            # we go up the column we have currently updated
            for l in range(n - 1, i, -1):
                rightSons = table[l][j + 1]
                for k in range(1, j + 1):
                    for leftSon in table[i][k]:
                        # generate the couples
                        for rightSon in rightSons:
                            # find a rule that goes X -> leftSon rightSon
                            possibleParents = getMatchingRulesRHS(
                                grammar, leftSon.name, rightSon.name
                            )
                            for matchingRule in possibleParents:
                                createAndAddNewNode(
                                    matchingRule, table, i, j, rightSon, leftSon
                                )
    return table


def createAndAddNewNode(matchingRule, table, i, j, rightSon, leftSon):
    parentNode = Node(lhs(matchingRule))
    rightSon.addParent(parentNode)
    leftSon.addParent(parentNode)
    table[i][j + 1] = table[i][j + 1] | set([parentNode])


def getMatchingRulesRHS(grammar, word1, word2=None):
    ret = []
    for rule in grammar.productions():
        right = rhs(rule)
        if word1 in right and (word2 == None or word2 in right):
            if word2 == None:
                ret.append(rule)
            else:
                if word1 == right[0] and word2 == right[1]:
                    ret.append(rule)
    return ret


def getSetMatrix(rows, cols):
    table = []
    for i in range(rows):
        table.append([])
        for _ in range(cols):
            table[i].append(set())
    return table


def cleanWord(word):
    word = word.strip()
    return word


def lhs(rule):
    return rule.lhs().symbol()


def rhs(rule):
    ret = []
    right = list(rule.rhs())
    for word in right:
        str = word.symbol()
        str = cleanWord(str)
        ret.append(str)
    return ret
