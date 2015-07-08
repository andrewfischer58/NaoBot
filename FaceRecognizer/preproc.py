#!/usr/bin/python

# Import the required modules
import cv2, os
import numpy as np
from PIL import Image

def dif_gaussian(img, sigma0 = 1.0, sigma1 = 2.0):
	img2=[]
	maxi = img.max()
	mini = img.min()
	for pix in img:#np.nditer(img)
		pix = ((pix-mini)/(maxi - mini) * 255
		img2.append(pix)
	
	img2 = np.uint8(img2)
	g1 = cv2.GaussianBlur(img2,(0,0),sigma0)
	#cv2.imshow('gauss1',g1)
	#cv2.waitKey(2000)
	g2 = cv2.GaussianBlur(img2,(0,0),sigma1)
	#cv2.imshow('gauss2',g2)
	#cv2.waitKey(2000)
	result = g1 - g2
	result2 = img + result
	return np.uint8(result2)
	
def gamma_correction(img, correction):
    img2 = img/255.0
    img3 = cv2.pow(img2, correction)
    return np.uint8(img3*255)

	

# Perform the tranining

# Append the images with the extension .sad into image_paths

predict_image_pil = Image.open('preproc.gif').convert('L')

predict_image = np.array(predict_image_pil, 'uint8')

predict_gamma = gamma_correction(predict_image,0.2)
cv2.imshow('gamma',predict_gamma)
cv2.waitKey(2000)
predict_gauss = dif_gaussian(predict_gamma,1.0,2.0)
cv2.imshow('gauss',predict_gauss)     
cv2.waitKey(5000)
predict_hist = cv2.equalizeHist(predict_gauss)
cv2.imshow('hist',predict_hist)
cv2.waitKey(2000)
