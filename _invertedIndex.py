import csv 
import nltk
nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import stopwords  
from nltk.tokenize import word_tokenize  

def inverted_index(corpus, terms):
    inverted_index = dict()
    for term in terms:
        inverted_index[term] = list()
        for index, tweet in enumerate(corpus):
            if term in tweet['tokenized']:
                inverted_index[term].append(index)

    return inverted_index

def parse_corpus():
    corpus = []
    stop_words = set(stopwords.words('english'))
    stop_words.update(set(stopwords.words('portuguese')))
    
    with open("./twitter_corpus/full-corpus.csv") as file:
        data = csv.reader(file)
        terms = set()
        next(data)
        for tweet in data:
            doc = {}
            doc['topico'], doc['sentimento'], doc['tweet_id'], doc['tweet_horario'], doc['texto'] = tweet
            doc['tokenized'] = set([w.lower() for w in word_tokenize(doc['texto']) if not w in stop_words])
            corpus.append(doc)
            terms.update(doc['tokenized'])

    return {
        'termos': terms,
        'corpus': corpus
    }
