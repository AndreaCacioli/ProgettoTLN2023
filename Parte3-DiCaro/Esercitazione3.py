import csv
from nltk.corpus import wordnet
import spacy
from spacy import displacy
from progress_bar import InitBar
from nltk.wsd import lesk


def get_dictionary():
    semantic_types_path = "./Parte3-DiCaro/csi_inventory_semantictypes.tsv"
    dictionary = {}
    with open(semantic_types_path) as file:
        tsv_file = csv.reader(file, delimiter="\t")
        for line in list(tsv_file)[0:]:
            pos = line[0][-1]
            id = int(line[0][3:-1])
            synset = wordnet.synset_from_pos_and_offset(pos, id)
            try:
                dictionary[synset] = (line[1], line[2])
            except:
                dictionary[synset] = line[1]
    print("Acquired dictionary")
    return dictionary


CORPUS_PATH = "./Parte3-DiCaro/wiki_movie_plots_deduped.csv"


def print_token(token):
    print(
        token.text,
        token.lemma_,
        token.pos_,
        token.tag_,
        token.dep_,
        token.shape_,
        token.is_alpha,
        token.is_stop,
    )


def get_sentences(strings, target, target_pos):
    ret = []
    indexes = []
    nlp = spacy.load("en_core_web_sm")
    pbar = InitBar("Sentence Segmentation and filtering")
    for i, s in enumerate(strings):
        if target.lower() in s.split():
            doc = nlp(s)
            for sent in list(doc.sents):
                for token in sent:
                    if token.text.lower() == target.lower() and is_pos(
                        token, target_pos
                    ):
                        ret.append(sent)
                        indexes.append(i)
                        break
        pbar(i / len(strings) * 100)
    return ret, indexes


def is_pos(token, pos="VERB"):
    if token.pos_ == pos:
        return True
    return False


def get_sub_verb_obj(doc, target_verb):
    subject_ = ""
    object_ = ""

    for token in doc:
        if token.text.lower() == target_verb.lower():
            verb = token
            break
    else:
        print(f"Target verb '{target_verb}' not found in the sentence.")
        return subject_, object_

    for child in verb.children:
        if "subj" in child.dep_:
            subject_ = child.text
        if "obj" in child.dep_:
            object_ = child.text

    return (subject_, verb, object_)


def is_pronoun(string):
    return (
        string in ["I"]
        or string.lower() in ["you", "he", "she", "it", "we", "you", "they"]
        or string.lower() in ["your", "his", "hers", "its", "our", "their"]
        or string.lower() in ["him", "her", "them"]
    )


def get_synset(sentence, word):
    if is_pronoun(word):
        return "-PRON-"
    else:
        return lesk(sentence, word, "n")


def get_type(synset, dictionary):
    if type(synset) is str and synset == "-PRON-":
        return "PERSON"
    else:
        try:
            return dictionary[synset]
        except:
            return "UNKNOWN"


if __name__ == "__main__":
    strings = []
    TARGET = "watch"
    TARGET_POS = "VERB"
    with open(CORPUS_PATH) as file:
        csv_file = csv.reader(file)
        for line in list(csv_file)[1:]:
            strings.append(line[-1])

    sentences, indexes = get_sentences(strings, TARGET, TARGET_POS)
    tuples = []
    for sentence, i in zip(sentences, indexes):
        print(sentence)
        tuple = get_sub_verb_obj(sentence, TARGET)
        print(tuple)
        print()
        if tuple[0] != "" and tuple[2] != "":
            tuples.append((tuple, i))
    print("Loading semantic types...")
    dictionary = get_dictionary()
    print("Disambiguation of the tuples...")
    semantic_types_counts = {}
    for tuple, i in tuples:
        sentence = strings[i].split()
        subject_synset = get_synset(sentence, tuple[0])
        object_synset = get_synset(sentence, tuple[2])
        sub_type = get_type(subject_synset, dictionary)
        obj_type = get_type(object_synset, dictionary)
        try:
            semantic_types_counts[(sub_type, obj_type)] += 1
        except:
            semantic_types_counts[(sub_type, obj_type)] = 1
    semantic_types_counts = dict(
        sorted(semantic_types_counts.items(), key=lambda item: item[1], reverse=True)
    )
    print(semantic_types_counts)
