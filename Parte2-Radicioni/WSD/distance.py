from nltk.corpus import wordnet
import math

MAX_DEPTH = 19


def index(sense1, sense2):
    return 2 * MAX_DEPTH - len(bfs(sense1, sense2))


def LeacockChodorow(sense1, sense2):
    return -math.log(len(bfs(sense1, sense2)) / (2 * MAX_DEPTH))


def bfs(start, goal):
    addedBy = {}
    visited = set([])
    queue = [start]
    while len(queue) > 0:
        current = queue.pop(0)
        if current == goal:
            return getPath(addedBy, start, goal)
        visited.add(current)
        for sense in getNeighbours(current):
            if sense not in visited and sense not in queue:
                queue.append(sense)
                addedBy[sense] = current


def getPath(addedByDictionary, start, goal):
    ret = []
    element = goal
    while element != start:
        ret.append(element)
        element = addedByDictionary[element]
    ret.append(start)
    ret.reverse()
    return ret


def getNeighbours(sense):
    neighbours = sense.hyponyms()
    neighbours.extend(sense.instance_hyponyms())
    neighbours.extend(sense.hypernyms())
    neighbours.extend(sense.instance_hypernyms())
    return neighbours


if __name__ == "__main__":
    from Lesk import simplifiedLesk
    from WuPalmer import maxDepth, depth

    print(depth(maxDepth(wordnet.all_eng_synsets())))

    start = simplifiedLesk("Jerusalem", [""])
    end = simplifiedLesk("Israel", [""])
    print(bfs(start, end))
    print()

    start = simplifiedLesk("rust", [""])
    end = simplifiedLesk("car", [""])
    print(bfs(start, end))
    print()
