import cv2
import urllib.request
import numpy as np

from PIL import ImageFont, ImageDraw, Image

def graphics(text, song, artist, link):
  if len(text) == 3:
    height = 230
  else:
    height = 200

  img = 40 * np.ones((height, 600, 3), dtype = np.uint8)
  
  cv2.rectangle(img, (18, 18), (131, 131), (0, 0, 0), 2)

  req = urllib.request.urlopen(link)
  arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
  pic = cv2.imdecode(arr, -1) # 'Load it as it is'
  pic = cv2.resize(pic, (110,110), interpolation = cv2.INTER_AREA)

  img[20:130,20:130] = pic[0:110,0:110]

  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  img = Image.fromarray(img)
  draw = ImageDraw.Draw(img)

  text_size = 50
  if len(song) > 14:
    text_size = int(700 / len(song))
  font = ImageFont.truetype("cour.ttf", text_size)
  draw.text((150, 70), song, font=font, fill=(255, 255, 255), anchor='lb')
  
  text_size = 30
  if len(artist) > 22:
    text_size = int(660 / len(artist))
  font = ImageFont.truetype("cour.ttf", text_size)
  draw.text((156, 110), artist, font=font, fill=(255, 255, 255), anchor='lb')

  img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

  counter = 0
  for line in text:
    cv2.putText(img, line, (20, 166 + 30*counter), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    counter += 1

  cv2.imshow('', img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  