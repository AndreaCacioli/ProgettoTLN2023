Andrea Cacioli
===

[TOC]

# Progetto Tecnologie per il Linguaggio Naturale (Parte 1 - Linguistica Computazionale Generale)

## Consegna CKY: tlhIngan maH!
La consegna richiedeva di implementare l'algoritmo di riconoscimento CKY per l'identificazione di stringe generate da una grammatica libera dal contesto.
Tale algoritmo é un riconoscitore e in quanto tale si preoccupa solo di dire se esiste un albero che genera la stringa senza peró fornirlo.

Inoltre é richiesto di testare tale algoritmo su delle frasi inglesi a partire dalla grammatica L1 fornita nel Jurafsky.

Successivamente é richiesto che venga scritta una grammatica per la lingua Klingon per le sole frasi:
- tlhIngan Hol Dajatlh'a’? (Do you speak Klingon?)
- puq vIlegh jIH (I see the child)
- pa'Daq jIHtaH (I'm in the room)
- tlhIngan maH! (We are Klingon!)

## Sviluppo

### Fase 1 - Implementazione struttura dati e Algoritmo CKY

Per questo progetto ho deciso di non limitarmi al solo riconoscitore CKY che restituisce vero se una stringa appartiene al linguaggio generato da una grammatica, ma invece di implementare il parser completo che restituisce l'albero (o gli alberi) che genera una tale stringa.

Per fare tutto questo si é implementata una classe GraphNode che rappresenta un nodo di un grafo con peró delle peculiaritá:

- Un nodo ha dei figli
- Un figlio puó avere numerosi padri
- Figli diversi possono avere padri in comune

Tale struttura dati ci permetterá di trovare tutti gli alberi che un algoritmo genera a partire da un nodo start di una CFG.

Tale implementazione permette inoltre di avere una rappresentazione ad albero anche su terminale quando si stampa un nodo.

