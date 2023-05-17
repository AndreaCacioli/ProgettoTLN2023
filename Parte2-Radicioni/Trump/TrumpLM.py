import csv
import random
from termcolor import cprint


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
    string = "<s> " + string
    string = string + " </s>"
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


def print_model(matrix):
    for key, value in matrix.items():
        cprint(f"{key}", color="red")
        for innerKey, innerValue in value.items():
            cprint(f"{innerKey}:{innerValue}\t", end="", color="green")
        print()


def is_valid_sentence(string):
    return not ",false," in string and not "Android" in string and not "&amp;" in string


NO_EVENT = "</NoEvent>"


# Given a dictionary of outcomes and their probabilities return a random outcome based on those probabilities
def simulate_random_variable(distribution):
    cumulative = []
    outcomes = []
    sum = 0
    GRANULARITY = 100000
    for key, value in distribution.items():
        if value > 1 or sum > GRANULARITY:
            raise ValueError("The dictionary must contain a probability distribution")
        if value > 0:
            sum += value * GRANULARITY
            cumulative.append(sum)
            outcomes.append(key)
    if sum == 0:
        return NO_EVENT
    if sum < GRANULARITY - 0.1 * GRANULARITY:
        raise ValueError("The dictionary must contain a probability distribution")
    res = random.randint(0, GRANULARITY)
    i = 0
    while res > cumulative[i]:
        i += 1
    return outcomes[i]


def generate_text(model, words_number, initial_window):
    n = len(list(model.keys())[0].split())
    if len(initial_window) != n:
        raise IndexError(
            "The length of the starting sequence is incompatible with the model"
        )
    window = initial_window
    ret = []
    for item in initial_window:
        ret.append(item)
    while len(ret) < words_number:
        string = get_string_from_collection(window)
        probability = model[string]
        next_word = simulate_random_variable(probability)
        if next_word == NO_EVENT:
            ret.append("</s>")
            return get_string_from_collection(ret)
        window.pop(0)
        window.append(next_word)
        ret.append(next_word)
    return get_string_from_collection(ret)


tweets = []
with open("./Parte2-Radicioni/Trump/tweets.csv", encoding="utf8") as fp:
    reader = csv.DictReader(fp)
    for row in reader:
        row["text"] = clean(row["text"])
        if is_valid_sentence(row["text"]):
            tweets.append(row)


def get_random_initial_window(corpus, N):
    prob_distr = {}
    sum = 0
    for dic in corpus:
        text = dic["text"]
        text = text.split()
        start = text[0:N - 1]
        start_string = get_string_from_collection(start)
        try:
            prob_distr[start_string] += 1
        except:
            prob_distr[start_string] = 1
        sum += 1
    for key, value in prob_distr.items():
        prob_distr[key] = value / sum
    return simulate_random_variable(prob_distr).split()
        

def get_markov_matrix_fast(corpus, N):
    model = {}
    countsN = {}
    countsN_1 = {}
    big_string_array = get_big_string(corpus)
    for i in range(len(big_string_array) - N):
        Nsubs = get_string_from_collection(big_string_array[i : i + N])
        N_1subs = get_string_from_collection(big_string_array[i : i + N - 1])
        try:
            countsN[Nsubs] += 1
        except:
            countsN[Nsubs] = 1
        try:
            countsN_1[N_1subs] += 1
        except:
            countsN_1[N_1subs] = 1
    for bigger, num in countsN.items():
        smaller = get_string_from_collection(
            bigger.split()[0 : len(bigger.split()) - 1]
        )
        nth_word = bigger.split()[-1]
        det = countsN_1[smaller]
        try:
            model[smaller][nth_word] = num / det
        except:
            model[smaller] = {}
            model[smaller][nth_word] = num / det

    return model


if __name__ == "__main__":
    N = 3
    dictionary = get_markov_matrix_fast(corpus=tweets, N=N)
    print()
    window = get_random_initial_window(tweets, N)
    print(generate_text(dictionary, words_number=50, initial_window=window))
