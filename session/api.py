import requests
user = input("Enter tv show name")
url = requests.get(f"https://api.tvmaze.com/search/shows?q={user}")
data = url.json()
print(data)