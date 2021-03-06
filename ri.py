#ATENÇÃO
#Realizamos a incluusão da obra através do método de
#download da biblioteca NLTK

import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import RSLPStemmer

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
        inverted_index[term] = list()
        for index, sentenca in enumerate(sentencas_processadas):
            if term in sentenca:
                inverted_index[term].append(index)
    return inverted_index

nltk.download('machado')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('rslp')

#documento = nltk.corpus.machado.raw('romance/marm08.txt')
arquivo = open('Dom Casmurro - MA.txt', 'r')
documento = arquivo.read()
stopwords = set(nltk.corpus.stopwords.words('portuguese'))

sentencas_processadas = sent_tokenize(documento.replace('\n', ' '))

tokens = []
for s in sentencas_processadas:
    words = word_tokenize(s)    
    for w in words:
        tokens.append(w)

tokens = [t for t in tokens if t.isalnum()]
tokens_lower = [t.lower() for t in tokens]
tokens_stepwords = [w for w in tokens_lower if w not in stopwords]

vocab = rem_dup(tokens_stepwords)

index = inverted_index(sentencas_processadas, vocab)

stemmer = RSLPStemmer()
tokens_stemming = [stemmer.stem(t) for t in vocab]
tokens_after_stemming = rem_dup(tokens_stemming)

index_stemming = inverted_index(sentencas_processadas, tokens_after_stemming)

file_index = open('Index Invertido.txt', 'w', encoding='utf8')
file_index_stemming = open('Index Inv. com Stemming.txt', 'w', encoding='utf8')

for i in index:
    file_index.write(f'index(size): {i}({len(index)}) -> {index[i]}\n')
    
for i in index_stemming:
    file_index_stemming.write(f'index(size): {i}({len(index_stemming)}) -> {index_stemming[i]}\n')


arquivo.close()
file_index.close()
file_index_stemming.close()





