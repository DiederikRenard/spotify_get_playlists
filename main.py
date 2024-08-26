# We are going to make an automation script that takes Spotify playlists and makes lists of youtube-urls
# with the file of youtube_urls you could potentially make a nice playlist on youtube...
# maybe even another thing that ISN'T illegal... I DO NOT CONDONE USING YOUTUBE TO MP3 CONVERTERS SUCH AS:
# https://ytmp3s.nu/6ufl/
# https://y2mate.nu/Pio1/
# https://notube.lol/fr/youtube-app-3

import os
import base64
import urllib.parse

from requests import post, get
import json
from flask import Flask, redirect, request, jsonify, session
import urllib
from datetime import datetime

# TO-DO: FIND SPOTIFY-API
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_KEY = os.environ['CLIENT_KEY']
REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

app = Flask(__name__)
app.secret_key = '5444521123544jscsk'


@app.route('/')
def index():
    return 'Welcome to my Spotify App!<a href="/login">Login</a>'


@app.route('/login')
def login():
    scope = 'user-read-private user-read-email'

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True,
    }

    auth_url = f'{AUTH_URL}?{urllib.parse.urlencode(params)}'

    return redirect(auth_url)


@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({'error': request.args['error']})

    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_KEY,
        }

        response = post(url=TOKEN_URL, data=req_body)
        token_info = response.json()
        print(token_info)
        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

        return redirect('/playlists')


@app.route('/playlists')
def get_playlists():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f'Bearer {session["access_token"]}'
    }

    response = get(API_BASE_URL + 'me/playlists', headers=headers)

    playlists = response.json()

    return jsonify(playlists)


@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_KEY
        }

        response = post(TOKEN_URL, data=req_body)
        new_token_info = response.json()
        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

        return redirect('/playlists')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

# send POST request to the token endpoint URL.
# def get_token():
#     auth_string: str = CLIENT_ID + ':' + CLIENT_KEY
#     auth_bytes = auth_string.encode('utf-8')
#     auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
#
#     url = "https://accounts.spotify.com/api/token"
#     headers = {
#         "Authorization": "Basic " + auth_base64,
#         "Content-Type": "application/x-www-form-urlencoded",
#
#     }
#     data = {"grant_type": "client_credentials"}
#     result = post(url, headers=headers, data=data)
#     json_result = json.loads(result.content)
#     auth_token = json_result["access_token"]
#     # print(json_result)
#     return auth_token


# Function for getting an auth_token
def get_auth_token(token):
    return {"Authorization": "Bearer " + token}





def search_for_playlist(token, search_query, search_type):
    url = "https://api.spotify.com/v1/me/playlists"
    headers = get_auth_token(token)
    # query = f"?q={search_query}&type={search_type}&limit=1"

    query_url = url
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    print(json_result)


token1 = get_token()
# auth_code = get_auth_code()
# print(auth_code)
print(search_for_playlist(token1, "Energy-Metal-Faolan", "playlist"))

# TO-DO: USE API TO MAKE LIST OF SONGS: ARTIST


# TO-DO: USE LIST TO FIND YOUTUBE-URLS


# TO-DO: MAKE LIST OF YOUTUBE-URLS


# TO-DO: USE YOUTUBE URLS TO CONVERT TO MP3 - WITHOUT INFRINGING ON COPYRIGHT (personal responsibility req.)


# TO-DO: ENJOY
