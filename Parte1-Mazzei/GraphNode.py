class Node:
    def __init__(self, name, parents=[], children=[]) -> None:
        self.name = name
        self.parents = parents
        self.children = children

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
