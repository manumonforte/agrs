import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def get_artists_in_file(filename):
    """
    Create artists list from the file given
    :param filename:
    :return: list of artists
    """
    return [line.strip() for line in open(filename, 'r')]


def get_artists(sp, artists, data):
    """
    Add content to data json with the id and name of the artist
    :param data:
    :param artists:
    :param sp which contains the connection to spotify API
    :return: json data with artists
    """
    for artist in artists:
        results = sp.search(q='artist:' + artist, type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            id = items[0]['id']
            urn = 'spotify:artist:{}'.format(id)
            elem = sp.artist(urn)
            data[id] = {}
            data[id]['name'] = elem['name']
            data[id]['popularity'] = elem['popularity']
            data[id]['genres'] = elem['genres']
            data[id]['followers'] = elem['followers']['total']
        else:
            return None


def get_recommendations_by_artist(sp, data):
    """
    Add content to the data json with the artists' tracks
    :param sp which contains the connection to spotify API
    :param data:
    :return: dictionary of recommended songs given an artist id
    """
    for id in data.keys():
        recommendation_list = {}
        urn = 'spotify:artist:{}'.format(id)
        results = sp.artist_top_tracks(urn)
        # results = sp.recommendations(seed_artists=[id], limit=25)
        mean_pop = np.array([])
        for track in results['tracks']:
            mean_pop = np.append(mean_pop, [track['popularity']])
            recommendation_list[track['id']] = {'name': track['name'], 'popularity': track['popularity']}
        data[id]['tracks'] = recommendation_list
        data[id]['avg_popularity_songs'] = np.mean(mean_pop)


def get_track_artists(sp, data):
    """
    Add content to the data json with the partners of the main artist and the styles of each song
    :param sp which contains the connection to spotify API
    :param data:
    :return:
    """
    for id in data.keys():
        data[id]['partners'] = {}
        for id_song in data[id]['tracks'].keys():
            urn = 'spotify:track:{}'.format(id_song)
            track = sp.track(urn)
            for elem in track['artists']:
                if elem['id'] != id:
                    if elem['id'] not in data[id]['partners'].keys():
                        data[id]['partners'][elem['id']] = {}
                        data[id]['partners'][elem['id']]['name'] = elem['name']
                        data[id]['partners'][elem['id']]['times'] = 1
                        popularity_results = sp.search(q='artist:' + elem['name'], type='artist')
                        items = popularity_results['artists']['items']
                        if len(items) > 0:
                            data[id]['partners'][elem['id']]['popularity'] = items[0]['popularity']
                    else:
                        data[id]['partners'][elem['id']]['times'] += 1


def get_nodes_and_weights(grafo, data):
    for key in data:
        grafo.add_node(data[key]['name'], weight=data[key]['popularity'])

    return grafo


def get_edges(grafo, data):
    for key in data:
        artist = data[key]['name']
        for partner in data[key]['partners']:
            # print(artist, data[key]['partners'][partner]['name'], data[key]['partners'][partner]['times'])
            grafo.add_edge(artist, data[key]['partners'][partner]['name'], weight=data[key]['partners'][partner]['times'])

    return grafo


def get_labels_and_colors(g):
    labels = {}
    colors = []
    for n in g.nodes:
        if len(g.nodes[n]) == 0:
            labels[n] = str(n)
            # labels.append((str(n), str(0)))
            colors.append(0)
        else:
            labels[n] = str(n) + " " + str(g.nodes[n]['weight'])
            # labels.append((str(n), str(g.nodes[n]['weight'])))
            colors.append(g.nodes[n]['weight'])

    return labels, colors


def draw_graph(g, labels={}, colors=[]):
    pos = nx.spring_layout(g)
    nx.draw(g, pos, with_labels=True, labels=labels, node_color=colors)
    plt.axis('off')
    plt.show()
