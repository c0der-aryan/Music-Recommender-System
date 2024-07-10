import os , json , spotipy , pandas as pd, numpy as np , csv , time , scipy, networkx as nx 

from functools import reduce
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint


class GenreRecommender():
    def __init__(self, song_data_filepath : str):
        self.song_data_filepath = song_data_filepath
        with open(self.song_data_filepath,'r',encoding='utf-8') as f: self.song_data = json.loads(f.read())

        self.song_genre_dict = { d['SongID'] : list(set(d['SongData']['genre']+d['SongData']['artists'][0]['genre'])) for d in self.song_data}
        self.songs = sorted(list(set([x['SongID'] for x in self.song_data])))
        self.genres = sorted(list(set(reduce(lambda x,y: x+y , [x['SongData']['genre'] + x['SongData']['artists'][0]['genre'] for x in self.song_data]))))
        self.num_songs = len(self.songs)
        self.num_genres = len(self.genres)

        self.graph = nx.Graph()
        self.graph.add_nodes_from(self.songs)
        self.graph.add_nodes_from(self.genres)
        for a,b in self.song_genre_dict.items():
            for g in b:
                self.graph.add_edge(a,g)
    def genreLoss(self,songid1 , songid2):
        a1 = set(self.graph.neighbors(songid1))
        a2 = set(self.graph.neighbors(songid2))
        return 1.5 * np.exp(-3/2*len(a1.intersection(a2)))
        
genre_rec = GenreRecommender("song_data/filtered_songdata.json")


print(genre_rec.genreLoss('0VjIjW4GlUZAMYd2vXMi3b', '1bDbXMyjaUIooNwFE9wn0N'))

p