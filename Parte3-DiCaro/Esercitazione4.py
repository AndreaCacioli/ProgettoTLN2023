# Text Segmentation
# We need to write a program that differentiates between different topics written in the same file
import spacy

def read_file(path):
    separation = 0
    sentences = [[]]
    i = 0
    with open(path) as file:
        lines  = file.readlines()
        for line in lines:
            if line == '---':
                separation += 1
                i+=1
            else:
                sentences[i].append(line)


PATH = './Parte3-DiCaro/TextSegmentation.txt'

if __name__ == "__main__":
    read_file(PATH)
