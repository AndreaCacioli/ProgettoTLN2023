# Siccome non siamo macchine e non possiamo comunicare con gli embedding, usiamo i dizionari.

#Task: Calcolare l'overlap lessicale tra le definizioni.
import pandas as pd

df = pd.read_csv('Definitions.tsv', sep= '\t')
