import json
from preprocess_data import *
# Importamos matplotlib para la visualizacion


if __name__ == '__main__':
    with open('processed_data.json') as json_file:
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


