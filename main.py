from graphics import graphics
from functions import get_genre
from env import *

import torch
import pickle
with open('model', 'rb') as f: 
    model  = pickle.load(f)
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(SPOTIPY_CID, SPOTIPY_SECRET)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


while 1:
    print('>>> Enter song:')
    song = input()

    print('>>> Enter artist:')
    artist = input()

    try:
        text, artist, song, link = get_genre(song, artist, model, sp)
        text = text.split('\n')
        graphics(text, song, artist, link)
    except IndexError as e:
        print('Could not find the song!')
