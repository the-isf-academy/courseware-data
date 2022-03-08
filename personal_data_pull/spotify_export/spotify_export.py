import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import time
import json

SPOTIPY_CLIENT_ID='719286f4971e4d3985933ab31f96e659'
SPOTIPY_CLIENT_SECRET='6586305e7b304efcbc3556cfbce9b023'
SPOTIPY_REDIRECT_URI='http://127.0.0.1:9090'
SCOPE = "user-top-read"

DATA = "data/MyData/StreamingHistory4.json"

def streaming_history_to_csv():
    with open(DATA) as json_file:
        streaming_history = json.load(json_file)
    events = []
    for event in streaming_history:
        artist = event['artistName']
        track = event['trackName']
        date = event['endTime']
        day = date.split()[0]
        time_played = date.split()[1]
        duration = event['msPlayed']
        event_info = get_track_info(artist, track)
        if event_info != None:
            event_info.extend([day,time_played,duration])
            events.append(event_info)

    # create dataset
    df = pd.DataFrame(events, columns = ['title','artist', 'album','popularity','explicit','genres', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'release_date','length_of_song','date_streamed', 'time_streamed','length_time_listened'])
    # save to CSV
    timestamp = time.strftime("%d%b_%H%M")
    df.to_csv('spotify_data_export_{}.csv'.format(timestamp))

def get_track_info(artist_name,track_name):
    query = "track:{} artist:{}".format(track_name,artist_name)
    track_data = sp.search(q=query, type="track,episode", limit=1)
    if len(track_data['tracks']['items'])== 0: #didn't work - probably podcast
        return

    track = track_data['tracks']['items'][0]

    #the song data
    title = track['name']
    artist = track['artists'][0]['name']
    album = track['album']['name']
    release = track['album']['release_date']
    length = track['duration_ms']
    popularity = track['popularity']
    explicit = track['explicit']

    #get genre from artist data
    artist_id = track['artists'][0]['id']
    artist_data = sp.artist(artist_id)
    genres = artist_data['genres']

    #get audio get_track_features
    track_id = track['id']
    features = sp.audio_features([track_id])
    if features[0] == None:
        return
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    acousticness = features[0]['acousticness']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    valence = features[0]['valence']
    tempo = features[0]['tempo']

    track_info = [title,artist,album,popularity, explicit, genres, danceability, energy, loudness, speechiness, acousticness, instrumentalness, liveness, valence, tempo, release,length]
    return track_info

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
client_secret=SPOTIPY_CLIENT_SECRET,
redirect_uri=SPOTIPY_REDIRECT_URI,
scope=SCOPE))

streaming_history_to_csv()
