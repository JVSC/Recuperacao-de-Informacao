import nltk
from _invertedIndex import parse_corpus, inverted_index

docs = parse_corpus()
index = inverted_index(docs['corpus'], docs['termos'])

for i in index:
    print(f'indice: {i} - {index[i]}')