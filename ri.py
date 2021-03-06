#ATENÇÃO
#Realizamos a incluusão da obra através do método de
#download da biblioteca NLTK

import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import RSLPStemmer

from os import listdir
from os.path import isfile, join
import json

mypath = './Obras'

def rem_dup(seq, idfun=None): 
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result

temporario = []

def inverted_index(sentencas_processadas, terms):
    inverted_index = dict()
    print(f'Termos: {len(terms)}, sentenças: {len(sentencas_processadas)}')
    i = 0
    for term in terms:
        inverted_index[term] = {"obras":[], "sentencas": []}
        for index, sentenca in enumerate(sentencas_processadas):
            for i, s in enumerate(sentenca['sentencas']):                
                if term in s:
                    inverted_index[term]["obras"].append(sentenca['id'])
                    inverted_index[term]["sentencas"].append((sentenca['id'], i))
        i = i +1 
    return inverted_index

def rem_dup_index(inverted_index, terms):
    for term in terms:
        inverted_index[term]['obras'] = list(dict.fromkeys(inverted_index[term]['obras']))
    return inverted_index

#nltk.download('machado')
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('rslp')

documentos = []

print('Começo de leitura de arquivos...')

files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for index, file in enumerate(files):
    arquivo = open(f'Obras/{file}', 'r', encoding='unicode_escape')
    documentos.append({"id": index, "obra": arquivo.read()})
    arquivo.close()

print('Final de leitura de arquivos...')

stopwords = set(nltk.corpus.stopwords.words('portuguese'))

print('Processando sentenças...')

sentencas_processadas = []
for index, documento in enumerate(documentos):
    sentencas_processadas.append({"id": index, "sentencas": sent_tokenize(documento['obra'].replace('\n', ' '))})

print('Finalizado processamento de sentenças...')

print('Iniciando tokenização...')

tokens = []
for sentenca in sentencas_processadas:
    for s in sentenca["sentencas"]:
        words = word_tokenize(s)    
        for w in words:
            tokens.append(w)

tokens = [t for t in tokens if t.isalnum()]
tokens_lower = [t.lower() for t in tokens]
tokens_stepwords = [w for w in tokens_lower if w not in stopwords]

print('Finalizado tokenização...')
print('Removendo redundancias...')

vocab = rem_dup(tokens_stepwords)

print('Remoção de redundancias concluídas...')

print('Iniciando indexação...')

index = inverted_index(sentencas_processadas, vocab)
index = rem_dup_index(index, vocab)

with open('./indexed/index.json', 'w') as fp:
    json.dump(index, fp)
print('Finalizado indexação...')

print('Iniciando processo de Stemming...')
stemmer = RSLPStemmer()
tokens_stemming = [stemmer.stem(t) for t in vocab]
tokens_after_stemming = rem_dup(tokens_stemming)
print('Finalizado processo de Stemming...')
print('Indexando após Stemming...')

index_stemming = inverted_index(sentencas_processadas, tokens_after_stemming)
index_stemming = rem_dup_index(index_stemming, tokens_after_stemming)


with open('./indexed/index_stemmed.json', 'w') as fp:
    json.dump(index_stemming, fp)

print('Finzalizado processo após Stemming...')

#file_index = open('Index Invertido.txt', 'w', encoding='utf8')
# file_index_stemming = open('Index Inv. com Stemming.txt', 'w', encoding='utf8')

# for i in index:
#     file_index.write(f'index(size): {i}({len(index)}) -> {index[i]}\n')
    
# for i in index_stemming:
#     file_index_stemming.write(f'index(size): {i}({len(index_stemming)}) -> {index_stemming[i]}\n')

#file_index.close()
# file_index_stemming.close()





