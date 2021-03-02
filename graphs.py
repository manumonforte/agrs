import json
import networkx as nx
from agrs.preprocess_data import *
from agrs.utils import get_nodes_and_weights, get_edges, get_labels_and_colors, draw_graph

if __name__ == '__main__':
    with open('data/processed_data.json') as json_file:
        data = json.load(json_file)
    # print(data)

    g = nx.Graph()
    g = get_nodes_and_weights(g, data)
    g = get_edges(g, data)

    labels, colors = get_labels_and_colors(g)

    draw_graph(g, labels, colors)

    print("centrality")
    centrality = nx.degree_centrality(g)
    print(centrality)

    print("closeness")
    closeness = nx.closeness_centrality(g)
    print(closeness)

    print("betweenness")
    betweenness = nx.betweenness_centrality(g)
    print(betweenness)

    print("eigenvector")
    eigenvector = nx.eigenvector_centrality(g)
    print(eigenvector)

    print("pagerank")
    pagerank = nx.pagerank(g)
    print(pagerank)

    for id in data.keys():
        data[id]['centrality'] = centrality[data[id]['name']]
        data[id]['closeness'] = closeness[data[id]['name']]
        data[id]['betweenness'] = betweenness[data[id]['name']]
        data[id]['eigenvector'] = eigenvector[data[id]['name']]
        data[id]['pagerank'] = pagerank[data[id]['name']]

    with open('data/data_d3js.json', 'w+', encoding='UTF-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)
