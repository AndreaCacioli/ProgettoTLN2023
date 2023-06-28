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
    f = True
    i = 0
    with open(path) as file:
        lines = file.readlines()
        for line in lines:
            if "---" in line:
                f = True
                separations += 1
            else:
                if f:
                    sentences += f"START{i}>"
                    i += 1
                f = False
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


def get_random_comb(words, separations):
    size = len(words)
    comb = []
    extraction_range = int(size / separations)
    sum = 0
    for _ in range(separations):
        outcome = random.randint(0, extraction_range)
        sum += outcome
        comb.append(sum)
    return comb


def advanced_strategy(words, separations, iterations):
    # start_iter = iterations
    comb = get_random_comb(words, separations)
    # pbar = InitBar("Refining the solution...")
    selected_separator = None
    direction = None
    rollback_counter = 0
    while iterations > 0:
        score = compute_score(get_sections_from_comb(words, comb))
        if score == float("-inf"):
            print("Restarting")
            comb = get_random_comb(words, separations)
            continue

        if selected_separator == None:
            selected_separator = random.randint(0, separations - 1)
        # True as a value for direction represents a LEFTWARD movement
        if direction == None:
            direction = random.choice([True, False])
        step = 1

        old_comb = comb.copy()
        comb, new_score = move(comb, selected_separator, direction, step)
        print(
            f"Comb = {comb} \t Separator #{selected_separator} went {direction} Score: {new_score} which is better? {new_score > score}"
        )
        if new_score < score:
            rollback_counter += 1
            print("Rolling Back...")
            comb = old_comb
            direction = None
            selected_separator = None
        else:
            rollback_counter = 0
            # Generally we have to try each separator twice (one for each direction)
            # If we tried twice the minimum required amount, we are stuck on a local minimum
            # So we add a perturbation
        if rollback_counter > separations * 2 * 2:
            rollback_counter = 0
            perturbation_magnitude = 10  # words
            perturbated_comb = []
            for indicator in comb:
                perturbated_comb.append(
                    random.randint(
                        indicator - perturbation_magnitude,
                        indicator + perturbation_magnitude,
                    )
                )
            print(
                f"Perturbating the comb\t old comb: {comb}, new comb: {perturbated_comb}"
            )
            comb = perturbated_comb

        iterations -= 1
        # pbar((start_iter - iterations) / start_iter * 100)
    return comb, compute_score(get_sections_from_comb(words, comb))


def move(comb, selected_separator, direction, step):
    if direction:
        comb[selected_separator] -= step
    else:
        comb[selected_separator] += step
    new_score = compute_score(get_sections_from_comb(words, comb))
    return comb, new_score


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


def compute_score(sections):
    # No 0-length sections
    for section in sections:
        if len(section) == 0:
            return float("-inf")
    score = 0
    for i in range(len(sections)):
        for j in range(i, len(sections)):
            section1 = sections[i]
            section2 = sections[j]
            overlap = len(set(section1).intersection(set(section2)))
            # make it a relative error
            overlap = overlap / len(section1)
            # give negative feedback
            score -= overlap

    # We give a point if the section contains duplicate words
    for section in sections:
        counts = {}
        size = len(section)
        for word in set(section):
            for selected_word in section:
                if selected_word == word:
                    try:
                        counts[word] += 1
                    except:
                        counts[word] = 1
        for key, value in counts.items():
            if value != 1:
                score += value / size

    # To prevent small sections we give a bad score to divisions that contain small sections
    minimum_length_section = sections[0]
    total_length = 0
    for section in sections:
        total_length += len(section)
        if len(minimum_length_section) > len(section):
            minimum_length_section = section
    min_length = len(minimum_length_section)
    if min_length < total_length / (2 * len(sections)):
        score -= total_length
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
    best_comb, best_score = advanced_strategy(words, separations, 500)
    print(f"The best separation was found in {best_comb}, with a score of {best_score}")
    sections = get_sections_from_comb(words, best_comb)
    for section in sections:
        print(section)
        print("---")
