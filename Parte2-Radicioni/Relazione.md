# Relazione Progetti semantica lessicale

Andrea Cacioli
Matricola: 914501

[TOC]

---

## Esercitazione 1 - WSD

Esercitazione sul word sense disambiguation utilizzando **Wordnet**.
In questa prima parte esercitazione era richiesta la disambiguazione tra termini a partire dal contesto utilizzando l'algoritmo di Lesk.

### Parte 1 - SemCor

A partire dal dataset SemCor, disponibile in NLTK, si é utilizzata **l'estrazione di nomi e verbi** della stessa frase da usare come contesto per l'algoritmo di Lesk.

Cosí facendo si ottiene una disambiguazione corretta dal 30% al 50% delle parole.

### Parte 2 - WordSim353

Utilizzando il dataset che contiene associazioni di parole annotati con la similaritá semantica si procede in questo modo:

- Disambiguazione dei due termini usando uno come contesto per l'altro
- Calcolo dei seguenti 3 coefficienti di Similaritá tra synset:
  - Indice di Wu e Palmer
  - Indice di Vicinanza Semantica
  - Indice di Leacock e Chodorow
- Calcolo dell'indice di correlazione di Pearson e Spearman (scipy)

