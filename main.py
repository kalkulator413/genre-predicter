from graphics import graphics
from functions import get_genre

while 1:
    print('>>> Enter song:')
    song = input()

    print('>>> Enter artist:')
    artist = input()

    try:
      text, artist, song, link = get_genre(song, artist)
      text = text.split('\n')
      graphics(text, song, artist, link)
    except Exception as e:
        print('Could not find the song!')
        raise Exception('Song Not Found')
        # print(e)