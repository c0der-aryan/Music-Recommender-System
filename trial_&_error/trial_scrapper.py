# import os
# import json
# import requests

# from pytube import YouTube
# from  pytube import Search 

# from pprint import pprint

# def ytb_url_to_mp3 (url) : 
#     yt = YouTube(url)
#     video = yt.streams.filter(only_audio = True).first()
#     destination = "mp3_files/"
#     out_file = video.download(output_path = destination) 
#     base , _  = os.path.splitext(out_file)
#     new_file = base + ".mp3"
#     os.rename(out_file , new_file)
#     return yt.title

# url_spotify_api= "https://spotify23.p.rapidapi.com/tracks/"
# url_spotify_api_lrcs = "https://spotify23.p.rapidapi.com/track_lyrics/"
# url_lang = "https://language-identify-detector.p.rapidapi.com/languageIdentify"


# def lang_detector (lrcs) : 
    
#     payload = { "text": lrcs }

#     headers_lrcs = {
# 	"x-rapidapi-key": "c3a0ff933cmsh9c6ca83440520f7p1f106ajsn86d70f424094",
# 	"x-rapidapi-host": "language-identify-detector.p.rapidapi.com",
# 	"Content-Type": "application/json"

#     }
#     response = requests.post(url_lang, json=payload, headers=headers)
#     langs = response.json()["languageCodes"]
#     top_langs = [i["code"] for i in langs if i["confidence"]>0.1 ]
#     print(top_langs)







# # querystring = {"id":"4WNcduiCmDNfmTEz7JvmLv"}

# # despa
# # querystring = {"id":"6habFhsOp2NvshLv26DqMb"}

# # omw
# querystring = {"id":"4n7jnSxVLd8QioibtTDBDq"}


# headers = {
#     "x-rapidapi-key": "c3a0ff933cmsh9c6ca83440520f7p1f106ajsn86d70f424094",
#     "x-rapidapi-host": "spotify23.p.rapidapi.com"
# }

# def get_song_info(querystring) : 
#     global headers
#     querystring = {"ids" : querystring["id"]}
#     song_info = requests.get(url_spotify_api, headers=headers, params=querystring)
#     json_metadata = song_info.json()

#     # extracting the name and aritist of the song
#     track = json_metadata["tracks"][0]
#     song_name = track["name"]
#     artists = list(artist["name"] for artist in track["artists"])
#     song_dict = {"song_name" : song_name , "artists" : artists }
#     return song_dict

# def get_song_lyrics(querystring) : 
#     global headers
#     song_lyrics = requests.get(url_spotify_api_lrcs, headers=headers, params=querystring)
#     song_lrcs_json = song_lyrics.json()

#     lrcs = "| ".join([i["words"] for i in song_lrcs_json["lyrics"]["lines"]])
#     return lrcs

# def get_song_lyrics_and_metadata (querystring) : 
#     song_dict = get_song_info(querystring)
#     song_dict["lyrics"] = get_song_lyrics(querystring)
#     return song_dict

# dict1 = get_song_lyrics_and_metadata(querystring)
# pprint(dict1)
# # song_ytb_search = song_name + ", ".join(artists)

# # # Searching the song on YouTube
# # s = Search(song_ytb_search)
# # first_result = s.results[0]

# # url = f"https://www.youtube.com/watch?v={first_result.video_id}"

