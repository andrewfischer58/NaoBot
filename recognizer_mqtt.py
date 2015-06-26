#!/usr/bin/python

# Import the required modules
import cv2, os
import paho.mqtt.client as mqtt
import numpy as np
from PIL import Image



# For face detection we will use the Haar Cascade provided by OpenCV.
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

# For face recognition we will the the LBPH Face Recognizer 
recognizer = cv2.createLBPHFaceRecognizer()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
		
def on_message(client, userdata, rc):
	# Receive the image and create a file to process
	print("Message received! ")
	with open("img.jpg","wb") as fd:
		fd.write(rc.payload)
	
	
	# Open the image properly for the face detection
	predict_image_pil = Image.open('img.jpg').convert('L')
	predict_image = np.array(predict_image_pil, 'uint8')
	
	# Uses the cascade to detect a face on the picture
	faces = faceCascade.detectMultiScale(predict_image)
	
	# If faces is empty, then the cascade found no faces on the picture
	if faces == []:
		print 'No faces were found!'
		cli.publish('response','NoFace',1)
	else:
		# Applies the recognition to the frame where the face was detected
		for (x, y, w, h) in faces:
			nbr_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
			
			# As confidence is actually the Distance, we subtract it of 100 to create a more logical confidence
			conf100 = 100.0 - conf
			
			# If a match is found, the name is sent to the robot
			if nbr_predicted != -1:
				#Find name that matches the key predicted.
				print 'Face found!' 
				print "{} is Correctly Recognized with confidence {}".format(nbr_predicted, conf)
				name = 'Name'
				cli.publish('response',name,1)
			else:
				print 'No faces were found!' 
				cli.publish('response','Null',1)
			
		
	
def get_images_and_labels(path):
    # Append all the absolute image paths in a list image_paths
    # We will not read the image with the .sad extension in the training set
    # Rather, we will use them to test our accuracy of the training
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    # images will contains face images
    images = []
    # labels will contains the label that is assigned to the image
    labels = []
    for image_path in image_paths:
        # Read the image and convert to grayscale
        image_pil = Image.open(image_path).convert('L')
		
        # Convert the image format into numpy array
        image = np.array(image_pil, 'uint8')
        # Get the label of the image
        nbr = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
        # Detect the face in the image
        faces = faceCascade.detectMultiScale(image)
        # If face is detected, append the face to images and the label to labels
        for (x, y, w, h) in faces:
            images.append(image[y: y + h, x: x + w])
            labels.append(nbr)
            #cv2.imshow("Adding faces to traning set...", image[y: y + h, x: x + w])
            #cv2.waitKey(50)
    # return the images list and labels list
    return images, labels

	
	
	
# Path to the Yale Dataset
path = './yalefaces'
# Call the get_images_and_labels function and get the face images and the 
# corresponding labels
images, labels = get_images_and_labels(path)
#cv2.destroyAllWindows()

# Perform the tranining
recognizer.train(images, np.array(labels))
print 'Training complete!'
# Connect to MQTT server and wait for images
cli = mqtt.Client("Receiver",1883)
cli.on_message = on_message
cli.on_connect = on_connect

cli.connect("54.173.42.47")

cli.subscribe("presence",2)

cli.loop_forever()
