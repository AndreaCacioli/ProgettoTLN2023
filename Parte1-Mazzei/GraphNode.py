class Node:
    def __init__(self, name, parents=[], children=[]) -> None:
        self.name = name
        self.parents = []
        self.children = []
        for parent in parents:
            self.addParent(parent)
        for child in children:
            self.addChild(child)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def addParent(self, node):
        self.parents.append(node)
        if not self in node.children:
            node.addChild(self)

    def addChild(self, node):
        self.children.append(node)
        if not self in node.parents:
            node.addParent(self)

    def _printTreeString(self, level):
        print(f"{self.name}")
        for child in self.children:
            if level != 1:
                print("|", end="")
            print((level - 1) * "    " + "|____", end="")
            child._printTreeString(level + 1)

    def printTreeString(self):
        self._printTreeString(1)

    def getStringRec(self):
        if len(self.children) == 0:
            return self.name
        else:
            s = ""
            for child in self.children:
                s = child.getString() + " " + s
            return s

    def getString(self):
        s = self.getStringRec()
        words = s.split()
        s = ""
        for word in words:
            word = word.strip()
            s += word + " "
        return s.strip()
