import json, requests 

url = "https://spotify-scraper.p.rapidapi.com/v1/search"

querystring = {"term":"Thinking Out Loud","type":"track"}

headers = {
	"x-rapidapi-key": "7c69ed93edmsh738092811b387a1p1156a6jsn88f01c2b66d3",
	"x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(json.dumps(response.json(),indent=4))