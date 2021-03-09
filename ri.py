import json
from indexer import Indexer
from matrizes import build_matrizes

#nltk.download('machado')
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('rslp')
Indexer('./Obras').inverted_index(False)
build_matrizes()

