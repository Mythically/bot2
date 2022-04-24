import os
from spotify_playing_token_refresh import tokenManager
import requests

# SPOTIFY_ACCESS_TOKEN = os.environ['SPOTIFY_ACCESS_TOKEN']
SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'


def get_current_track(access_token):
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    # print(access_token)
    print(response)
    json_resp = response.json()
    # print(json_resp)

    track_name = json_resp['item']['name']
    artists = [artist for artist in json_resp['item']['artists']]
    link = json_resp['item']['external_urls']['spotify']

    artist_names = ', '.join([artist['name'] for artist in artists])

    current_track_info = {
        "track_name": track_name,
        "artists": artist_names,
        "link": link
    }
    return track_name + " by " + artist_names + " " + link


def get_song(channel_name, ctx_channel):
    access_token = tokenManager(channel_name, ctx_channel)
    os.environ['SPOTIFY_ACCESS_TOKEN'] = access_token
    return get_current_track(access_token)
