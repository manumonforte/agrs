import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from utils import *
import random

if __name__ == '__main__':
    random.seed(10)
    # Load credentials
    with open('credentials.json') as json_file:
        config = json.load(json_file)

    CLIENT_ID = config['CLIENT_ID']
    CLIENT_SECRET = config['CLIENT_SECRET']

    # get connection
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    data = {}

    artists = get_artists_in_file('artists')

    get_artists(sp, artists, data)

    get_recommendations_by_artist(sp, data)
    # Guardar popularidad de las canciones
    

    get_track_artists(sp, data)

    with open('data_raw.json', 'w', encoding='UTF-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)
