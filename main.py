from api_info import *
import torch
import torch.nn as nn
import numpy as np
import pickle

import cv2

import urllib
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

genres = ['folk', 'rock', 'pop', 'hip-hop', 'electronic']
tempo_max = 220
loudness_max = -60
with open('model', 'rb') as f: 
    model  = pickle.load(f)

def get_genre(name, artist):
  results = sp.search(q="track:" + name + " artist:" + artist, type="track")
  track_id = results['tracks']['items'][0]['id']
  artist = results['tracks']['items'][0]['artists'][0]['name']
  name = results['tracks']['items'][0]['name']
  img_link = results['tracks']['items'][0]['album']['images'][0]['url']

  f = sp.audio_features(track_id)[0]
  song = np.array([
      f['danceability'], 
      f['energy'], 
      f['loudness']/loudness_max, 
      f['speechiness'], 
      f['acousticness'], 
      f['instrumentalness'], 
      f['liveness'], 
      f['valence'], 
      f['tempo']/tempo_max
  ])
  song = torch.tensor(song).reshape(9).float()

  t = model(song)
  value = (t == max(t)).nonzero(as_tuple=True)[0].detach()

  to_return = (f'Primary genre: {genres[value]} ({round(int(10000*max(t)))/100}% confidence)\n')
  
  if max(t) < .6:
    t_list = list(t)
    t_list[t_list.index(max(t_list))] = torch.tensor(0)
    secondary_genre = genres[t_list.index(max(t_list))]
    sum = 0
    for val in t_list:
      sum += val.item()
    secondary_confidence = max(t_list) / sum
    if secondary_confidence > .5:
      to_return += f'Secondary genre: {secondary_genre} ({round(int(10000*secondary_confidence))/100}% confidence)\n'

  return to_return, artist, name, img_link

def graphics():
  width = 600
  if len(text) == 3:
    height = 230
  else:
    height = 200
  def start():
    img = 40 * np.ones((height, width, 3), dtype = np.uint8)

    text_size = 2
    if len(song) > 12:
      text_size = 24 / len(song)
    cv2.putText(img, song, (int(width/4), 70), cv2.FONT_HERSHEY_SIMPLEX, text_size, (255, 255, 255), 1, cv2.LINE_AA)
    text_size = 1
    if len(artist) > 22:
      text_size = 22 / len(artist)
    cv2.putText(img, artist, (int(width/4) + 6, 120), cv2.FONT_HERSHEY_SIMPLEX, text_size, (255, 255, 255), 1, cv2.LINE_AA)

    counter = 0
    for line in text:
      cv2.putText(img, line, (20, 166 + 30*counter), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
      counter += 1

    cv2.rectangle(img, (18, 18), (131, 131), (0, 0, 0), 2)

    req = urllib.request.urlopen(link)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    pic = cv2.imdecode(arr, -1) # 'Load it as it is'
    pic = cv2.resize(pic, (110,110), interpolation = cv2.INTER_AREA)

    img[20:130,20:130] = pic[0:110,0:110]

    return img

  img = start()
  cv2.imshow('',img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  

while 1:
    print('>>> Enter song:')
    song = input()

    print('>>> Enter artist:')
    artist = input()

    try:
      text, artist, song, link = get_genre(song, artist)
      text = text.split('\n')
      graphics()
    except Exception as e:
        print('Could not find the song!')
        raise Exception('Song Not Found')
        # print(e)