import torch
import numpy as np

genres = ['electronic', 'folk', 'hip_hop', 'jazz', 'pop', 'rock']

def get_song_tensor(name, artist, cache, sp):
  if (name, artist) in cache:
    return cache[(name, artist)]

  results = sp.search(q="track:" + name + " artist:" + artist, type="track")
  track_id = results['tracks']['items'][0]['id']
  artist = results['tracks']['items'][0]['artists'][0]['name']
  name = results['tracks']['items'][0]['name']
  img_link = results['tracks']['items'][0]['album']['images'][0]['url']

  f = sp.audio_features(track_id)[0]
  song = np.array([
      f['danceability'], 
      f['energy'], 
      f['loudness'], 
      f['speechiness'], 
      f['acousticness'], 
      f['instrumentalness'], 
      f['liveness'], 
      f['valence'], 
      f['tempo']
  ])
  song = torch.tensor(song).reshape(9).float()
  cache[(name, artist)] = (song, img_link)
  return song, img_link

def get_genre(name, artist, cache, model, sp):
  song, img_link = get_song_tensor(name, artist, cache, sp)  

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
    if secondary_confidence > .6:
      to_return += f'Secondary genre: {secondary_genre} ({round(int(10000*secondary_confidence))/100}% confidence)\n'

  return to_return, artist, name, img_link