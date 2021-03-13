from flask import Flask, render_template, jsonify, request, url_for, send_from_directory
from boolean_search import BooleanModel
from vector_space_search import pesquisa_vetorial
from matrizes import build_matrizes
import json

app = Flask(__name__)

corpus_info = open('./templates/corpus_info.json', 'r', encoding='utf8')
data = json.load(corpus_info)

@app.route('/')
def index():
    return render_template('index.html', info=data, result=0)

@app.route('/', methods=['POST'])
def pesquisa():
    if(request.form['pesquisa_booleana']):
        query = request.form['pesquisa_booleana']
        results = BooleanModel(query).run()
        tipo = 'booleana'
        print(results)
    elif(request.form['pesquisa_vetorial']):
        query = request.form['pesquisa_vetorial']
        results = pesquisa_vetorial(query)
        tipo = 'vetorial'
    return render_template('index.html', info=data, result=results, type=tipo )

@app.route('/graph', methods=['GET'])
def graph():
    result = build_matrizes()
    return render_template('graph.html', data=result)
    