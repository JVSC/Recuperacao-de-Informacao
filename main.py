
from _invertedIndex import parse_corpus
from _invertedIndex import inverted_index
from _invertedIndex import stemming_tokens
from _invertedIndex import inverted_index_stemming

docs = parse_corpus()
index = inverted_index(docs['corpus'], docs['termos'])
stemming,stemming_map = stemming_tokens(docs['termos'])
index_stemming = inverted_index_stemming(docs['corpus'], stemming)

file_index = open('index_invertido.txt', 'w', encoding='utf8')
file_index_stemming = open('index_invertido_stemming.txt', 'w',encoding='utf8')
file_stemming = open('stemming.txt', 'w',encoding='utf8')

for i in index:
    file_index.write(f'indice(tamanho): {i}({len(index[i])}) - {index[i]}\n')
    #     print(f'indice: {i} - {index[i]}')

for i in index_stemming:
    file_index_stemming.write(f'indice(tamanho): {i}({len(index_stemming[i])}) - {index_stemming[i]}\n')
    #     print(f'indice: {i} - {index_stemming[i]}')
    
file_stemming.write('Token Original - Token com Stemming')
for s in stemming_map:
    file_stemming.write(f'{s["original"]} - {s["stemming"]}\n')
    #     print(f'{s["original"]} - {s["stemming"]}')
    
file_index.close()
file_index_stemming.close()
file_stemming.close()
