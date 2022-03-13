import pickle
import torch
import numpy as np

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

with open('model', 'rb') as f: 
    model  = pickle.load(f)

genres = ['folk', 'rock', 'pop', 'hip-hop', 'electronic']
tempo_max = 220
loudness_max = -60

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