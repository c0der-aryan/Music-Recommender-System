import os
import time
import json
import pandas as pd
import requests
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from transformers import pipeline, AutoTokenizer

load_dotenv()
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
# RAPID_API_KEY = os.getenv('RAPID_API_KEY')
RAPID_API_KEY = '9b26345b0bmsh1c2507c6907e090p167f5ejsn8d07cf522582'
RAPID_API_KEYS = ["c3a0ff933cmsh9c6ca83440520f7p1f106ajsn86d70f424094",
                  "2dc6ff46e1msh3a45f918ceff202p19e4b0jsn4927726f0857",
                  ]

API_KEY_INDEX = 0

# Initialize Transformers pipeline and tokenizer
pipe = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", device=0)
tokenizer = AutoTokenizer.from_pretrained("j-hartmann/emotion-english-distilroberta-base")

# Initialize Spotipy client
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# def get_song_lyrics_1(id):
#     global RAPID_API_KEY , API_KEY_INDEX
#     url_spotify_api_lrcs = "https://spotify23.p.rapidapi.com/track_lyrics/"
#     headers = {
#         "x-rapidapi-key": RAPID_API_KEY,
#         "x-rapidapi-host": "spotify23.p.rapidapi.com"
#     }
#     cnt = 0
#     while True:
#         song_lyrics = requests.get(url_spotify_api_lrcs, headers=headers, params={"id": id})
#         if song_lyrics.status_code == 429:  # Too Many Requests
            
#             API_KEY_INDEX +=1
#             if API_KEY_INDEX < len(RAPID_API_KEYS) : 
#                 print("on api number : " , API_KEY_INDEX+1)
#                 RAPID_API_KEY = RAPID_API_KEYS[API_KEY_INDEX]
#                 headers = {
#                     "x-rapidapi-key": RAPID_API_KEY,
#                     "x-rapidapi-host": "spotify23.p.rapidapi.com"
#                 }
#                 song_lyrics = requests.get(url_spotify_api_lrcs, headers=headers, params={"id": id})
#             else : 
#                 print("api keys used up")
#                 break

#         elif song_lyrics.status_code == 401:  # Unauthorized
#             return ""
#         elif song_lyrics.status_code == 404:  # Not Found
#             return ""
#         elif song_lyrics.status_code == 200:
#             break
#         else:
#             song_lyrics.raise_for_status()
#     song_lrcs_json = song_lyrics.json()
#     lrcs = " ".join([i["words"] for i in song_lrcs_json["lyrics"]["lines"]])
#     lrcs = ""
#     return lrcs

def get_song_lyrics_1(id):
    global RAPID_API_KEY

    url_spotify_api_lrcs = "https://spotify23.p.rapidapi.com/track_lyrics/"
    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": "spotify23.p.rapidapi.com"
    }

    while True:
        song_lyrics = requests.get(url_spotify_api_lrcs, headers=headers, params={"id": id})
        if song_lyrics.status_code == 429:  # Too Many Requests
            retry_after = int(song_lyrics.headers.get("Retry-After", 3))
            print("Retry-After " , retry_after)
            time.sleep(retry_after)
        elif song_lyrics.status_code == 401:  # Unauthorized
            return ""
        elif song_lyrics.status_code == 404:  # Not Found
            return ""
        elif song_lyrics.status_code == 200:
            break
        else:
            song_lyrics.raise_for_status()

    song_lrcs_json = song_lyrics.json()
    lrcs = " ".join([i["words"] for i in song_lrcs_json["lyrics"]["lines"]])
    return lrcs


def get_song_lyrics(id):
    try:
        lrcs = get_song_lyrics_1(id)
    except requests.RequestException as e:
        print(f"Error fetching lyrics for song {id}: {e}")
        lrcs = ""
    return lrcs

def langs(lrcs):
    global RAPID_API_KEY
    url = "https://language-identify-detector.p.rapidapi.com/languageIdentify"

    payload = {"text": lrcs}
    headers_1 = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": "language-identify-detector.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers_1)
    response.raise_for_status()
    langs = response.json()["languageCodes"]

    top_langs = [i["code"] for i in langs if i["confidence"] > 0.1]
    return top_langs

