from nltk import CFG
import CKY

klingonGrammar = CFG.fromstring(
    """
        S -> NP VP
        VP -> Verb NP
        VP -> Dajatlha | vIlegh | jIHtaH | maH 
        NP -> Adj Noun
        NP -> tlhIngan | Hol | puq | paDaq | jIH

        Adj -> tlhIngan
        Noun -> tlhIngan | Hol | puq | paDaq | jIH
        Verb -> Dajatlha | vIlegh | jIHtaH | maH 
"""
)

sentences = []
sentences.append("tlhIngan Hol Dajatlha")
sentences.append("puq vIlegh jIH")
sentences.append("paDaq jIHtaH")
sentences.append("tlhIngan maH")

for sentence in sentences:
    table = CKY.parse(sentence, klingonGrammar)
    for node in table[0][len(table)]:
        node.printTreeString()
        print()

