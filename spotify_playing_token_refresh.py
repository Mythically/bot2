import os

import requests

refresh_token = os.environ['SPOTIFY_REFRESH_TOKEN5']
refresh_token_link = "https://accounts.spotify.com/api/token"
client_base64 = os.environ['SPOTIFY_CLIENT_DETAILS_BASE64']


def get_new_token():
    print("Refreshing token....")
    response = requests.post(refresh_token_link,
                             data={"grant_type": "refresh_token",
                                   "refresh_token": refresh_token},
                             headers={"Authorization": f"Basic {client_base64}"})
    resp_json = response.json()
    print(resp_json)
    return resp_json['access_token']



