# -*- coding: utf-8 -*-
"""
Title          : main.py
Author         : Jasmeet Narang, Dimple Mehra
Description    : visualizating and calculating network measures on the processed data
                 retrieved from DataProcessing.py file
"""
import json
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import networkx as nx
import numpy as np
from collections import Counter
from DataProcessing import api
import tweepy



# read the edges
def read_data(filename):
    with open(filename,'r') as f:
        stored_edges = json.load(f)
    #print('in function')
    #print(stored_edges)
    return stored_edges

# add edges to the graph
def create_graph(edges):
    graph = nx.Graph()
    graph.add_edges_from(edges, weight=3)


    return graph

# draw the graph and save as png
def draw_network(graph,filename):
    pos = nx.spring_layout(g, k=1, iterations=100)
    nx.draw_networkx(graph,pos,with_labels=True, node_size=20, node_color='red', alpha=0.6, edge_color='grey', width=2, font_size=13)
    plt.title('Friendship Network')
    figure = plt.gcf()
    figure.set_size_inches(20,15)
    plt.savefig(filename ,dpi=200,format='png')
    plt.axis('off')
    plt.show()

# calcuating degree distribution
def degree_distribution(graph):
    degree_sequence = list(dict(nx.degree(graph)).values())
    degree_count = Counter(degree_sequence)

    k=[]
    for degree, count in degree_count.items():
        k.append((degree, count/len(graph.nodes())))
    k = sorted(k)

    ks = [x[0] for x in k]
    deg = range(len(ks))

    plt.bar(deg, [x[1] for x in k], align='center', width= 0.80, alpha=0.4)

    plt.title("Degree Distribution (N=%d)"
              %(len(graph.nodes())))

    plt.ylabel("Fraction")
    plt.xlabel("Degree")
    plt.show()

# calculating clustering coefficent
def clusterning_coefficient(g):
    cluster_coef = list(nx.clustering(g).values())
    plt.hist(list(cluster_coef), alpha = 0.4, bins=20)
    plt.xlabel('clustering coefficient ')
    plt.ylabel('count')
    plt.title('clustering coefficient (N=%d)'
              %(len(g.nodes())))
    plt.show()

# calculating closeness centrality
def closeness(g):
    print("closeness centrality :", nx.closeness_centrality(g))
    pos = nx.spring_layout(g,k=1, iterations=100)
    nodes = nx.draw_networkx_nodes(g,pos, node_size=50,cmap=plt.cm.inferno,
                             node_color=list(nx.closeness_centrality(g).values()),
                             nodelist=nx.closeness_centrality(g).keys())
    norm = mcolors.SymLogNorm(linthresh=0.01, base=10)
    nodes.set_norm(norm=norm)
    nx.draw_networkx_edges(g, pos, edge_color='grey')

    plt.title('Closeness Centrality (N=%d)'
              %(len(g.nodes())))
    plt.axis('off')
    plt.colorbar(nodes)
    plt.show()


if __name__ == '__main__':
    new_edges = read_data('data/screen_names.txt')

    #create a graph and save as png file
    g = create_graph(new_edges)
    draw_network(g, 'Images/graph.png')

    # getting the network measures
    degree_distribution(g)

    clusterning_coefficient(g)

    closeness(g)





