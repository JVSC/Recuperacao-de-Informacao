from nltk.stem import RSLPStemmer
from nltk.tokenize import word_tokenize
from collections import deque
from helpers import shunting_yard_parser
import json
 

class BooleanModel:
    def __init__(self, max_distance=False):
        entrada = input("Busca: ")
        busca = word_tokenize(entrada.lower())
        self.query = deque(shunting_yard_parser(busca))
        self.max_distance = max_distance

        with open('./indexed/config.json') as f:
            d = json.load(f)
            self.doc_table = d['index_lookup']

    def run(self):
        docs = self._find() 
        results = []
        with open('./indexed/config.json') as f:
            d = json.load(f)
            doc_table = d['index_lookup']
        for doc in docs:
            results.append(doc_table[str(doc)])
        return results
    
    def _find(self):
        index = None
        findings = []
        stemmer = RSLPStemmer()
        with open("./indexed/index.json") as f:
            index = json.load(f)
            
        while(self.query):
            res = []
            token = self.query.popleft()
            if token == 'and':
                right_exp = findings.pop()
                left_exp = findings.pop()
                # busca AND
                res = self._and(left_exp, right_exp)

            elif token == 'or':
                right_exp = findings.pop()
                left_exp = findings.pop()
                # busca OR
                res = self._or(left_exp, right_exp)

            elif token == 'not':
                exp = findings.pop()
                docs = []
                with open("./indexed/config.json") as data:
                    d = json.load(data)
                    docs = d['doc_index']
                res = self._not(exp, docs) 
            else:
                #token = stemmer.stem(token)
                if token in index:
                    res = index[token]['obras']
            findings.append(res)

        # caso esteja vazio, retornar a lista vazia, já que geram problemas ao tentar dar pop em list vazia
        if not findings:
            return findings
        else:
            return findings.pop()

    def _and(self, p1, p2):
        docs = []
        p1_index = 0
        p2_index = 0

        while(p1_index < len(p1) and p2_index < len(p2)):
            doc_p1 = p1[p1_index]
            doc_p2 = p2[p2_index]
            
            if doc_p1 == doc_p2:
                docs.append(doc_p1)
                p1_index = p1_index + 1
                p2_index = p2_index + 1
            elif doc_p1 > doc_p2:
                p2_index = p2_index + 1
            elif doc_p2 > doc_p1:
                p1_index = p1_index + 1

        return docs

    def _or(self, p1, p2):
        docs = []
        p1_index = 0
        p2_index = 0
        while(p1_index < len(p1) or p2_index < len(p2)):
            
            if(p1_index < len(p1) and p2_index < len(p2)):
                doc_p1 = p1[p1_index]
                doc_p2 = p2[p2_index]

                if doc_p1 == doc_p2:
                    docs.append(doc_p1)
                    p1_index = p1_index + 1
                    p2_index = p2_index + 1

                elif doc_p1 > doc_p2:
                    docs.append(doc_p2)
                    p2_index = p2_index + 1

                elif doc_p2 > doc_p1:
                    docs.append(doc_p1)
                    p1_index = p1_index + 1
            
            elif(p1_index >= len(p1)):
                docs.append(p2[p2_index])
                p2_index = p2_index + 1
            
            elif(p2_index >= len(p2)):
                docs.append(p1[p1_index])
                p1_index = p1_index + 1

        return docs

    def _not(self, p1, p2):
        if(not p1):
            return p2
        docs = []
        p1_index = 0

        for item in p2:
            if(item != p1[p1_index]):
                docs.append(item)
            elif(p1_index + 1 < len(p1)):
                p1_index = p1_index + 1
        return docs

print(BooleanModel().run())