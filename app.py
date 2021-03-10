from flask import Flask, render_template, jsonify, request, url_for
from boolean_search import pesquisa_booleana
import json

app = Flask(__name__)

corpus_info = open('./templates/corpus_info.json', 'r', encoding='utf8')
data = json.load(corpus_info)

@app.route('/')
def index():
    return render_template('index.html', info=data)

@app.route('/', methods=['POST'])
def pesquisa():
    query = request.form['pesquisa_booleana']
    results = pesquisa_booleana(query)
    return render_template('index.html', info=data, list=results)