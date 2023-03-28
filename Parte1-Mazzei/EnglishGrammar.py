from nltk import CFG
import CKY


englishGrammar = CFG.fromstring(
    """
        S -> NP VP
        S -> VP
        S -> X1 VP
        X1 -> Aux NP
        S -> book | include | prefer
        S -> Verb NP
        S -> X2 PP
        S -> Verb PP
        S -> VP PP
        NP -> Pronoun
        NP -> Proper-Noun
        NP -> Det Nominal
        Nominal -> Noun
        Nominal -> Nominal Noun
        Nominal -> Nominal PP
        VP -> Verb
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

string = "book the flight through Huston"

print(englishGrammar.productions())

CKY.parse(string, englishGrammar)
