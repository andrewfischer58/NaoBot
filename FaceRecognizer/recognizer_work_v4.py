#!/usr/bin/python

# Import the required modules
import cv2, os
import paho.mqtt.client as mqtt
import numpy as np
#from PIL import Image
import Image
import publish_name
import types
import time
from scipy import ndimage
from pymongo import MongoClient

# For face detection we will use the Haar Cascade provided by OpenCV.
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

# For face recognition we will the the LBPH Face Recognizer 
recognizer = cv2.createLBPHFaceRecognizer()

#Mongo DB
client = MongoClient('localhost', 27017)

db = client.pollsapp

collection =  db.faceImages


def on_publish(cli, userdata, mid):
  # Disconnect after our message has been sent.
  print 'Message sent'
  cli.disconnect()

def is_empty(any_structure):
    if any_structure:
        print('Structure is not empty.')
        return False
    else:
        print('Structure is empty.')
        return True

def dif_gaussian(img, sigma0 = 1.0, sigma1 = 2.0,alpha = 0.1, tau = 10.0, gamma = 0.2):
	img = np.array(img, dtype=np.float32)
	img = np.power(img, gamma)
	result = np.asarray(ndimage.gaussian_filter(img,sigma0) - ndimage.gaussian_filter(img,sigma1))
	result = result / np.power(np.mean(np.power(np.abs(result),alpha)), 1.0/alpha)
	result = result / np.power(np.mean(np.power(np.minimum(np.abs(result),tau),alpha)), 1.0/alpha)
	result = tau*np.tanh(result/tau)

	return result  
  
  
  
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
	faces = faceCascade.detectMultiScale(predict_image, scaleFactor = 1.2)
	
	print faces
	# If faces is empty, then the cascade found no faces on the picture
	
	if isinstance(faces,types.TupleType):
	#no faces
		print 'No faces were found!'
		#publish_name.main()
		cli = mqtt.Mosquitto("FaceResults")
		cli.connect("54.173.42.47")
		cli.on_publish = on_publish
		time.sleep(5)
		cli.publish('response','Stranger',2)
	
	else:
	#found face
		# Applies the recognition to the frame where the face was detected
		for (x, y, w, h) in faces:
			predict_gauss = dif_gaussian(predict_image)
			nbr_predicted, conf = recognizer.predict(predict_gauss[y: y + h, x: x + w])
			
			# As confidence is actually the Distance, we subtract it of 100 to create a more logical confidence
			conf100 = 100.0 - conf
			
			# If a match is found, the name is sent to the robot
			if nbr_predicted != -1:
				#Find name that matches the key predicted.
				print 'Face found!' 
				print "{} is Correctly Recognized with confidence {}".format(nbr_predicted, conf)
				count = 0
				
				while(os.path.isfile(path + '/subject' + str(nbr_predicted) + '.' + str(count) + '.jpg') == True):
					count += 1
		
				cv2.imwrite(path + '/subject' + str(nbr_predicted) + '.' + str(count) + '.jpg',predict_image[y: y + h, x: x + w])
				
				
				Subject = nbr_predicted
				
				post = collection.find_one({"id": Subject})
					
				#print "Are you " + post['firstname'] + ' ' + post['lastname']
                                name = "You are recognized as " +post['name']+", with "+str(int(conf100))+" percent confidence. Hello, "+post['name']
                                print name
##				response = raw_input('Enter your answer: ')
##				print response
##			
##				if (response == 'yes'):
##					print 'Hello ' + post['firstname']
##                                        name = post['firstname'] + ' ' + post['lastname']
##				else:
##					print 'Who are you?' 
##					#place speech to text function here 
##					response = raw_input('Enter your first name: ') 
##					#and here
##					response1 = raw_input('Enter your last name: ')
##					name=response +  ' ' + response1
##					post = collection.find({"firstname": response, 'lastname': response1})
##
##					if (post.count()==0):
##						print 'What is your full name?'
##					else:
##						for i in post:
##							print 'Hello ' + i['firstname'] + ' ' + i['lastname']
				cli = mqtt.Mosquitto("FaceResults")
				cli.connect("54.173.42.47")
				cli.on_publish = on_publish
				time.sleep(3)
				cli.publish('response', name,2)
				break






                        else:
                                print 'No faces were found!' 
                                cli.publish('response','Null',2)

		
		#used to test and publish the image of the source/taken picture 
		#publish_name.main(nbr_predicted, conf)
	
	
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
        #img_hist = cv2.equalizeHist(image)
		
        nbr = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
        # Detect the face in the image
        faces = faceCascade.detectMultiScale(image)
        # If face is detected, append the face to images and the label to labels
        for (x, y, w, h) in faces:
            image_gauss = dif_gaussian(image)
            images.append(image_gauss[y: y + h, x: x + w])
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
#cv2.destroyAllWindows()

# Perform the training
recognizer.train(images, np.array(labels))
print 'Training complete!'
# Connect to MQTT server and wait for images
cli = mqtt.Client("Receiver",1883)


cli.on_message = on_message
cli.on_connect = on_connect

cli.connect("54.173.42.47")

cli.subscribe("presence",2)

cli.loop_forever()
