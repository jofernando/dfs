from datetime import datetime
from dfs import Graph
from flask import Flask, render_template, request, send_file
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx


app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('hello.html')

@app.route('/enviar', methods=['POST'])
def salvar():
    graph = criar_grafo(request.form)
    nodes = graph.nodes
    partida = request.form['partidaVertice']
    destino = request.form['destinoVertice']
    path = graph.dfs_path(partida, destino, path=[], visited=set())
    colours = criar_cores(nodes, partida, destino)
    desenhar_grafo_com_caminho(graph, colours, path)
    filename = salvar_arquivo()
    return send_file(filename, mimetype='image/gif')

def criar_grafo(form):
    nodes = set()
    nodes.update(form.getlist('nomeVertice[]'))
    graph = Graph()
    graph.add_nodes_from(nodes)
    for a, b in zip(form.getlist('uVertice[]'), form.getlist('vVertice[]')):
        graph.add_edge(a, b)
    return graph

def criar_cores(nodes, partida, destino):
    colours = [(0.18, 0.03, 0.37)] * len(nodes)
    colours = dict(zip(nodes, colours))
    colours[partida] = (0, 0.49, 0.51)
    colours[destino] = (0.92, 0.36, 0.36)
    return [*colours.values()]

def salvar_arquivo():
    filename = datetime.now().strftime("graphs/%Y%m%d%H%M%S") + '.png'
    plt.savefig(filename)
    plt.clf()
    return filename

def desenhar_grafo_com_caminho(graph, colours, path):
    route_edges = [(path[n], path[n + 1]) for n in range(len(path) - 1)]
    pos = nx.spring_layout(graph)
    nodes = graph.nodes
    nx.draw_networkx_nodes(graph, pos=pos, nodelist=nodes, node_color=colours, node_size=400)
    nx.draw_networkx_labels(graph, pos=pos, font_color='w')
    nx.draw_networkx_edges(graph, pos=pos, edgelist=graph.edges)
    nx.draw_networkx_edges(graph, pos=pos, edgelist=route_edges, edge_color = 'r')