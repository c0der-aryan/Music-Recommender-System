import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch , ast
import json , pandas as pd, numpy as np , networkx as nx 

from functools import reduce
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint

# tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
# model = AutoModel.from_pretrained('bert-base-uncased')

# def cosine_similarity_genres(sentence1, sentence2):
#     global tokenizer, model
#     def sent_maker (sent): 
#         sent = ast.literal_eval(sent)[:2]
#         sent = ", ".join(sent)    
#         return sent
    
#     def get_sentence_embedding(sentence):
#         inputs = tokenizer(sentence, return_tensors='pt', truncation=True, padding=True)
#         with torch.no_grad():
#             outputs = model(**inputs)
#         sentence_embedding = outputs.last_hidden_state[:, 0, :]
#         return sentence_embedding

#     embedding1 = get_sentence_embedding(sent_maker(sentence1))
#     embedding2 = get_sentence_embedding(sent_maker(sentence2))

#     embedding1 = torch.nn.functional.normalize(embedding1, p=2, dim=1)
#     embedding2 = torch.nn.functional.normalize(embedding2, p=2, dim=1)

#     return torch.nn.functional.cosine_similarity(embedding1, embedding2).item()

def pearson_correlation_sentiments (vec1, vec2):
    mean_vec1 = np.mean(vec1)
    mean_vec2 = np.mean(vec2)
    numerator = np.sum((np.array(vec1) - mean_vec1) * (np.array(vec2) - mean_vec2))
    denominator = np.sqrt(np.sum((np.array(vec1) - mean_vec1)**2)) * np.sqrt(np.sum((np.array(vec2) - mean_vec2)**2))
    return 1 - (numerator / denominator)

class GenreRecommender():
    def __init__(self):
        self.song_data_filepath = "song_data/filtered_songdata.json"
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

id1 = "0VjIjW4GlUZAMYd2vXMi3b"  
id2 = "1bDbXMyjaUIooNwFE9wn0N"

genre_rec = GenreRecommender()
genre_loss = genre_rec.genreLoss(id1, id2)

sp_analysis_loss_list = ["danceability","energy","key","loudness","mode","speechiness","acousticness","instrumentalness","liveness","valence","tempo"]

def individual_index_similarity(vec1, vec2):
    similarities = [abs(a - b) / max(abs(a), abs(b)) if max(abs(a), abs(b)) != 0 else 1 for a, b in zip(vec1, vec2)]
    return similarities

df = pd.read_csv("/Users/aryansood/Github/Music-Recommender-System/song_data/output_file.csv")
for index , row in df.iterrows():
    if index == 0 : 
        sp_analysis_1 = [row[i] for i in sp_analysis_loss_list]
    elif index == 1 : 
        sp_analysis_2 = [row[i] for i in sp_analysis_loss_list]
    else : break

print(sp_analysis_1)
print(sp_analysis_2)
print(individual_index_similarity(sp_analysis_1 , sp_analysis_2))