import sys
import os
import json
import spotipy
import spotipy.util as util
import webbrowser
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

def connectWithYouTube():
    CLIENT_SECRET_FILE = 'client_secret.json'
    YT_SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, YT_SCOPES)
    credentials = flow.run_console()
    youtube = build('youtube', 'v3', credentials=credentials)
    print(type(youtube))
    return youtube

def getLikeYouTubeVideos(youtube):
    likeVideosList = []
    request = youtube.playlistItems().list(
        playlistId='LLlY4Roho4V3-gunrDEifPsA',
        part='snippet',
        maxResults=50
    )
    response = request.execute()
    for item in response['items']:
        likeVideosList.append(item['snippet']['title'])
        print(item['snippet']['title'])

    return likeVideosList

def checkIfSongInSpotify():
    pass

def createEmptySpotifyPlaylist():
    pass

def connectWithSpotify():
    pass

def addSongsToSpotifyPlaylist():
    pass

youtube = connectWithYouTube()
youtubeLikedVideos = []
youtubeLikedVideos=getLikeYouTubeVideos(youtube)

print(youtubeLikedVideos)