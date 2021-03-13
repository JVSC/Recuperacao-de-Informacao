import json
import nltk
from nltk.tokenize import word_tokenize
from helpers import angle_distance

def pesquisa_vetorial(entrada):
    with open('./scoring/frequency_matrix.json') as f:
        frequency_matrix = json.load(f)
    with open("./indexed/config.json") as f:
        d = json.load(f)
        docs_len = len(d['doc_index'])
        docs_map = d['index_lookup']

    # ler entrada 
    # entrada = input("Busca: ")
    # entrada = "moça manca e gentil"
    entrada = word_tokenize(entrada.lower())
    busca = []
    for word in entrada:
        stopwords = nltk.corpus.stopwords.words('portuguese')
        if word in stopwords or not word.isalnum():
            continue
        else:
            busca.append(word)

    # Coordenadas do vetor para cada palavra na busca
    axis = list(set(busca))
    axis_map = {}
    for i in range(len(axis)):
        axis_map[axis[i]] = i

    docs = [[0 for x in range(len(axis))] for y in range(docs_len)]
    query = [0 for x in range(len(axis))]

    for x in busca:
        index = axis_map[x]
        query[index]+=1

    for index, doc in enumerate(docs):
        for x in axis:
            if x in frequency_matrix:
                doc[axis_map[x]] = frequency_matrix[x][index]

    lowest = {'index': 0, 'val':1000}
    for index, doc in enumerate(docs):
        angle = angle_distance(query, doc)
        print(f'documento: {doc}, busca: {query} - distancia: {angle}')
        if lowest['val'] > angle:
            lowest['index'] = index
            lowest['val'] = angle

    i = lowest['index']
    i = docs_map[str(i)]
    return i
    # print(f'Melhor resultado: {i}')