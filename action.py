from bs4 import BeautifulSoup
import re
import base64
images = []
soup = BeautifulSoup(base64.b64decode(open("base64.txt","r").read()))
for img in soup.findAll('img'):
  images.append(img.get('src'))
print(str(images))