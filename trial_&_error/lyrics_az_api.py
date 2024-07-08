import os
import time
import json
import azapi
import spotipy
import requests
import pandas as pd

from pprint import pprint
from dotenv import load_dotenv
from transformers import pipeline

from spotipy.oauth2 import SpotifyClientCredentials
song_title = "On My Way"
artists = ['Alan Walker', 'Sabrina Carpenter', 'Farruko']

final_search = song_title + artists[0]

def get_song_lyrics_2(artist , song_title) : 

    API = azapi.AZlyrics('google', accuracy=0.5)

    API.artist = artist
    API.title = song_title

    API.getLyrics(save=True, ext='lrc')
    
    return API.lyrics

# c = time.time()
# lrcs = get_song_lyrics_2(artists[0] , song_title)
# f = time.time()

# print(f-c)

def get_song_lyrics_1(id) : 

    url_spotify_api_lrcs = "https://spotify23.p.rapidapi.com/track_lyrics/"
    headers = {
        "x-rapidapi-key": "c3a0ff933cmsh9c6ca83440520f7p1f106ajsn86d70f424094",
        "x-rapidapi-host": "spotify23.p.rapidapi.com"
    }

    # Rate limit and retry logic
    while True:
        song_lyrics = requests.get(url_spotify_api_lrcs, headers=headers, params={"id": id})
        if song_lyrics.status_code == 429:  # Too Many Requests
            retry_after = int(song_lyrics.headers.get("Retry-After", 1))
            time.sleep(retry_after)
        else:
            break
 
    # song_lyrics = requests.get(url_spotify_api_lrcs, headers=headers, params={"id" : id})
    song_lrcs_json = song_lyrics.json()
    # print(json.dumps(song_lrcs_json))

    lrcs = " ".join([i["words"] for i in song_lrcs_json["lyrics"]["lines"]])
    return lrcs

def get_song_lyrics(id , artist , song_title) : 
    try : 
        lrcs = get_song_lyrics_1(id)
    except : 
        lrcs = get_song_lyrics_2(artist , song_title)
    return lrcs

def get_song_lyrics(id ) : 
    try : 
        lrcs = get_song_lyrics_1(id)
    except : 
        lrcs = " "
    return lrcs

id = "03kRGW8x3iBxcvjmDU1I0Q"
artist = "DAKU"
song_title = "Adhura"
a = []
a.append(get_song_lyrics(id))
print(a)