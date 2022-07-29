from datetime import datetime
from flask import Flask, render_template, request, send_file
import matplotlib.pyplot as plt
import networkx as nx

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('hello.html')

@app.route('/enviar', methods=['POST'])
def salvar():
    nodes = set()
    nodes.update(request.form.getlist('emailCoautor[]'))
    nodes.update(request.form.getlist('nomeCoautor[]'))
    graph = nx.Graph()
    for a, b in zip(request.form.getlist('emailCoautor[]'), request.form.getlist('nomeCoautor[]')):
        graph.add_edge(int(a), int(b))
    nx.draw(graph, with_labels=True, font_weight='bold')
    filename = datetime.now().strftime("graphs/%Y%m%d%H%M%S") + '.png'
    plt.savefig(filename)
    return send_file(filename, mimetype='image/gif')
