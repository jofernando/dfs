from flask import Flask
from flask import render_template
from flask import request
from dfs import Graph

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('hello.html')

@app.route('/enviar', methods=['POST'])
def salvar():
    nodes = set()
    nodes.update(request.form.getlist('emailCoautor[]'))
    nodes.update(request.form.getlist('nomeCoautor[]'))
    graph = Graph(len(nodes), directed=False)
    for a, b in zip(request.form.getlist('emailCoautor[]'), request.form.getlist('nomeCoautor[]')):
        graph.add_edge(int(a), int(b))
    return ''.join(str(x) for x in graph.dfs(0, 4))