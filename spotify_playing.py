import os
from datetime import time
from pprint import pprint

import requests

SPOTIFY_ACCESS_TOKEN = "BQBOYKS-4kyYYf6Yw2aMPLhE08cOAgpmmczYmo8gUp45Mp6roea_Gr-Gi541fCyiepIj4C682rzAJze-QrNAxYq55Iwn3fgqRs0tmVTbV_mxFMx9LC0boGGbOileaM1_Yf5jHAissALla6dwEaHu_TrAloMvk6tkiI85"
SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'


def get_current_track():
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            "Authorization": f"Bearer {os.environ['FLOW_CODE']}"
        }
    )
    json_resp = response.json()
    print(json_resp)
    track_name = json_resp['item']['name']
    artists = [artist for artist in json_resp['item']['artists']]

    link = json_resp['item']['external_urls']['spotify']

    artist_names = ', '.join([artist['name'] for artist in artists])

    current_track_info = {
        "track_name": track_name,
        "artists": artist_names,
        "link": link
    }

    return current_track_info


def main():
    current_track_id = None
    while True:
        current_track_info = get_current_track()

        if current_track_info['id'] != current_track_id:
            pprint(
                current_track_info,
                indent=4,
            )
            current_track_id = current_track_info['id']

        time.sleep(1)


if __name__ == '__main__':
    main()