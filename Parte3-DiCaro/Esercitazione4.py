# Text Segmentation
# We need to write a program that differentiates between different topics written in the same file
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from progress_bar import InitBar
import itertools
import random


def read_file(path):
    separations = 0
    sentences = ""
    with open(path) as file:
        lines = file.readlines()
        for line in lines:
            if "---" in line:
                separations += 1
            else:
                sentences += line
    return sentences, separations


def preprocess(string):
    tokenizer = RegexpTokenizer(r"\w+")
    words = tokenizer.tokenize(string)
    stop_words = set(stopwords.words("english"))
    ret = []
    for word in words:
        if word not in stop_words:
            ret.append(word)
    return ret


def get_sections_from_comb(words, comb):
    sections = []
    last_indicator = 0
    for indicator in comb:
        sections.append(words[last_indicator:indicator])
        last_indicator = indicator
    sections.append(words[last_indicator:])
    return sections


def advanced_strategy(words, separations, iterations):
    start_iter = iterations
    size = len(words)
    comb = []
    extraction_range = size / separations
    sum = 0
    for i in range(separations):
        outcome = random.randint(0, extraction_range)
        sum += outcome
        comb.append(sum)

    scores = []
    pbar = InitBar("Refining the solution...")
    while iterations > 0:
        score = compute_score(get_sections_from_comb(words, comb))
        scores.append(score)
        selected_separator = random.randint(0, separations - 1)
        direction = random.choice(["left", "right"])
        step = calculate_step(scores)
        old_comb = comb.copy()
        if direction == "left":
            comb[selected_separator] -= step
        else:
            comb[selected_separator] += step
        new_score = compute_score(get_sections_from_comb(words, comb))
        if new_score < score:
            comb = old_comb
        iterations -= 1
        pbar((start_iter - iterations) / start_iter * 100)
    return comb, compute_score(get_sections_from_comb(words, comb))


def calculate_step(scores):
    if len(scores) < 5:
        return 1
    i = -2
    count = 0
    last_score = scores[-1]
    while True:
        score = scores[i]
        if score != scores:
            break
        else:
            i += 1
            count += 1

    return max(5 * count, 1)


def basic_strategy(words, separations):
    size = len(words)
    # Assumption: a text section will be at least 20 words long
    print(f"\tNumber of words: {size}")
    print(f"\tSeparations: {separations}")
    combs = list(itertools.combinations(range(20, size - 20), separations))
    pbar = InitBar("Trying all possible separations")
    best_comb = ()
    best_score = float("-inf")
    for i, comb in enumerate(combs):
        sections = get_sections_from_comb(words, comb)
        score = compute_score(sections)
        if score > best_score:
            best_score = score
            best_comb = comb
        pbar(i / len(combs) * 100)
    return best_comb, best_score


# gives a high score (0) if the sections do not share any words
# gives a low score (negative number) if the sections do share words
def compute_score(sections):
    score = 0
    for i in range(len(sections)):
        for j in range(i, len(sections)):
            section1 = sections[i]
            section2 = sections[j]
            overlap = len(set(section1).intersection(set(section2)))
            score -= overlap
    # To prevent small sections we divide the score by the size of the smallest one
    minimum_length_section = sections[0]
    for section in sections:
        if len(minimum_length_section) > len(section):
            minimum_length_section = section
    min_length = len(minimum_length_section)
    score /= min_length + 1

    # We give a point if the section contains duplicate words
    for section in sections:
        for target_word in set(section):
            for word in section:
                if word == target_word:
                    score += 1
    return score


PATH = "./Parte3-DiCaro/TextSegmentation-Electron-Flour-Window-Positivism-Purple.txt"
PATH = "./Parte3-DiCaro/TextSegmentation-Electron-Flour-Window-Positivism.txt"
PATH = "./Parte3-DiCaro/TextSegmentation-NBA-ArtNoveau-Cream.txt"

if __name__ == "__main__":
    print("Reading file...")
    sentences, separations = read_file(PATH)
    print("Preprocessing...")
    words = preprocess(sentences)
    size = len(words)
    print("Finding best separation...")
    best_comb, best_score = advanced_strategy(words, separations, 5000)
    print(f"The best separation was found in {best_comb}, with a score of {best_score}")
    sections = get_sections_from_comb(words, best_comb)
    for section in sections:
        print(section)
        print("---")
