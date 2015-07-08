#!/usr/bin/python

# Import the required modules
import cv2, os
import numpy as np
import paho.mqtt.client as mqtt
from PIL import Image

# For face detection we will use the Haar Cascade provided by OpenCV.
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

# For face recognition we will the the LBPH Face Recognizer 
recognizer = cv2.createLBPHFaceRecognizer()


def on_publish(cli, userdata, mid):
  # Disconnect after our message has been sent.
  cli.disconnect()


def dif_gaussian(img, sigma0 = 1.0, sigma1 = 2.0):
	g1 = cv2.GaussianBlur(img,(0,0),sigma0)
	#cv2.imshow('gauss1',g1)
	#cv2.waitKey(2000)
	g2 = cv2.GaussianBlur(img,(0,0),sigma1)
	#cv2.imshow('gauss2',g2)
	#cv2.waitKey(2000)
	result = g1 - g2
	return np.uint8(result)
	
def gamma_correction(img, correction):
    img2 = img/255.0
    img3 = cv2.pow(img2, correction)
    return np.uint8(img3*255)

	
def get_images_and_labels(path):
    # Append all the absolute image paths in a list image_paths
    # We will not read the image with the .sad extension in the training set
    # Rather, we will use them to test our accuracy of the training
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if not f.endswith('.sad')]
    # images will contains face images
    images = []
    # labels will contains the label that is assigned to the image
    labels = []
    for image_path in image_paths:
        # Read the image and convert to grayscale
        image_pil = Image.open(image_path)#.convert('L')
        # Convert the image format into numpy array
        image = np.array(image_pil, 'uint8')
        #img_gamma = gamma_correction(image,1.2)
        #img_gauss = dif_gaussian(img_gamma)
        # Get the label of the image
        img_hist = cv2.equalizeHist(image)		
        nbr = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
        # Detect the face in the image
        faces = faceCascade.detectMultiScale(img_hist)
        # If face is detected, append the face to images and the label to labels
        for (x, y, w, h) in faces:
            images.append(image[y: y + h, x: x + w])
            labels.append(nbr)
            #cv2.imshow("Adding faces to traning set...", image[y: y + h, x: x + w])
            #cv2.waitKey(50)
    # return the images list and labels list
    return images, labels

# Path to the Yale Dataset
path = './dataset'
# Call the get_images_and_labels function and get the face images and the 
# corresponding labels
images, labels = get_images_and_labels(path)
cv2.destroyAllWindows()

# Perform the tranining
recognizer.train(images, np.array(labels))

# Append the images with the extension .sad into image_paths
#'L' converting image to grayscale 
predict_image_pil = Image.open('test1.jpg').convert('L')

predict_image = np.array(predict_image_pil, 'uint8')

#predict_gamma = gamma_correction(predict_image,0.2)
#cv2.imshow('gamma',predict_gamma)
#cv2.waitKey(2000)
#predict_gauss = dif_gaussian(predict_gamma,1.0,2.0)
#cv2.imshow('gauss',predict_gauss)     
#cv2.waitKey(2000)
#predict_hist = cv2.equalizeHist(predict_gauss)
#cv2.imshow('hist',predict_image)
#cv2.waitKey(2000)
faces = faceCascade.detectMultiScale(predict_image,scaleFactor = 1.2)

for (x, y, w, h) in faces:
	nbr_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
	
	print "{} is Correctly Recognized with confidence {}".format(nbr_predicted, conf)
	'''
	cv2.imshow("Recognizing Face", predict_image[y: y + h, x: x + w])
	count = 0
	cv2.waitKey(2000)
	'''
	'''
	while(os.path.isfile(path + '/subject' + str(nbr_predicted) + '.' + str(count) + '.jpg') == True):
		count += 1
		
	cv2.imwrite(path + '/subject' + str(nbr_predicted) + '.' + str(count) + '.jpg',predict_image[y: y + h, x: x + w])
	'''
Subject = nbr_predicted
name  = ''
if(Subject == 16):
	name = 'Lincoln'
elif(Subject == 18):
	name = 'Yiran'
elif(Subject == 20):
	name = 'Andrew'
else:
	name = 'stranger'
	
print ('Hello ' + name) 

cli = mqtt.Mosquitto("image-send")
cli.connect("54.173.42.47")
cli.on_publish = on_publish

#send image
cli.publish("response",name,1)

cli.loop_forever()