def song_info_loader(id, genres, artist_ids, artists, name, missing_lyrics_list):
    global pipe, tokenizer , RAPID_API_KEY , API_KEY_INDEX

    tid = f'spotify:track:{id}'
    
    analysis = sp.audio_features(tid)[0]
    track = sp.track(tid)
    
    lrcs = get_song_lyrics(id)
    if lrcs != "" and lrcs != " ":
        tokens = tokenizer(lrcs, truncation=True, max_length=512, return_tensors="pt")
        truncated_lrcs = tokenizer.decode(tokens.input_ids[0], skip_special_tokens=True)
        output = pipe(truncated_lrcs)
        scores = {i["label"]: i["score"] for i in output if i["score"] > 0.1}
        lst = ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]
        sentiments = [scores.get(key, 0) for key in lst]
        languages = langs(truncated_lrcs)
    else:
        sentiments = []
        languages = []
        # Add song details to missing lyrics list
        missing_lyrics_list.append({
            "song_title": name,
            "artist_names": str(artists),
            "artist_ids": str(artist_ids),
            "song_id": id  # Include song ID for reference
        })

    exp = track["explicit"]
    album = track["album"]
    release_date = album["release_date"]

    song_info = {
        "song_title": name,
        "explicit": exp,
        "artists": str(artists),
        "artist_ids": str(artist_ids),
        "genres": str(genres),
        "release_date": release_date,
        "lyrics": lrcs,
        "sentiments": str(sentiments),
        "languages": str(languages)
    }
    try : 
        song_info.update(analysis)
    except : 
        pass
    return song_info

try : 
    main_df = pd.read_csv("song_data/songs_data.csv")
    cSongs = set(main_df['song_title'])
except :
    main_df = pd.DataFrame({})
    cSongs = set([])

try : 
    missing_lyrics_df = pd.read_csv("song_data/missing_lyrics_songs.csv")
except :
    missing_lyrics_df = pd.DataFrame([])

temp_list = []
missing_lyrics_list = []
cnt = 0

# Ask the user for the starting and ending count
start_count = 0
end_count = 10000

with open("song_data/filtered_songdata.json", 'r') as file:
    dataset = json.load(file)

for songnum , song in enumerate(dataset[start_count:end_count]):
    cnt += 1
    id = song["SongID"]
    song_data = song["SongData"]
    name = song_data["title"]
    genres = song_data["genre"]

    if name in cSongs: continue
    artists = [i["name"] for i in song_data["artists"]]
    artist_ids = [artist["id"] for artist in song_data["artists"]]
        
    temp_list.append(song_info_loader(id, genres, artist_ids, artists, name, missing_lyrics_list))
    cSongs.add(name)
    print(f"Processed song {cnt}",end = "\r")

    if cnt % 10 == 0:
        temp_df = pd.DataFrame(temp_list)
        main_df = pd.concat([main_df, temp_df], ignore_index=True)
        main_df = main_df.drop_duplicates()
        temp_list = []
        main_df.to_csv("song_data/songs_data.csv", index=False)

        miss = pd.DataFrame(missing_lyrics_list)
        missing_lyrics_df = pd.concat([missing_lyrics_df, miss], ignore_index=True)
        missing_lyrics_df = missing_lyrics_df.drop_duplicates()
        missing_lyrics_list = []
        missing_lyrics_df.to_csv("song_data/missing_lyrics_songs.csv", index=False)


        print(" "*50 + f"Concatenated and saved {cnt} songs , index {songnum+start_count}",end="\r")

if temp_list:
    temp_df = pd.DataFrame(temp_list)
    main_df = pd.concat([main_df, temp_df], ignore_index=True)
    main_df.to_csv("songs_data.csv", index=False)
    print( f"Concatenated and saved {cnt} songs\r")

# missing_lyrics_df = pd.DataFrame(missing_lyrics_list)

# miss = pd.DataFrame(missing_lyrics_list)

# missing_lyrics_df = pd.concat([missing_lyrics_df, miss], ignore_index=True)
# missing_lyrics_df.to_csv("missing_lyrics_songs.csv", index=False)
# print("Saved songs with missing lyrics to missing_lyrics_songs.csv")
