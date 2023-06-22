import csv
from nltk.corpus import wordnet
import spacy
from spacy import displacy
from progress_bar import InitBar


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
                        break
        pbar(i / len(strings) * 100)
    return ret


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


if __name__ == "__main__":
    strings = []
    TARGET = "watch"
    TARGET_POS = "VERB"
    with open(CORPUS_PATH) as file:
        csv_file = csv.reader(file)
        for line in list(csv_file)[1:5000]:
            strings.append(line[-1])

    sentences = get_sentences(strings, TARGET, TARGET_POS)
    tuples = []
    for sentence in sentences:
        print(sentence)
        tuple = get_sub_verb_obj(sentence, TARGET)
        print(tuple)
        print()
        if tuple[0] != "" and tuple[2] != "":
            tuples.append(tuple)
    print(tuples)