# # # download ytb vid as mp3
# # name = ytb_url_to_mp3(url)
# # print(name)
# """{
#     "tracks": [
#         {
#             "album": {
#                 "album_type": "single",
#                 "artists": [
#                     {
#                         "external_urls": {
#                             "spotify": "https://open.spotify.com/artist/3t8WiyalpvnB9AObcMufiE"
#                         },
#                         "id": "3t8WiyalpvnB9AObcMufiE",
#                         "name": "Mahmut Orhan",
#                         "type": "artist",
#                         "uri": "spotify:artist:3t8WiyalpvnB9AObcMufiE"
#                     },
#                     {
#                         "external_urls": {
#                             "spotify": "https://open.spotify.com/artist/40Hr91B6wn9pO83Gj0JMrP"
#                         },
#                         "id": "40Hr91B6wn9pO83Gj0JMrP",
#                         "name": "Ali Arutan",
#                         "type": "artist",
#                         "uri": "spotify:artist:40Hr91B6wn9pO83Gj0JMrP"
#                     },
#                     {
#                         "external_urls": {
#                             "spotify": "https://open.spotify.com/artist/5xkqotsRPu6KQ4PiWjSGQf"
#                         },
#                         "id": "5xkqotsRPu6KQ4PiWjSGQf",
#                         "name": "Selin",
#                         "type": "artist",
#                         "uri": "spotify:artist:5xkqotsRPu6KQ4PiWjSGQf"
#                     }
#                 ],
#                 "external_urls": {
#                     "spotify": "https://open.spotify.com/album/1B68g8b4wpedNDvvQLAoCe"
#                 },
#                 "id": "1B68g8b4wpedNDvvQLAoCe",
#                 "images": [
#                     {
#                         "height": 640,
#                         "url": "https://i.scdn.co/image/ab67616d0000b273fa258529452f4ed34cc961b1",
#                         "width": 640
#                     },
#                     {
#                         "height": 300,
#                         "url": "https://i.scdn.co/image/ab67616d00001e02fa258529452f4ed34cc961b1",
#                         "width": 300
#                     },
#                     {
#                         "height": 64,
#                         "url": "https://i.scdn.co/image/ab67616d00004851fa258529452f4ed34cc961b1",
#                         "width": 64
#                     }
#                 ],
#                 "is_playable": true,
#                 "name": "In Control (feat. Selin)",
#                 "release_date": "2020-10-30",
#                 "release_date_precision": "day",
#                 "total_tracks": 1,
#                 "type": "album",
#                 "uri": "spotify:album:1B68g8b4wpedNDvvQLAoCe"
#             },
#             "artists": [
#                 {
#                     "external_urls": {
#                         "spotify": "https://open.spotify.com/artist/3t8WiyalpvnB9AObcMufiE"
#                     },
#                     "id": "3t8WiyalpvnB9AObcMufiE",
#                     "name": "Mahmut Orhan",
#                     "type": "artist",
#                     "uri": "spotify:artist:3t8WiyalpvnB9AObcMufiE"
#                 },
#                 {
#                     "external_urls": {
#                         "spotify": "https://open.spotify.com/artist/40Hr91B6wn9pO83Gj0JMrP"
#                     },
#                     "id": "40Hr91B6wn9pO83Gj0JMrP",
#                     "name": "Ali Arutan",
#                     "type": "artist",
#                     "uri": "spotify:artist:40Hr91B6wn9pO83Gj0JMrP"
#                 },
#                 {
#                     "external_urls": {
#                         "spotify": "https://open.spotify.com/artist/5xkqotsRPu6KQ4PiWjSGQf"
#                     },
#                     "id": "5xkqotsRPu6KQ4PiWjSGQf",
#                     "name": "Selin",
#                     "type": "artist",
#                     "uri": "spotify:artist:5xkqotsRPu6KQ4PiWjSGQf"
#                 }
#             ],
#             "disc_number": 1,
#             "duration_ms": 179232,
#             "explicit": false,
#             "external_ids": {
#                 "isrc": "USUS12000579"
#             },
#             "external_urls": {
#                 "spotify": "https://open.spotify.com/track/1JDwfM6fzE7HtRukcJSZDd"
#             },
#             "id": "1JDwfM6fzE7HtRukcJSZDd",
#             "is_local": false,
#             "is_playable": true,
#             "linked_from": {
#                 "external_urls": {
#                     "spotify": "https://open.spotify.com/track/4WNcduiCmDNfmTEz7JvmLv"
#                 },
#                 "id": "4WNcduiCmDNfmTEz7JvmLv",
#                 "type": "track",
#                 "uri": "spotify:track:4WNcduiCmDNfmTEz7JvmLv"
#             },
#             "name": "In Control (feat. Selin)",
#             "popularity": 50,
#             "preview_url": "https://p.scdn.co/mp3-preview/1d53b96abb564f9ba08427c3c5361dd8fbe72f7d?cid=d8a5ed958d274c2e8ee717e6a4b0971d",
#             "track_number": 1,
#             "type": "track",
#             "uri": "spotify:track:1JDwfM6fzE7HtRukcJSZDd"
#         }
#     ]
# }"""


import requests
# def get_song_lyrics(id) : 

#     url_spotify_api_lrcs = "https://spotify23.p.rapidapi.com/track_lyrics/"
#     headers = {
#         "x-rapidapi-key": "c3a0ff933cmsh9c6ca83440520f7p1f106ajsn86d70f424094",
#         "x-rapidapi-host": "spotify23.p.rapidapi.com"
#     }

#     song_lyrics = requests.get(url_spotify_api_lrcs, headers=headers, params={"id" : id})
#     song_lrcs_json = song_lyrics.json()

#     lrcs = " ".join([i["words"] for i in song_lrcs_json["lyrics"]["lines"]])
#     return lrcs
# print(get_song_lyrics("4n7jnSxVLd8QioibtTDBDq"))

