import json

json_path = "song_data/selected_users.json"

with open(json_path, 'r') as file:
    data = json.load(file)

# Print the JSON data
print(json.dumps(data[10], indent=4))  # Pretty-print with indentation

data_pt = data[10]

song_ids = data_pt["SongIDs"]
ids_to_compare = song_ids[:-1]
to_compare = song_ids[-1]

for i in ids_to_compare : 
    # find that id in file 
    # apply the sim score 
    # if we have lyrics available then use sim funt 1 
    # else use sim func 2
    pass