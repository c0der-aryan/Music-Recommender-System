import json

json_path = "song_data/selected_users.json"

with open(json_path, 'r') as file:
    data = json.load(file)

# Print the JSON data
print(json.dumps(data[10], indent=4))  # Pretty-print with indentation

data_pt = data[10]

print(data_pt["SongIDs"])