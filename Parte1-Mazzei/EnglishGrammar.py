from nltk import CFG
import CKY

grammar = CFG.fromstring(
    """
        S -> NP VP
        S -> X1 VP
        X1 -> Aux NP
        Aux -> does | do
        NP -> I | she | me | you
        NP -> Huston | NWA
        NP -> Det Nominal
        NP -> Det Noun
        Nominal -> morning | quick | cool | adventurous | mountain | cold
        Nominal -> Nominal Noun
        Nominal -> Nominal PP
        Nominal -> X3 Nominal
        X3 -> X3 Nominal
        X3 -> morning | quick | cool | adventurous | mountain
        VP -> book | include | prefer | love | like | drink
        VP -> Verb Nominal
        VP -> Verb NP
        VP -> Verb PP
        VP -> X2 PP
        X2 -> Verb NP
        VP -> VP PP
        VP -> Adverb VP
        PP -> Preposition NP
        Det -> that | this | the | a
        Noun -> book | flight | meal | money | day | water
        Verb -> book | include | prefer | love | like | drink
        Pronoun -> I | she | me | you
        Proper-Noun -> Huston | NWA
        Preposition -> from | to | on | near | through
        Adverb -> Adv1 Adv2
        Adverb -> definitely | often | never | really | rarely
        Adv1 -> never | rarely
        Adv2 -> ever 
"""
)


strings = []
strings.append("I prefer the money")
strings.append("I book the flight")
strings.append("I book the flight through Huston")
strings.append("does she prefer a morning flight")
strings.append("I love a quick meal")
strings.append("do you like a cool adventurous mountain day")
strings.append("I really love that book")
strings.append("you definitely prefer Huston")
strings.append("you rarely ever drink cold water")

for string in strings:
    table = CKY.parse(string, grammar)
    for node in table[0][len(table)]:
        if node.name == "S" and node.getString() == string:
            node.printTreeString()
            print()
