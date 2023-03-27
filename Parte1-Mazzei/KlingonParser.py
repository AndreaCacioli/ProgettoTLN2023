from nltk import CFG

grammar = CFG.fromstring("""
        S -> NP VP
        PP -> P NP
        NP -> Det N | NP PP
        VP -> V NP | VP PP
        Det -> 'a' | 'the'
        N -> 'dog' | 'cat'
        V -> 'chased' | 'sat'
        P -> 'on' | 'in'
                         """)

print(grammar.productions())
