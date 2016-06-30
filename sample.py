"""Application to host a website that displays related artists on spotify"""
import urllib.request
import urllib.parse
import urllib.error
import flask
from flask import request
import spotipy
import spotipy.oauth2 as auth
from secrets import client_id, client_secret
import random


#############################
# Magical list of things
#
# Must do:
#   Error Page
#
#
#############################

CACHE = '.spotipyoauthcache'
APP = flask.Flask(__name__)
SPOTIFY = spotipy.Spotify()
IDS = []
ACCESS = auth.SpotifyOAuth(
    client_id,
    client_secret,
    "http://localhost:8080/callback/q",
    scope="playlist-modify-public",
    cache_path=CACHE)

def find_artist(name):
    """Given a text string search for an artist that closly matches it"""
    if type(name) is not str:
        return None
    if name == "":
        return None
    formattedname = name.replace(" ", "+")
    results = SPOTIFY.search(q='artist:' + formattedname, type="artist")
    artist_info = []
    artist_info.append(results["artists"]["items"][0]["id"])
    artist_info.append(results["artists"]["items"][0]["name"])
    return artist_info

def get_related_artist(artist_id):
    """Select a random related artist to the given artist"""
    artist_info = []
    results = SPOTIFY.artist_related_artists(artist_id)
    rel_len = len(results["artists"])
    artist_index = random.randrange(rel_len)
    artist_info.append(results["artists"][artist_index]["id"])
    artist_info.append(results["artists"][artist_index]["name"])
    return artist_info

def generate_artist_string(ids):
    """Generate a readable representation of the chosen artists"""
    artiststring = ""
    counter = 0
    for artist in ids:
        artiststring += artist[1]
        if counter < len(ids) - 1:
            counter += 1
            artiststring += ", "
    return artiststring

def generate_artist_id_list(user_authenticated_wrapper, ids):
    """Generate a list of artist ids"""
    tracks = []
    for artist in ids:
        for song in user_authenticated_wrapper.artist_top_tracks(artist[0])['tracks'][:5]:
            tracks.append(song['id'])
    return tracks

def create_playlist():
    """Create and fill a playlist with songs from the selected artists"""
    access_token = ""
    token_info = ACCESS.get_cached_token()

    if token_info:
        access_token = token_info['access_token']
    else:
        url = request.url
        code = ACCESS.parse_response_code(url)
        if code:
            token_info = ACCESS.get_access_token(code)
            access_token = token_info['access_token']
    if access_token:
        user_authenticated_wrapper = spotipy.Spotify(access_token)
        artiststring = generate_artist_string(IDS)
        playlist_id = user_authenticated_wrapper.user_playlist_create(
            "relatedartistbot",
            artiststring)['id']
        tracks = generate_artist_id_list(user_authenticated_wrapper, IDS)
        user_authenticated_wrapper.user_playlist_add_tracks(
            user_authenticated_wrapper.me()['id'],
            playlist_id, tracks)
        playlisturl = "http://open.spotify.com/user/relatedartistbot/playlist/" + playlist_id
        return playlisturl
    return False

def generate_list(name):
    """Generates a list of artist ids for populating playlist"""
    artist_info = find_artist(name)
    ids = []
    ids.append(artist_info)
    for _ in range(4):
        related_id = get_related_artist(artist_info[0])
        while related_id in ids:
            related_id = get_related_artist(artist_info[0])
        ids.append(related_id)
        artist_info = related_id
    return ids

def send_url_request(url):
    """Quick url sending function REMOVE ME"""
    req = urllib.request.Request(url)
    urllib.request.urlopen(req)

def main():
    """Nothing much here, just spinning up a server"""
    APP.run(debug=True, use_reloader=False, port=8080, host='')

def html_for_auth():
    """Generate the html that will be inserted into the page"""
    return "<a href='" + ACCESS.get_authorize_url() + "'>Generate A Playlist</a>"

@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    auth.SpotifyClientCredentials(client_id, client_secret)
    send_url_request(ACCESS.get_authorize_url())

    return flask.render_template('index.html')

@APP.route('/', methods=['POST'])
def my_form_post():
    """ Respond to user form post then display page
        with results
    """
    text = request.form['text']
    global IDS
    IDS = generate_list(text)
    return flask.render_template('display.html', ids=IDS, html_auth=ACCESS.get_authorize_url())

@APP.route('/callback/q')
def callback():
    """ Will be called when spotify calls back
        with the user's authentication
    """
    playlisturl = create_playlist()
    if not playlisturl:
        return "callback broken"
    else:
        return flask.render_template('result.html', playlistlink=playlisturl)

if __name__ == "__main__":
    main()
