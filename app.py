from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    corpus_info = open('./templates/corpus_info.json', 'r', encoding='utf8')
    data = json.load(corpus_info)

    return render_template('index.html', info=data)