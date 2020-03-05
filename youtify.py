import sys
import os
import json
import spotipy
import spotipy.util as util
import webbrowser
from typing import List, Dict
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow


def connectWithYouTube():
    CLIENT_SECRET_FILE = 'client_secret.json'
    YT_SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, YT_SCOPES)
    credentials = flow.run_console()
    youtube = build('youtube', 'v3', credentials=credentials)
    return youtube


def getLikeYouTubeVideos(youtube):
    likeVideosList = []
    request = youtube.playlistItems().list(
        playlistId='PLUDiWN5Y39G5lI9s2dBL1zHa_SljpGnTL',
        part='snippet',
        maxResults=50
    )
    response = request.execute()
    for item in response['items']:
        likeVideosList.append(item['snippet']['title'])
        print(item['snippet']['title'])

    return likeVideosList


def connectWithSpotify(username):
    scope = 'playlist-modify-private'
    # scope = 'playlist-modify-public'
    try:
        token = util.prompt_for_user_token(username, scope)
    except:
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username, scope)

    return token


def createEmptySpotifyPlaylist(username, spotifyObject) -> str:
    #spotifyObject.user_playlist_create(username, "YouTubeLiked13", public=False,
    #                                   description='songs copied from youtube liked playlist by python script')

    result = spotifyObject.search(q='YouTubeLiked13', type='playlist')
    print(result)
    for item in result['playlists']['items']:
        playlist_id = item['id']

    print("playlist_id: " + playlist_id)
    return playlist_id


def getTrackIds(spotifyObject, trackDictionary: Dict) -> List[str]:
    trackIdList = []

    for key, value in trackDictionary.items():
        print(key + " | " + value)
        result = spotifyObject.search(q='artist:' + key.replace("'","") + ' track:' + value.replace("'",""), type='track')
        trackIdList.append(result['tracks']['items'][0]['id'])
        #print(json.dumps(result['tracks']['items'][0], indent=4, sort_keys=True))

    return trackIdList


def addSongsToSpotifyPlaylist(spotifyObject, username, playlist_id, track_ids):
    spotifyObject.user_playlist_add_tracks(username, playlist_id, track_ids)


def transformListToDict(youtubeLikedVideos: List) -> Dict:
    trackDict = {}
    for item in youtubeLikedVideos:
        track = item.split(" - ")
        trackDict[track[0]] = track[1]

    return trackDict


# youtube = connectWithYouTube()
# youtubeLikedVideos = []
# youtubeLikedVideos=getLikeYouTubeVideos(youtube)

# print(youtubeLikedVideos)
username = '11124907609'
token = connectWithSpotify(username)
tracksList = ['Taylor Swift - Blank Space', "Guns N' Roses - November Rain", "Guns N' Roses - Don't Cry",
              "Avril Lavigne - When You're Gone", 'Aerosmith - Dream On', 'The Killers - The Man',
              'Coldplay - Yellow']
tracksDict = {}
if token:
    spO = spotipy.Spotify(auth=token)
    playListId = createEmptySpotifyPlaylist(username, spO)
    tracksDict = transformListToDict(tracksList)
    IDsList = getTrackIds(spO, tracksDict)
    addSongsToSpotifyPlaylist(spO, username, playListId, IDsList)

    #for i in IDsList:
    #   print(i + "\n")

else:
    print("Can't get token for", username)

#result = spO.search(q='artist:' + "Guns N Roses" + ' track:' + "Dont Cry", type='track')
#or item in result['tracks']:
#print(json.dumps(result, indent=4, sort_keys=True))
#print(spO.search(q='YouTubeLiked11', type='playlist'))