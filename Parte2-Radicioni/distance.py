from nltk.corpus import wordnet
from Lesk import simplifiedLesk


def bfs(start, goal):
    addedBy = {}
    visited = set([])
    queue = [start]
    while len(queue) > 0:
        print(f"length is now {len(queue)}")
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
    neighbours = []
    neighbours.extend(sense.hyponyms())
    neighbours.extend(sense.instance_hyponyms())
    neighbours.extend(sense.hypernyms())
    neighbours.extend(sense.instance_hypernyms())
    return neighbours


start = simplifiedLesk("thing", "")
end = simplifiedLesk("entity", "")

print(bfs(start, end))
input("Press Enter to continue...")

start = simplifiedLesk("rust", "")
end = simplifiedLesk("car", "")

print(bfs(start, end))
input("Press Enter to continue...")

start = simplifiedLesk("program", "")
end = simplifiedLesk("Jerusalem", "")

print(bfs(start, end))
input("Press Enter to continue...")
