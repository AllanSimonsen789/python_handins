#!flask/bin/python
from flask import Flask
import networkx as nx
import random



app = Flask(__name__)

@app.route('/flask_app/')
def index():
    return "Hello, World from flask server!"


@app.route('/wiki/randomNodes', methods=['GET'])
def get_randomnodes():
    graph = nx.read_edgelist("/home/jovyan/my_notebooks/handins/week9modules/Wiki-Vote.txt")
    idchosen = random.randint(1, len(graph))
    neighbors = graph[str(idchosen)]
    return "id choosen: " + str(idchosen) + " has neighbors: " + str(neighbors)

if __name__ == '__main__':
    app.run(debug=True)