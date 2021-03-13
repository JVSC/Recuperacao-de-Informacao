import json
from indexer import Indexer
from matrizes import build_matrizes

#nltk.download('machado')
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('rslp')
index = Indexer('./Obras').inverted_index(False)
with open("./indexed/index.json", 'w', encoding='utf8') as f:
    json.dump(index, f)
build_matrizes()

