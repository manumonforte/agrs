from agrs.etl.preprocess_data import *
from agrs.etl.utils import get_nodes_and_weights, get_edges, get_labels_and_colors, draw_graph

if __name__ == '__main__':
    with open('../data/processed_data.json') as json_file:
        data = json.load(json_file)
    # print(data)

    data_d3js = {'nodes': [], 'links': []}

    g = nx.Graph()
    g = get_nodes_and_weights(g, data, data_d3js)
    g = get_edges(g, data, data_d3js)

    labels, colors = get_labels_and_colors(g)

    draw_graph(g, labels, colors)

    centrality = nx.degree_centrality(g)
    closeness = nx.closeness_centrality(g)
    betweenness = nx.betweenness_centrality(g)
    eigenvector = nx.eigenvector_centrality(g)
    pagerank = nx.pagerank(g)

    for node in data_d3js['nodes']:
            current_name = node['name']
            node['id'] = current_name
            node['name'] = None
            node['centrality'] = round(centrality[current_name] * 100, 2)
            node['closeness'] = round(closeness[current_name] * 100, 2)
            node['betweenness'] = round(betweenness[current_name] * 100, 2)
            node['eigenvector'] = round(eigenvector[current_name] * 100, 2)
            node['pagerank'] = round(pagerank[current_name] * 100, 2)
            node.pop('partners', None)
            node.pop('tracks', None)
            node.pop('genres', None)

    with open('../data/data_d3js.json', 'w+', encoding='UTF-8') as outfile:
        json.dump(data_d3js, outfile, ensure_ascii=False)
