import json
import urllib.request, urllib.parse, urllib.error
import flask
from flask import request
import socket
import random
import spotipy
import spotipy.util as util
import spotipy.oauth2 as auth
from secrets import client_id, client_secret


#############################
# Magical list of things
#
# Must do:
#   Refactor from raw url requests to wrapper
#   Generate http and webpage from results
#
# Possible:
#   Genereate User Playlists
#
#############################

CACHE = '.spotipyoauthcache'
APP = flask.Flask(__name__)
spotify = spotipy.Spotify()
IDs = []
acc = auth.SpotifyOAuth(client_id, client_secret, "http://localhost:8080/callback/q", scope="playlist-modify-public", cache_path=CACHE)

def find_artist(name):
    formattedname = name.replace(" ", "+")
    results = spotify.search(q='artist:' + formattedname, type="artist")
    artistInfo = []
    artistInfo.append(results["artists"]["items"][0]["id"])
    artistInfo.append(results["artists"]["items"][0]["name"])
    return artistInfo

def get_artist_top_tracks(artistID):
    url = "https://api.spotify.com/v1/artists/" + artistInfo + "/top-tracks"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        the_page = response.read()
        data = json.loads(the_page.decode('utf-8'))
    print(the_page)

def get_related_artist(artistID):
    artistInfo = []
    print(artistID)
    results = spotify.artist_related_artists(artistID)
    rel_len = len(results["artists"])
    index = random.randrange(rel_len)
    artistInfo.append(results["artists"][index]["id"])
    artistInfo.append(results["artists"][index]["name"])
    return artistInfo

def populate_playlist(userID, playlistInfo, songlist):
    print("placeholder")

def create_playlist(userID):
    url = "https://api.spotify.com/v1/users/" + userID + "/playlists"

def spotify_authenticate():
    url.add_header("Authorization", "Basic " + client_id + ":" + client_secret)
    print(url)
    responseData = urllib.request.urlopen(url)
    print(responseData)

def generate_list(name):
    artistInfo = find_artist(name)
    ids = [] 
    ids.append(artistInfo)
    for i in range(4):
        relatedID = get_related_artist(artistInfo[0])
        while relatedID in ids:
            relatedID = get_related_artist(artistInfo[0])
        ids.append(relatedID)
        artistInfo = relatedID
    return ids

def send_url_request(url):
    req = urllib.request.Request(url)
    urllib.request.urlopen(req)

def main():
    APP.run(debug=True, use_reloader=False, port=8080, host='')



def html_for_auth():
    return "<a href='" + acc.get_authorize_url() + "'>Generate A Playlist</a>"

@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    credentials = auth.SpotifyClientCredentials(client_id, client_secret)
    send_url_request(acc.get_authorize_url())
    print(credentials.get_access_token())

    return flask.render_template('index.html')

@APP.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    IDs = generate_list(text)
    return flask.render_template('display.html', ids=IDs, html_auth=acc.get_authorize_url())
    return ""

@APP.route('/callback/q')
def callback():
    access_token = ""
    token_info = acc.get_cached_token()

    if token_info:
        access_token = token_info['access_token']
    else:
        url = request.url
        code = acc.parse_response_code(url)
        if code:
            token_info = acc.get_access_token(code)
            access_token = token_info['access_token']
    if access_token:
        sp = spotipy.Spotify(access_token)
        playlistID = sp.user_playlist_create("relatedartistbot", "test")['id']
        print(playlistID)
        tracks = []
        for artist in IDs:
            for song in sp.artist_top_tracks(artist[0])['tracks'][:10]:
                tracks.append(song['id'])
        results = sp.current_user()
        return results
    return ""

if __name__ == "__main__":
    main()

