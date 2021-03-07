import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import RSLPStemmer

import pandas as pd
import seaborn as sns

from os import listdir
from os.path import isfile, join
import json
import math

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


def inverted_index(sentencas_processadas, terms):
    inverted_index = dict()
    for term in terms:
        inverted_index[term] = {"obras":[], "sentencas": []}
        for index, sentenca in enumerate(sentencas_processadas):
            for i, s in enumerate(sentenca['sentencas']):                
                if term in s:
                    inverted_index[term]["obras"].append(sentenca['id'])
                    inverted_index[term]["sentencas"].append((sentenca['id'], i))
        if sum(inverted_index[term]['obras']) == 0.0:
            del inverted_index[term]
        else:
            inverted_index[term]['obras'] = list(dict.fromkeys(inverted_index[term]['obras']))
    return inverted_index

def frequency_terms_matrix(inverted_index):
    frequency_matrix = dict()
    for term in inverted_index:
        frequency_matrix_doc = [0] * len(listdir(mypath))
        for sentenca in inverted_index[term]['sentencas']:
            frequency_matrix_doc[sentenca[0]] += 1
        frequency_matrix[term] = frequency_matrix_doc
    return frequency_matrix
            
def wtd_matrix(frequency_matrix):
    wtd_matrix = dict()
    for term in frequency_matrix:
        wtd_matrix_docs = [0] * len(listdir(mypath))
        for index, freq in enumerate(frequency_matrix[term]):
            if freq != 0:
                wtd_matrix_docs[index] = 1 + math.log(freq, 10)
        wtd_matrix[term] = wtd_matrix_docs
    return wtd_matrix

def tf_query_document(query, doc, tf_terms_matrix):
    pass

def idf_matrix(frequency_matrix):
    idf_matrix = dict()
    for term in frequency_matrix:
        idf_matrix[term] = math.log(len(listdir(mypath))/len([i for i in frequency_matrix[term] if i > 0]), 10)
    return idf_matrix

def tf_idf_matrix(frequency_matrix):
    tf_idf_matrix = dict()
    for term in frequency_matrix:
        tf_idf_matrix_docs = [0] * len(listdir(mypath))
        for index in range(len(listdir(mypath))):
            if frequency_matrix[term][index] >= 1:
                tf_idf_matrix_docs[index] = (1 + math.log(frequency_matrix[term][index], 10)) * math.log(len(listdir(mypath))/len([i for i in frequency_matrix[term] if i > 0]), 10)
        tf_idf_matrix[term] = tf_idf_matrix_docs
    return tf_idf_matrix

#nltk.download('machado')
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('rslp')

documentos = []

files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for index, file in enumerate(files):
    arquivo = open(f'Obras/{file}', 'r', encoding='unicode_escape')
    documentos.append({"id": index, "obra": arquivo.read()})
    arquivo.close()

stopwords = set(nltk.corpus.stopwords.words('portuguese'))

sentencas_processadas = []
for index, documento in enumerate(documentos):
    sentencas_processadas.append({"id": index, "sentencas": sent_tokenize(documento['obra'].replace('\n', ' ').lower())})

tokens = []
for sentenca in sentencas_processadas:
    for s in sentenca["sentencas"]:
        words = word_tokenize(s)    
        for w in words:
            tokens.append(w)

tokens = [t for t in tokens if t.isalnum()]
tokens_lower = [t.lower() for t in tokens]
tokens_stepwords = [w for w in tokens_lower if w not in stopwords]

vocab = rem_dup(tokens_stepwords)
index = inverted_index(sentencas_processadas, vocab)

with open('./indexed/index.json', 'w', encoding='utf8') as fp:
    json.dump(index, fp)

stemmer = RSLPStemmer()
tokens_stemming = [stemmer.stem(t) for t in vocab]
tokens_after_stemming = rem_dup(tokens_stemming)

index_stemming = inverted_index(sentencas_processadas, tokens_after_stemming)

with open('./indexed/index_stemmed.json', 'w', encoding='utf8') as fp:
    json.dump(index_stemming, fp)

index_stemming = open('./indexed/index_stemmed.json', 'r', encoding='utf8')
index_json = json.load(index_stemming)
index_stemming.close()

frequency_matrix = frequency_terms_matrix(index_json)
wtd_matrix = wtd_matrix(frequency_matrix)
idf_matrix = idf_matrix(frequency_matrix)
tf_idf_matrix = tf_idf_matrix(frequency_matrix)

with open('./scoring/frequency_matrix.json', 'w', encoding='utf8') as fp:
    json.dump(frequency_matrix, fp)
    
with open('./scoring/wtd_matrix.json', 'w', encoding='utf8') as fp:
    json.dump(wtd_matrix, fp)
    
with open('./scoring/idf_matrix.json', 'w', encoding='utf8') as fp:
    json.dump(idf_matrix, fp)
    
with open('./scoring/tf_idf_matrix.json', 'w', encoding='utf8') as fp:
    json.dump(tf_idf_matrix, fp)

terms_frequency = []
for term in frequency_matrix:
    terms_frequency.append(term)

terms_tf_idf = []
for term in tf_idf_matrix:
    terms_tf_idf.append(term)

df_frequency_matrix = pd.DataFrame (frequency_matrix, columns = terms_frequency)
df_tf_idf_matrix = pd.DataFrame (tf_idf_matrix, columns = terms_tf_idf)

sns.set()
#parametros para definir min e max de escala de valores: vmin=0, vmax=0.5
#ax1 = sns.heatmap(df_frequency_matrix)
#ax2 = sns.heatmap(df_tf_idf_matrix) 

