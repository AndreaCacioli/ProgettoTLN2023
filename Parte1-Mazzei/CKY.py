from GraphNode import Node


def parse(string, grammar):
    print("\n\tProcessing the string: \t" + string)
    print("\n")
    words = string.split()
    n = len(words)

    table = getSetMatrix(n, n + 1)
    for j in range(0, n):
        word = words[j]
        word = cleanWord(word)
        wordNode = Node(word)

        rightSons = []
        for rule in getMatchingRulesRHS(grammar, word):
            head = lhs(rule)
            ruleNode = Node(head)
            wordNode.addParent(ruleNode)
            table[j][j + 1] = table[j][j + 1] | set([ruleNode])
            rightSons.append(head)

        for i in range(j - 1, -1, -1):
            # we go up the column we have currently updated
            for k in range(i + 1, 0, -1):
                for node in table[i][k]:
                    leftSon = node.name
                    # generate the couples
                    for rightSon in rightSons:
                        # find a rule that goes X -> leftSon rightSon
                        possibleParents = getMatchingRulesRHS(
                            grammar, leftSon, rightSon
                        )
                        for matchingRule in possibleParents:
                            parentNode = Node(lhs(matchingRule))
                            ruleNode.addParent(parentNode)
                            node.addParent(parentNode)
                            table[i][j + 1] = table[i][j + 1] | set([parentNode])
                            print("added a production head")
    return table


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
