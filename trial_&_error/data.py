import pandas as pd

file_to_filter = 'song_data/songs_data.csv'
file_with_ids = 'song_data/missing_lyrics_songs.csv'
output_file = 'song_data/output_file.csv'

df_to_filter = pd.read_csv(file_to_filter)
df_with_ids = pd.read_csv(file_with_ids)

# filtered_df = df_to_filter[~df_to_filter['song_id'].isin(df_with_ids['song_id'])]
filtered_df = df_to_filter[df_to_filter['sentiments'] != '[]']
filtered_df = filtered_df[filtered_df['song_title'] != '']

filtered_df.drop(columns = ["artist_names" , "song_id"] , inplace=True)

filtered_df.to_csv(output_file, index=False)
print(f"Filtered data saved to {output_file}")
