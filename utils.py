
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
            data[id] = {}
            data[id]['name'] = artist
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
        results = sp.recommendations(seed_artists=[id])
        for track in results['tracks']:
            recommendation_list[track['id']] = track['name']
        data[id]['tracks'] = recommendation_list


def get_track_artists(sp, data):
    """
    Add content to the data json with the partners of the main artist
    :param sp which contains the connection to spotify API
    :param data:
    :return:
    """
    for id in data.keys():
        for id_song in data[id]['tracks'].keys():
            urn = 'spotify:track:{}'.format(id_song)
            track = sp.track(urn)
            data[id]['partners'] = {}
            for elem in track['artists']:
                if elem['name'] not in data[id]['partners'].keys():
                    data[id]['partners'][elem['id']] = {}
                    data[id]['partners'][elem['id']]['name'] = elem['name']
                    data[id]['partners'][elem['id']]['times'] = 1
                else:
                    data[id]['partners'][elem['id']]['times'] += 1
