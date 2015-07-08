import cv2, os
import numpy as np
from PIL import Image


cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)


predict_image_pil = Image.open('test.jpg').convert('L')
predict_image = np.array(predict_image_pil, 'uint8')
faces = faceCascade.detectMultiScale(predict_image)
print faces
for (x, y, w, h) in faces:
	cv2.imshow("Recognizing Face", predict_image[y: y + h, x: x + w])
	cv2.waitKey(1000000)