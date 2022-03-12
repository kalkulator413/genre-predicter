import cv2
import urllib.request
import numpy as np

def graphics(text, song, artist, link):
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