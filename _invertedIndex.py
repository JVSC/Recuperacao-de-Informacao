import csv 
import nltk
nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import stopwords  
from nltk.tokenize import word_tokenize  

def count_word(sentence):
    counter = {}
    for word in set(sentence):
        counter[word] = 0
        for i in range(len(sentence) -1, -1, -1):
            if sentence[i] == word: 
                counter[word]=counter[word]+1
                del sentence[i]

    return sorted(counter.items(), key=lambda item:item[1])
    print("-")

def parse_corpus():
    tweet_arr = []
    stop_words = set(stopwords.words('english'))

    with open("./twitter_corpus/full-corpus.csv") as file:
        data = csv.reader(file)
        doc = {}
        next(data)
        for tweet in data:
            doc['topico'], doc['sentimento'], doc['tweet_id'], doc['tweet_horario'], doc['texto'] = tweet
            doc['tokenized'] = [w.lower() for w in word_tokenize(doc['texto']) if not w in stop_words]
            doc['indexed'] = count_word(doc['tokenized'])
            tweet_arr.append(doc)
    return tweet_arr
