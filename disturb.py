import cv2
import numpy as np
import random


image = cv2.imread('1.jpg')
a = random.random()
b = random.random()
image  =  np.array(image)
image = cv2.resize(image ,(1024 -int(10*b),575 - int(a *10)))
image = image [0:image.shape[0]-int(a*10), 0:image.shape[1]-int(b *5)]
cv2.imshow('s',image)
cv2.waitKey(0)
