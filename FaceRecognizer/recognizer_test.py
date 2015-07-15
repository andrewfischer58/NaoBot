#!/usr/bin/python

# Import the required modules
import cv2, os
import numpy as np
from PIL import Image
import types
from scipy import ndimage
from pymongo import MongoClient

# For face detection we will use the Haar Cascade provided by OpenCV.
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

client = MongoClient('localhost', 27017)

db = client.pollsapp

collection =  db.faceImages

def gamma_correction(img, correction):
    return np.power(img,correction)
	
	
# For face recognition we will the the LBPH Face Recognizer 
recognizer = cv2.createLBPHFaceRecognizer(threshold = 50)

def dif_gaussian(img, sigma0 = 1.0, sigma1 = 2.0,alpha = 0.1, tau = 10.0):
	img = np.array(img, dtype=np.float32)
	#img = np.power(img,0.2)
	img = gamma_correction(img,0.2)
	result = np.asarray(ndimage.gaussian_filter(img,sigma0) - ndimage.gaussian_filter(img,sigma1))
	result = result / np.power(np.mean(np.power(np.abs(result),alpha)), 1.0/alpha)
	result = result / np.power(np.mean(np.power(np.minimum(np.abs(result),tau),alpha)), 1.0/alpha)
	result = tau*np.tanh(result/tau)

	return result
	#return np.uint8(result)

	
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
        image_pil = Image.open(image_path).convert('L')
        # Convert the image format into numpy array
        image = np.array(image_pil, 'uint8')

        # Get the label of the image
        
        nbr = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
		
        # Detect the face in the image
        faces = faceCascade.detectMultiScale(image)
        # If face is detected, append the face to images and the label to labels
        for (x, y, w, h) in faces:
            predict_gauss = dif_gaussian(image,1.0,2.0)
            images.append(predict_gauss[y: y + h, x: x + w])
			
            #images.append(image[y: y + h, x: x + w])
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

predict_image_pil = Image.open('16.jpg').convert('L')

predict_image = np.array(predict_image_pil, 'uint8')


faces = faceCascade.detectMultiScale(predict_image,scaleFactor = 1.2)
print faces

if isinstance(faces,types.TupleType):
	print 'No faces'
else:
	for (x, y, w, h) in faces:
		predict_gauss = dif_gaussian(predict_image)
		nbr_predicted, conf = recognizer.predict(predict_gauss[y: y + h, x: x + w])
		if(nbr_predicted != -1):		
			print "{} is Correctly Recognized with confidence {}".format(nbr_predicted, conf)
			
			cv2.imshow("Recognizing Face", predict_gauss[y: y + h, x: x + w])
			count = 0
			
			while(os.path.isfile(path + '/subject' + str(nbr_predicted) + '.' + str(count) + '.jpg') == True):
				count += 1
				
			#cv2.imwrite(path + '/subject' + str(nbr_predicted) + '.' + str(count) + '.jpg',predict_image[y: y + h, x: x + w])
			cv2.waitKey(5000)
			
			Subject = nbr_predicted
			
			
			if(Subject == 16):
				name = 'Lincoln'
			elif(Subject == 17):
				name = 'Chris'
			elif(Subject == 18):
				name = 'Yiran'
			elif(Subject == 19):
				name = 'Ning'
			elif(Subject == 20):
				name = 'Andrew'
			elif(Subject == 21):
				name = 'Jeff'
			else:
				name = 'stranger'
			'''
			post = collection.find_one({"SubjectID": Subject})
					
			print "Are you " + post['firstname'] + ' ' + post['lastname']
			
			response = raw_input('Enter your answer: ')
			print response
			
			if (response == 'yes'):
				print 'Hello ' + post['firstname']
			else:
				print 'Who are you?' 
				response = raw_input('Enter your first name: ') 
				response1 = raw_input('Enter your last name: ')
				
				post = collection.find({"firstname": response, 'lastname': response1})

				if (post.count()==0):
					print 'What is your full name?'
				else:
					for i in post:
						print 'Hello ' + i['firstname'] + ' ' + i['lastname']
		break
		'''
			print ('Hello ' + name)