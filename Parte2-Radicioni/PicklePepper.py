from TrumpLM import get_markov_matrix, print_dictionary, generate_text, get_string_from_collection
dataset = [ ]

d1 = {}
d1["text"] ="<s> Peter Piper picked a peck of pickled pepper. </s>" 
dataset.append(d1)
d1 = {}
d1["text"] = "<s> Where's the pickled pepper that Peter Piper picked? </s>"
dataset.append(d1)

matrix = get_markov_matrix(corpus = dataset, N = 2)
string = generate_text(model=matrix, words_number=30, initial_window=["<s>"])
print()
print(get_string_from_collection( string))