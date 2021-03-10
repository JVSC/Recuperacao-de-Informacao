import pandas as pd
import seaborn as sns
from os import listdir
import math
import json
import matplotlib.pyplot as plt

mypath = "./Obras"

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

def build_matrizes():
    index_stemming = open('./indexed/index_stemmed.json', 'r', encoding='utf8')
    index_json = json.load(index_stemming)
    index_stemming.close()

    frequency_matrix = frequency_terms_matrix(index_json)
    wtd_matrix_var = wtd_matrix(frequency_matrix)
    idf_matrix_var = idf_matrix(frequency_matrix)
    tf_idf_matrix_var = tf_idf_matrix(frequency_matrix)

    with open('./scoring/frequency_matrix.json', 'w', encoding='utf8') as fp:
        json.dump(frequency_matrix, fp)
        
    with open('./scoring/wtd_matrix.json', 'w', encoding='utf8') as fp:
        json.dump(wtd_matrix_var, fp)
        
    with open('./scoring/idf_matrix.json', 'w', encoding='utf8') as fp:
        json.dump(idf_matrix_var, fp)
        
    with open('./scoring/tf_idf_matrix.json', 'w', encoding='utf8') as fp:
        json.dump(tf_idf_matrix_var, fp)

    terms_frequency = []
    for term in frequency_matrix:
        terms_frequency.append(term)

    terms_tf_idf = []
    for term in tf_idf_matrix_var:
        terms_tf_idf.append(term)

    df_frequency_matrix = pd.DataFrame (frequency_matrix, columns = terms_frequency)
    df_tf_idf_matrix = pd.DataFrame (tf_idf_matrix_var, columns = terms_tf_idf)
    df_frequency_matrix = df_frequency_matrix.T
    df_tf_idf_matrix = df_tf_idf_matrix.T

    sns.set()
    
    #parametros para definir min e max de escala de valores: vmin=0, vmax=0.5
    # ax1 = sns.heatmap(df_frequency_matrix)
    # ax2 = sns.heatmap(df_tf_idf_matrix)

    path = "./static/images/plot.png"
    if plt.savefig(path):
        return 1
    else:
        return 0