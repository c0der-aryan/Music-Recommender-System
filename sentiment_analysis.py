import pandas as pd
from functools import reduce
import pandas as pd, numpy as np , networkx as nx 
from transformers import pipeline, AutoTokenizer

file_path = '/Users/aryansood/Github/Music-Recommender-System/song_data/full_df.pkl'
df = pd.read_pickle(file_path)

df['sentiment'] = '[]'
required_cols = ["track_name" , 'track_id', 'explicit', 'artist_names',
       'artist_ids', 'acousticness', 'danceability', 'energy',
       'instrumentalness', 'liveness', 'loudness',
       'speechiness', 'tempo', 'popular_artist',
       'popular_artist_id', 'combined_genres', 'lyrics']
df = df.loc[: ,required_cols]


# Initialize Transformers pipeline and tokenizer
pipe = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", device=0 , top_k = 7)
tokenizer = AutoTokenizer.from_pretrained("j-hartmann/emotion-english-distilroberta-base")

def sentiments (lrcs) : 
    tokens = tokenizer(lrcs, truncation=True, max_length=512, return_tensors="pt")
    truncated_lrcs = tokenizer.decode(tokens.input_ids[0], skip_special_tokens=True)
    output = pipe(truncated_lrcs)[0]
    scores = {i["label"] : i["score"] for i in output}
    lst = ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]
    sentiments = [scores.get(key, 0) for key in lst]
    return sentiments

for index , row in df.iterrows() : 
    lrcs = str(row["lyrics"])
    if lrcs == "nan" : 
        df.loc[index , "sentiments" ] = str([0,0,0,0,0,0,0])
        continue
    df.loc[index , "sentiments" ] = str(sentiments(lrcs))

    print(f"current song : {index}", end = "\r")
    if index % 10 == 0: 
        df.to_pickle("sentiment_data.pkl")
        print( " "*50 , f"Concatenated and saved {index} songs" , end = "\r")

df.to_pickle("sentiment_data.pkl")