from nltk import CFG
import CKY


englishGrammar = CFG.fromstring(
    """
        S -> NP VP
        S -> X1 VP
        X1 -> Aux NP
        S -> Verb NP
        S -> X2 PP
        S -> Verb PP
        S -> VP PP
        NP -> I | she | me
        NP -> Huston | NWA
        NP -> Det Nominal
        Nominal -> book | flight | meal | money
        Nominal -> Nominal Noun
        Nominal -> Nominal PP
        VP -> book | include | prefer
        VP -> Verb NP
        VP -> X2 PP
        VP -> Verb PP
        VP -> VP PP
        X2 -> Verb NP
        PP -> Preposition NP
        Det -> that | this | the | a
        Noun -> book | flight | meal | money
        Verb -> book | include | prefer
        Pronoun -> I | she | me
        Proper-Noun -> Huston | NWA
        Aux -> does
        Preposition -> from | to | on | near | through
"""
)

string = "prefer the flight through Huston"

print(englishGrammar.productions())

table = CKY.parse(string, englishGrammar)

for i in range(len(table)):
    print()
    for j in range(1, len(table) + 1):
        print(f"\t {table[i][j]} \t\t\t", end="")


print()
