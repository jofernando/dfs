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
    route_edges = [(path[n], path[n+1]) for n in range(len(path)-1)]
    pos = nx.spring_layout(graph)
    nodes = [0,1,2,3,4]
    nx.draw_networkx_nodes(graph, pos=pos, nodelist=nodes, node_color=[(0.8,0.4,0.9),'y','y','y','g'])
    nx.draw_networkx_labels(graph, pos=pos)
    nx.draw_networkx_edges(graph, pos=pos, edgelist=graph.edges)
    nx.draw_networkx_edges(graph, pos=pos, edgelist=route_edges, edge_color = 'r')
    filename = datetime.now().strftime("graphs/%Y%m%d%H%M%S") + '.png'
    plt.legend(['partida', '', 'caminho', 'destino'])
    plt.savefig(filename)
    plt.clf()
    return send_file(filename, mimetype='image/gif')
