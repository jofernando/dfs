from datetime import datetime
from dfs import Graph
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
    nodes.update(request.form.getlist('nomeVertice[]'))
    graph = Graph()
    graph.add_nodes_from(nodes)
    for a, b in zip(request.form.getlist('uVertice[]'), request.form.getlist('vVertice[]')):
        graph.add_edge(a, b)
    path = graph.dfs_path(request.form['partidaVertice'], request.form['destinoVertice'])
    route_edges = [(path[n], path[n + 1]) for n in range(len(path) - 1)]
    pos = nx.spring_layout(graph)
    nodes = graph.nodes
    colours = [(0.18, 0.03, 0.37)] * len(nodes)
    colours = dict(zip(nodes, colours))
    colours[request.form['partidaVertice']] = (0, 0.49, 0.51)
    colours[request.form['destinoVertice']] = (0.92, 0.36, 0.36)
    nx.draw_networkx_nodes(graph, pos=pos, nodelist=nodes, node_size=400)
    nx.draw_networkx_labels(graph, pos=pos, font_color='w')
    nx.draw_networkx_edges(graph, pos=pos, edgelist=graph.edges)
    nx.draw_networkx_edges(graph, pos=pos, edgelist=route_edges, edge_color = 'r')
    filename = datetime.now().strftime("graphs/%Y%m%d%H%M%S") + '.png'
    plt.savefig(filename)
    plt.clf()
    return send_file(filename, mimetype='image/gif')
