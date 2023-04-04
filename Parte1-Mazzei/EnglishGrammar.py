from nltk import CFG
import CKY

dummyGrammar = CFG.fromstring(
    """
        S -> NP VP
        NP -> I | she | me
        NP -> Huston | NWA
        NP -> Det Nominal
        Nominal -> book | flight | meal | money
        Nominal -> Nominal PP
        VP -> book | include | prefer
        VP -> Verb NP
        VP -> Verb PP
        VP -> VP PP
        PP -> Preposition NP
        Det -> that | this | the | a
        Noun -> book | flight | meal | money
        Verb -> book | include | prefer
        Pronoun -> I | she | me
        Proper-Noun -> Huston | NWA
        Preposition -> from | to | on | near | through
"""
)

englishGrammar = CFG.fromstring(
    """
        S -> NP VP
        S -> X1 VP
        X1 -> Aux NP
        S -> book | include | prefer | is | prefer | like | need | want | fly | do
        S -> Verb NP
        S -> X2 PP
        S -> Verb PP
        S -> VP PP
        NP -> book | flight | meal | money | flights | breeze | trip | morning
        NP -> Huston 
        NP -> Det Nominal
        Nominal ->
        Nominal -> Nominal Noun
        Nominal -> Nominal PP
        VP -> book | include | prefer | is | prefer | like | need | want | fly | do
        VP -> Verb NP
        VP -> X2 PP
        X2 -> Verb NP
        VP -> Verb PP
        VP -> VP PP
        PP -> Preposition NP

        Det -> that | this | the | a | an | these
        Noun -> book | flight | meal | money | flights | breeze | trip | morning
        Verb -> book | include | prefer | is | prefer | like | need | want | fly | do
        Adjective -> cheapest | non-stop | first | latest | other | direct
        Pronoun -> I | she | me | you | it
        Proper-Noun -> Huston | NWA | Alaska | Baltimore | Los Angeles | Chicago | United | American
        Aux -> does
        Preposition -> from | to | on | near | through | in
"""
)

string = "does she prefer a morning flight"
string = "I book the flight through Huston"

table = CKY.parse(string, dummyGrammar)

for i in range(len(table)):
    for j in range(1, len(table) + 1):
        for node in list(table[i][j]):
            if node == "done":
                continue
            if len(node.parents) == 0:
                node.printTreeString()
                print()

print()
