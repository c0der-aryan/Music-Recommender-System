import sys
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint
SPOTIPY_CLIENT_ID = "to-be-defined"
SPOTIPY_CLIENT_SECRET = "to-be-defined"

sp =  spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID , SPOTIPY_CLIENT_SECRET))
if len(sys.argv) > 1:
    tid = sys.argv[1]
else:
    tid = 'spotify:track:4n7jnSxVLd8QioibtTDBDq'


features = ["danceability" , "energy" , "loudness" , "acousticness" , "instrumentalness" , "liveness" , "tempo"]
analysis = sp.audio_features(tid)[0]
track = sp.track(tid)
artists = [i["name"] for i in track["artists"]]
name = track["name"]
# final_analysis = {i:analysis[i] for i in features  }
# print(final_analysis)
song_info = {"name" : name,
             "artists" : artists}
print(song_info)




