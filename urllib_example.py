import json
import urllib.request, urllib.parse, urllib.error
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

spotify = spotipy.Spotify()

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

def main():
    name = "Bob Dylan"
    artistInfo = find_artist(name)
    
    IDs = []
    IDs.append(artistInfo)
    for i in range(3):
        print(artistInfo[0])
        relatedID = get_related_artist(artistInfo[0])
        while relatedID in IDs:
            relatedID = get_related_artist(artistInfo)
        IDs.append(relatedID)
        artistInfo = relatedID
    print(IDs)

    #token = util.prompt_for_user_token('relatedartistbot', "playlist-modify-public", client_id, client_secret)
    #print(token)
    #credentials = auth.SpotifyClientCredentials(client_id, client_secret)
   

if __name__ == "__main__":
    main()

