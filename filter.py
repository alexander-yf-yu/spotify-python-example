import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import datetime

load_dotenv()

max_valence = 1
min_valence = 0.5

scopes = ["user-top-read", "playlist-modify-public", "playlist-modify-private"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scopes))

top_tracks = sp.current_user_top_tracks(time_range='long_term')

songs = []
song_names = []

for idx, item in enumerate(top_tracks['items']):

    uri = item['uri']
    valence = sp.audio_features(uri)[0]['valence']
    
    # print(idx, valence, item['uri'], item['name'], [a['name'] for a in item['artists']])

    if min_valence <= valence and valence <= max_valence:
        songs.append(uri)
        song_names.append(item['name'])


new_playlist = sp.user_playlist_create(
    '21rfdwzw2c5n4jijqgutjmkrq',
    str(datetime.datetime.now()),
    public=False,
    description=f"valence lower bound (min happiness) = {min_valence}, valence upper bound (max happiness) = {max_valence}"
)

print('Creating playlist with songs' + song_names)

sp.playlist_add_items(new_playlist['id'], songs)