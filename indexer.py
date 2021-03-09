import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import RSLPStemmer

import json

from os import listdir
from os.path import isfile, join

from helpers import remove_duplicatas

class Indexer:
    # carrega os documentos para memória
    def __init__(self,link_documentos):
        # documentos completos
        self.documentos = []
        # documentos tokenizado em frases
        self.sentencas_processadas = []
        # tokens
        self.tokens = []
        self.tokens_stemmed = []
        # vocabulario unico
        self.vocabulario = []

        self.carregar_documentos(link_documentos)
        self.processar_sentencas()

    def carregar_documentos(self, link_documentos):
        files = [f for f in listdir(link_documentos) if isfile(join(link_documentos, f))]
        indexed_ID = []
        index_lookup = {}
        filename_lookup = {}

        print(f'- Carregando documentos')
        for index, file in enumerate(files):
            with open(f'Obras/{file}', 'r', encoding='unicode_escape') as arquivo:
                self.documentos.append({"id": index, "obra": arquivo.read()})
                indexed_ID.append(index)
                index_lookup[index] = file
                filename_lookup[file] = index
        
        with open('./indexed/config.json', 'w') as f:
            json.dump({'doc_index': indexed_ID, 'index_lookup': index_lookup, 'filename_lookup': filename_lookup}, f)
        
    def processar_sentencas(self):
        print("Processando sentenças")
        for index, documento in enumerate(self.documentos):
            self.sentencas_processadas.append({"id": index, "textos": sent_tokenize(documento['obra'].replace('\n', ' ').lower())})

    def tokenizar(self, stem):
        print("Tokenizando...")
        stopwords = nltk.corpus.stopwords.words('portuguese')

        for sentenca in self.sentencas_processadas:
            stemmer = None
            if(stem): 
                stemmer = RSLPStemmer()

            for texto in sentenca["textos"]:
                palavras = word_tokenize(texto)    
                for palavra in palavras:
                    if palavra in stopwords or not palavra.isalnum():
                        continue
                    palavra = palavra.lower()
                    if(stem):
                        palavra = stemmer.stem(palavra)
                    self.tokens.append(palavra)

        self.vocabulario = remove_duplicatas(self.tokens)

    def inverted_index(self, stem):
        self.tokenizar(stem)
        inverted_index = dict()

        for term in self.tokens:

            inverted_index[term] = {"obras":[], "sentencas": []}
            for index, sentenca in enumerate(self.sentencas_processadas):
                for i, texto in enumerate(sentenca['textos']):                
                    if term in texto:
                        inverted_index[term]["obras"].append(sentenca['id'])
                        inverted_index[term]["sentencas"].append((sentenca['id'], i))

            if sum(inverted_index[term]['obras']) == 0.0:
                del inverted_index[term]
            else:
                inverted_index[term]['obras'] = list(dict.fromkeys(inverted_index[term]['obras']))

        return inverted_index
