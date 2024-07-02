import os
import spotipy
import requests
from pprint import pprint

from pprint import pprint
from dotenv import load_dotenv
from transformers import pipeline


from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
pipe = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base" , device = "mps" , top_k = 7)

sp =  spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

def get_song_lyrics(id) : 

    url_spotify_api_lrcs = "https://spotify23.p.rapidapi.com/track_lyrics/"
    headers = {
        "x-rapidapi-key": "c3a0ff933cmsh9c6ca83440520f7p1f106ajsn86d70f424094",
        "x-rapidapi-host": "spotify23.p.rapidapi.com"
    }

    song_lyrics = requests.get(url_spotify_api_lrcs, headers=headers, params={"id" : id})
    song_lrcs_json = song_lyrics.json()

    lrcs = " ".join([i["words"] for i in song_lrcs_json["lyrics"]["lines"]])
    return lrcs

def song_info_loader(id) : 
    global pipe

    tid = f'spotify:track:{id}'
    features = ["danceability" , "energy" , "loudness" , "acousticness" , "instrumentalness" , "liveness" , "tempo"]
    analysis = sp.audio_features(tid)[0]
    track = sp.track(tid)

    artists = [i["name"] for i in track["artists"]]
    name = track["name"]
    lrcs = get_song_lyrics(id)
    output = pipe(lrcs[:514])[0]
    sentiments = [i["label"] for i in output if i["score"]>0.1]

    song_info = {"name" : name,
             "artists" : artists,
             "lyrics" : lrcs,
             "sentiments" : sentiments}
    
    final_analysis = {i:analysis[i] for i in features  }
    song_info.update(final_analysis)
    return song_info

pprint(song_info_loader("4n7jnSxVLd8QioibtTDBDq"))
# pprint(song_info_loader("0TK2YIli7K1leLovkQiNik"))

# id = "4n7jnSxVLd8QioibtTDBDq"
# print(get_song_lyrics(id))