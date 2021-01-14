from urllib2 import urlopen
import cv2
import numpy as np


def image_from_url(url):
    rep = urlopen(url).read()
    image = np.asarray(bytearray(rep), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


repertoire='./home/student/Vision/DS/Images'
lien_img="http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=n04096066"
img_url=urlopen(lien_img).read()
i=0
for url in img_url.split('\n'):
    try:
        chemin=repertoire+'image_'+str(i)+'.jpg'
        image=image_from_url(url)
        cv2.imwrite(chemin,image)
        i+=1
    except:
        pass
