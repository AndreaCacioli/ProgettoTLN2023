import csv
from itertools import product
import sys


def get_string_from_collection(tuple):
    s = ""
    for t in tuple:
        s = s + t + " "
    return s.strip()


def replace(string, target, substitution):
    words = string.split()
    for i in range(len(words)):
        word = words[i]
        if word[0 : len(target)] == target:
            words[i] = substitution
    return get_string_from_collection(words)


def clean(string):
    string = replace(string, "http://", "<link>")
    string = replace(string, "https://", "<link>")
    string = replace(string, "@", "<user>")
    string = replace(string, ".@", "<user>")
    return string


def get_all_words(tweets):
    words = set()
    for d in tweets:
        text = d["text"]
        words = words.union(set(text.split()))
    return words


def get_big_string(tweets):
    ret = ""
    for dict in tweets:
        ret = ret + dict["text"] + " "
    big_string = ret.split()
    return big_string


def get_probability(big_string, word, preceded_by):
    num = count_occurrences(big_string, preceded_by + " " + word)
    den = count_occurrences(big_string, preceded_by)
    if num == 0 or den == 0:
        return 0
    else:
        return num / den


def count_occurrences(string, words):
    workingString = string
    target = words.split()
    count = 0
    for i in range(len(workingString) - len(target)):
        subvec = workingString[i : i + len(target)]
        if subvec == target:
            count += 1
    return count


def print_dictionary(matrix):
    for key, value in matrix.items():
        print(key, ":{")
        for innerKey, innerValue in value.items():
            if innerValue != 0:
                print(f"\t{innerKey}:\t {innerValue}", end="")
        print("}")


def is_valid_sentence(string):
    return not ",false," in string


tweets = []
with open("./Parte2-Radicioni/tweets.csv", encoding="utf8") as fp:
    reader = csv.DictReader(fp)
    for row in reader:
        row["text"] = clean(row["text"])
        if is_valid_sentence(row["text"]):
            tweets.append(row)

# N-Grams
N = 2


def get_markov_matrix(corpus=tweets, N=N):
    matrix = {}
    big_string = get_big_string(corpus)
    words = get_all_words(corpus)
    combinations = product(words, repeat=N - 1)
    size = (len(words) ** (N - 1)) * len(words)
    print(f"Working on a size of {size}")
    i = 0
    for combo in combinations:
        combo = get_string_from_collection(combo)
        matrix[combo] = {}
        for word in words:
            prob = get_probability(big_string, word, preceded_by=combo)
            matrix[combo][word] = prob
            i += 1
            print(f"\r{i} / {size}", end="")
            sys.stdout.flush()
    return matrix


if __name__ == "__main__":
    import pickle

    try:
        print("Trying to recover file with markov matrix...")
        with open("saved_dictionary.pkl", "rb") as f:
            dictionary = pickle.load(f)
    except:
        print(f"Could not open the file, recalculating {N}-grams")
        dictionary = get_markov_matrix(corpus=tweets, N=N)
        with open("saved_dictionary.pkl", "wb") as f:
            pickle.dump(dictionary, f)

    print_dictionary(dictionary)
