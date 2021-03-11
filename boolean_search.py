from nltk.stem import RSLPStemmer
from nltk.tokenize import word_tokenize
from collections import deque
import json

def shunting_yard_parser(tokens):
    output = []
    stack = []
    left_parenthesis = '('
    right_parenthesis = ')'
    precedence = {}
    with open('./indexed/config.json') as f: 
        d = json.load(f)
        precedence = d['precedence_table']

    for token in tokens:
        if token not in precedence:
            output.append(token)

        elif token is left_parenthesis:
            stack.append(token) 

        elif token is right_parenthesis:
            operator = stack.pop()
            while operator != '(':
                ouput.append(operator)
                operator = stack.pop()

        elif token in precedence:
            if(stack):
                old_operator = stack[-1]
                while(precedence[old_operator] > precedence[token]):
                    output.append(stack.pop())
                    if(stack):
                        old_operator = stack[-1]
            stack.append(token)

    while(stack):
        output.append(stack.pop())

    return output

def and_operation(p1, p2):
    docs = []
    p1_index = 0
    p2_index = 0

    while(p1_index < len(p1) and p2_index < len(p2)):
        token_p1 = p1[p1_index]
        token_p2 = p2[p2_index]
        
        if token_p1 == token_p2:
            docs.append(token_p1)
            p1_index = p1_index + 1
            p2_index = p2_index + 1
        elif token_p1 > token_p2:
            p2_index = p2_index + 1
        elif token_p2 > token_p1:
            p1_index = p1_index + 1

    return docs

def or_operation(p1, p2):
    docs = []
    p1_index = 0
    p2_index = 0
    while(p1_index < len(p1) or p2_index < len(p2)):
        
        if(p1_index < len(p1) and p2_index < len(p2)):
            token_p1 = p1[p1_index]
            token_p2 = p2[p2_index]

            if token_p1 == token_p2:
                docs.append(token_p1)
                p1_index = p1_index + 1
                p2_index = p2_index + 1

            elif token_p1 > token_p2:
                docs.append(token_p2)
                p2_index = p2_index + 1

            elif token_p2 > token_p1:
                docs.append(token_p1)
                p1_index = p1_index + 1
        
        elif(p1_index >= len(p1)):
            docs.append(p2[p2_index])
            p2_index = p2_index + 1
        
        elif(p2_index >= len(p2)):
            docs.append(p1[p1_index])
            p1_index = p1_index + 1

    return docs

def not_operation(p1, p2):
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

def find(query):
    index = None
    findings = []
    stemmer = RSLPStemmer()
    with open("./indexed/index.json") as f:
        index = json.load(f)
        
    while(query):
        res = []
        token = query.popleft()
        if token == 'and':
            right_exp = findings.pop()
            left_exp = findings.pop()
            # busca AND
            res = and_operation(left_exp, right_exp)

        elif token == 'or':
            right_exp = findings.pop()
            left_exp = findings.pop()
            # busca OR
            res = or_operation(left_exp, right_exp)

        elif token == 'not':
            exp = findings.pop()
            docs = []
            with open("./indexed/config.json") as data:
                d = json.load(data)
                docs = d['doc_index']
            res = not_operation(exp, docs)
        
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

def pesquisa_booleana(entrada):
    busca = word_tokenize(entrada.lower())

    query = shunting_yard_parser(busca)

    docs = find(deque(query))

    # print("- Resultados")
    doc_table = {}
    results = []
    with open('./indexed/config.json') as f:
        d = json.load(f)
        doc_table = d['index_lookup']
    for doc in docs:
        # print(f'--> {doc_table[str(doc)]}')
        results.append(doc_table[str(doc)])
    return results
