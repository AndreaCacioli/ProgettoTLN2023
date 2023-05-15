import csv
from itertools import product
import sys

with open("./Parte2-Radicioni/tweets.csv" ,encoding='utf8') as fp:
    reader = csv.reader(fp, delimiter=",", quotechar='"')
    next(reader, None)  # skip the headers
    data_read = [row for row in reader]

tweets = []

def get_string_from_collection(tuple):
    s = ""
    for t in tuple:
        s = s + t + " "
    return s.strip()

def remove_links(string):
    target = "https://"
    words = string.split()
    for i in range(len(words)):
        word = words[i]
        if word[0:len(target)] == target:
            words[i] = "<link>"
    return get_string_from_collection(words)

def remove_users(string):
    target = "@"
    words = string.split()
    for i in range(len(words)):
        word = words[i]
        if word[0:len(target)] == target:
            words[i] = "<user>"
    return get_string_from_collection(words)

def clean(string):
    string = remove_links(string)
    string = remove_users(string)
    return string

for i in range(len(data_read)):
    dictionary = {}
    dictionary["source"] = data_read[i][0]
    dictionary["text"] = f"<s> {data_read[i][1]} </s> "
    dictionary["text"] = clean(dictionary["text"])
    dictionary["created_at"] = data_read[i][2]
    dictionary["retweet_count"] = data_read[i][3]
    dictionary["favorite_count"] = data_read[i][4]
    dictionary["is_retweet"] = data_read[i][5]
    dictionary["id_str"] = data_read[i][6]
    tweets.append(dictionary)

#N-Grams
N = 2

def get_all_words(tweets):
    words = set()
    for d in tweets:
        text = d["text"]
        words = words.union(set(text.split()))
    return words

def get_big_string(tweets):
    ret = ""
    for dict in tweets:
        ret = ret + dict["text"]
    big_string = ret.split()
    return big_string


def get_markov_matrix(corpus = tweets, N = 2):
    matrix = {}
    words = get_all_words(corpus)
    big_string = get_big_string(corpus)
    combinations = product(words, repeat = N - 1) 
    size = (len(words) ** (N - 1)) * len(words)
    print(f"Working on a size of {size}")
    i = 0
    for combo in combinations:
        combo = get_string_from_collection(combo)
        matrix[combo] = {}
        for word in words:
            prob = get_probability(big_string, word, preceded_by = combo)
            matrix[combo][word] = prob
            i += 1
            print(f"\r{i} / {size}" , end='')
            sys.stdout.flush()
    return matrix

def get_probability(big_string, word, preceded_by):
    num =  count_occurrences(big_string, preceded_by + " " + word)
    den =  count_occurrences (big_string, preceded_by)
    if num == 0 or den == 0:
        return 0
    else: 
        return num / den

def count_occurrences(string, words):
    workingString = string
    target = words.split()
    count = 0
    for i in range(len(workingString ) - N):
        subvec = workingString[i:i+N]
        if subvec == target:
            count += 1
    return count


def decode(matrix):
    print(matrix)

if __name__ == "__main__":
    import pickle 
    try:
        print("Trying to recover file with markov matrix...")
        with open('saved_dictionary.pkl', 'rb') as f:
            dictionary = pickle.load(f)
    except:
        print(f"Could not open the file, recalculating {N}-grams")
        dictionary = get_markov_matrix(corpus = tweets, N = N)
        with open('saved_dictionary.pkl', 'wb') as f:
            pickle.dump(dictionary, f)
    print(dictionary)



            

