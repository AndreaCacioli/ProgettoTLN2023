from TrumpLM import get_markov_matrix, print_dictionary
dataset = [ ]

d1 = {}
d1["text"] ="<s> Peter Piper picked a peck of pickled pepper. </s>" 
dataset.append(d1)
d1 = {}
d1["text"] = "<s> Where's the pickled pepper that Peter Piper picked? </s>"
dataset.append(d1)

matrix = get_markov_matrix(corpus= dataset)
print()
print()
print_dictionary(matrix=matrix)