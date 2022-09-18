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
    errors = []
    if(validate(request.form, errors)):
        graph = criar_grafo(request.form)
        nodes = graph.nodes
        partida = request.form['partidaVertice']
        destino = request.form['destinoVertice']
        path = graph.a_star_path(partida, destino)
        if (path is None):
            errors.append('Nenhum caminho encontrado para o ponto de partida e destino informados')
            return render_template('hello.html', errors=errors)
        colours = criar_cores(nodes, partida, destino)
        desenhar_grafo_com_caminho(graph, colours, path)
        filename = salvar_arquivo()
        return send_file(filename, mimetype='image/gif')
    return render_template('hello.html', errors=errors)

def validate(form, errors):
    valid = True
    nodes = set()
    nodes.update(form.getlist('nomeVertice[]'))
    if(len(nodes) < 2):
        valid = False
        errors.append('A quantidade de vertices não pode ser menor que 2')
    if(form['partidaVertice'] not in nodes):
        valid = False
        errors.append('O vertice de partida precisa estar na declaração dos vertices')
    if(form['destinoVertice'] not in nodes):
        valid = False
        errors.append('O vertice de destino precisa estar na declaração dos vertices')
    return valid

def criar_grafo(form):
    nodes = set()
    nodes.update(form.getlist('nomeVertice[]'))
    graph = Graph()
    graph.add_nodes_from(nodes)
    for a, b, c in zip(form.getlist('uVertice[]'), form.getlist('vVertice[]'), form.getlist('pesos[]')):
        graph.add_edge(a, b, weight=float(c))
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
    nx.draw_networkx_edges(graph, pos=pos, edgelist=graph.edges, edge_color=(0.8,0.8,0.85))
    nx.draw_networkx_edges(graph, pos=pos, edgelist=route_edges, edge_color = 'r')

    edge_labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels)