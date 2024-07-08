import os
import time
import spotipy
import requests
import pandas as pd
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

    lrcs = " ".join([i["words"] for i in song_lrcs_json["lyrics"]["lines"]])
    return lrcs

def langs(lrcs) :
    url = "https://language-identify-detector.p.rapidapi.com/languageIdentify"

    payload = { "text": lrcs }
    headers_1 = {
        "x-rapidapi-key": "c3a0ff933cmsh9c6ca83440520f7p1f106ajsn86d70f424094",
        "x-rapidapi-host": "language-identify-detector.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers_1)
    langs = response.json()["languageCodes"]

    top_langs = [i["code"] for i in langs if i["confidence"]>0.1 ]
    return top_langs

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

    exp = track["explicit"]
    dur = track["duration_ms"]
    scores = {i["label"] :  i["score"] for i in output if i["score"]>0.1}
    lst = ["anger" , "disgust" , "fear" , "joy" , "neutral" , "sadness" , "surprise"]
    sentiments = [scores.get(key, 0) for key in lst]

    album = track["album"]
    release_date = album["release_date"]

    artist_ids = []

    for artist in track["artists"]:
        artist_ids.append(artist["id"])

    artists_data = sp.artists(artist_ids)

    genres = []

    for artist in artists_data["artists"]:
        genres += artist["genres"]

    genres = set(genres) # removes duplicates

    song_info = { "song_title" : name,
                 "song_id" : id, 
                 "track_duration" : dur,
                 "explicit" : exp,
                 "artists" : artists,
                 "artist_ids" : artist_ids,
                 "genres" :  genres,
                 "release_date" : release_date,
                 "lyrics" : lrcs,
                 "sentiments" : sentiments, 
                 "languages" : langs(lrcs) }
    
    final_analysis = {i:analysis[i] for i in features  }
    song_info.update(final_analysis)
    return song_info

# import time 
# c = time.time()
# (pd.DataFrame(song_info_loader("4n7jnSxVLd8QioibtTDBDq"))).to_csv("data1.csv")
# f = time.time()
# print(f-c)
# pprint(song_info_loader("0TK2YIli7K1leLovkQiNik"))

# id = "4n7jnSxVLd8QioibtTDBDq"
# print(get_song_lyrics(id))

ids = ["4n7jnSxVLd8QioibtTDBDq" , "0TK2YIli7K1leLovkQiNik" , "4cktbXiXOapiLBMprHFErI" , "2Sl7H4cPHwg0rfNJu9N4eO" ]

data = []
cnt = 0
for id in ids :
    print(cnt)
    c = time.time()
    data.append(song_info_loader(id))
    f = time.time()
    print(f-c)
    cnt+=1
df = pd.DataFrame(data)
df.to_csv('data1.csv', index=False)

# data = pd.read_csv('music_data.csv')
# print(data.head())