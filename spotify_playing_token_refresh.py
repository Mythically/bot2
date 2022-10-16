import os
import requests
import botDB
from typing import TypedDict


class dbInfo(TypedDict):
    token: str
    token_time: float
    channel_name: str


refresh_token = os.environ["SPOTIFY_REFRESH_TOKEN"]
refresh_token_link = "https://accounts.spotify.com/api/token"
client_base64 = os.environ["SPOTIFY_CLIENT_DETAILS_BASE64"]


def getFinalTokenPair(channel_name):
    response = requests.get(
        "https://accounts.spotify.com/api/token",
        headers={"Authorization": f"Basic {client_base64}"},
        data={
            "grant_type": "authorization_code",
            "code": "auth_code",
            "redirect_uri": "http://localhost",
        },
    ).json()
    # code  = response.code
    # if botDB.insetSpotifyRefreshToken():


def tokenManager(channel_name, ctx_channel):
    token: str = botDB.fetchToken(channel_name, ctx_channel)[0]["refreshToken"]
    token_time: float = float(botDB.fetchToken(channel_name, ctx_channel)[0]["time"])

    print(token, token_time)
    print("Checking token age....")
    if botDB.checkTokenAge(token_time):
        return token

    else:
        print("Refreshing token....")
        response = requests.post(
            refresh_token_link,
            data={"grant_type": "refresh_token", "refresh_token": refresh_token},
            headers={"Authorization": f"Basic {client_base64}"},
        )
        resp_json = response.json()
        new_token = resp_json["access_token"]
        botDB.updateToken(channel_name, new_token, ctx_channel)
        print(resp_json)
        return new_token
