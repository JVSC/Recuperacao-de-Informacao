from flask import Flask, render_template, jsonify, request, url_for, send_from_directory
from boolean_search import pesquisa_booleana
from matrizes import build_matrizes
import json

app = Flask(__name__)

corpus_info = open('./templates/corpus_info.json', 'r', encoding='utf8')
data = json.load(corpus_info)

@app.route('/')
def index():
    return render_template('index.html', info=data, list=0)

@app.route('/', methods=['POST'])
def pesquisa():
    query = request.form['pesquisa_booleana']
    results = pesquisa_booleana(query)
    return render_template('index.html', info=data, list=results)

@app.route('/graph', methods=['GET'])
def graph():
    result = build_matrizes()

    return render_template('graph.html', data=result)
    