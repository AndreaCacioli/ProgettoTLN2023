# Siccome non siamo macchine e non possiamo comunicare con gli embedding, usiamo i dizionari.

#Task: Calcolare l'overlap lessicale tra le definizioni.

import nltk
import csv
len_thresh = 5

def add_definition(l, d):
    if len(d.split()) > len_thresh:
        l.append(d)
    return l
door_definitions = []
ladybug_definitions = []
pain_definitions = []
blurriness_definitions = []

with open("./Parte3-DiCaro/TLN-definitions-23.tsv") as file:
    tsv_file = csv.reader(file, delimiter="\t")
     
    for line in list(tsv_file)[1:]:
        add_definition(door_definitions, line[1])
        add_definition(ladybug_definitions, line[2])
        add_definition(pain_definitions, line[3])
        add_definition(blurriness_definitions, line[4])
print(ladybug_definitions)
door_sum = 0
door_count = 0
ladybug_sum = 0
ladybug_count = 0
pain_sum = 0
pain_count = 0
blurriness_sum = 0
blurriness_count = 0
d_c = []
l_c = []
p_c = []
b_c = []

for i in range(len(door_definitions)):
    for j in range (len(door_definitions)):
        if i != j and (i, j) not in d_c and (j, i) not in d_c:
            overlap = len(set(door_definitions[i].split()).intersection(set(door_definitions[j])))
            door_sum += overlap
            door_count += 1
            d_c.append((i, j))
door_mean = float(door_sum/door_count)

for i in range(len(ladybug_definitions)):
    for j in range (len(ladybug_definitions)):
        if i != j and (i, j) not in l_c and (j, i) not in l_c:
            overlap = len(set(ladybug_definitions[i].split()).intersection(set(ladybug_definitions[j])))
            ladybug_sum += overlap
            ladybug_count += 1
            l_c.append((i, j))

ladybug_mean = float(ladybug_sum/ladybug_count)

for i in range(len(pain_definitions)):
    for j in range (len(pain_definitions)):
        if i != j and (i, j) not in p_c and (j, i) not in p_c:
            overlap = len(set(pain_definitions[i].split()).intersection(set(pain_definitions[j])))
            pain_sum += overlap
            pain_count += 1
            p_c.append((i, j))
pain_mean = float(pain_sum/pain_count)

for i in range(len(blurriness_definitions)):
    for j in range (len(blurriness_definitions)):
        if i != j and (i, j) not in b_c and (j, i) not in b_c:
            overlap = len(set(blurriness_definitions[i].split()).intersection(set(blurriness_definitions[j])))
            blurriness_sum += overlap
            blurriness_count += 1
            b_c.append((i, j))
blurriness_mean = float(blurriness_sum/blurriness_count)

print(door_mean)
print(ladybug_mean)
print(pain_mean)
print(blurriness_mean)
