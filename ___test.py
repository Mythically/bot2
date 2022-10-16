import requests
result = requests.get("https://api.chucknorris.io/jokes/random").json()
print(result["value"])