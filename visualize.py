import json
from networkx.readwrite import json_graph
import networkx as nx
import matplotlib.pyplot as plt

filename = '2.5.2'
G = nx.Graph()
with open(filename) as json_file:
    data = json.load(json_file)
    for i in range(len(data)):
        G.add_node(i)
        for j in range(len(data[str(i)])):
            G.add_edge(i, int(data[str(i)][j]))
dic = {}
print G.size()
for i in range(len(G.nodes())):
    dic[i] = i
for i in range(1):
    plt.figure()
    plt.title('spring')
    nx.draw_spring(G, node_size=0,width=.2, labels=dic, font_size=8, font_color='red')


plt.show()
