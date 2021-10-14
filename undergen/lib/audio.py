from typing import TYPE_CHECKING

import requests

if TYPE_CHECKING:
    from undergen.lib.data import Character

url = "https://api.15.ai/app/getAudioFile5"
cdn_url = "https://cdn.15.ai/audio/"
headers = {'authority': 'api.15.ai',
           'access-control-allow-origin': '*',
           'accept': 'application/json, text/plain, */*',
           'dnt': '1',
           'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
           'content-type': 'application/json;charset=UTF-8',
           'sec-gpc': '1',
           'origin': 'https://15.ai',
           'sec-fetch-site': 'same-site',
           'sec-fetch-mode': 'cors',
           'sec-fetch-dest': 'empty',
           'referer': 'https://15.ai/',
           'accept-language': 'en-US,en;q=0.9'}


def get_sound(character: "Character", text: str):
    character_name = character.sound_name
    emotion = "Normal"

    response = requests.post(url, json = {
        "character": character_name,
        "emotion": emotion,
        "text": text
    }, headers = headers)

    if response.status_code != 200:
        raise RuntimeError(f"15.ai responded with code {response.status_code}.")

    data_json = response.json()
    wav_name = data_json["wavNames"][0]

    second_response = requests.get(cdn_url + wav_name)

    if second_response.status_code != 200:
        raise RuntimeError(f"15.ai CDN responded with code {second_response.status_code}.")

    return second_response.content
