'''Face Recognition Main File'''
import cv2
import numpy as np
import glob
from scipy.spatial import distance
from imutils import face_utils
from keras.models import load_model
import tensorflow as tf
import time
from fr_utils import *
from inception_blocks_v2 import *
import os

#with CustomObjectScope({'tf': tf}):
FR_model = load_model('nn4.small2.v1.h5')
print("Total Params:", FR_model.count_params())

face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

threshold = 0.25

face_database = {}

for name in os.listdir('images'):
	for image in os.listdir(os.path.join('images',name)):
		identity = os.path.splitext(os.path.basename(image))[0]
		face_database[identity] = fr_utils.img_path_to_encoding(os.path.join('images',name,image), FR_model)

#print(face_database)
threshold = 0.1

video_capture = cv2.VideoCapture(0)
person_found = None

while True:
	ret, frame = video_capture.read()
	frame = cv2.flip(frame, 1)

	faces = face_cascade.detectMultiScale(frame, 1.3, 5)
	for(x,y,w,h) in faces:
		cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
		roi = frame[y:y+h, x:x+w]
		encoding = img_to_encoding(roi, FR_model)
		min_dist = 100
		identity = None

		for(name, encoded_image_name) in face_database.items():
			dist = np.linalg.norm(encoding - encoded_image_name)
			if(dist < min_dist):
				min_dist = dist
				identity = name.split("_")[0]

		if min_dist < threshold:
			person_found = str(identity)

	if person_found != None: 
		frame = cv2.copyMakeBorder(frame, 0, 30, 0, 0, cv2.BORDER_CONSTANT, value= (0, 0, 0))
		cv2.putText(frame, "Hello " + str(identity) + "!", (10, frame.shape[0] - 25), cv2.FONT_HERSHEY_COMPLEX, 2.5, (255, 255, 255), 2)
	else: 
		cv2.putText(frame, "Looking for you ", (60, 45), cv2.FONT_HERSHEY_COMPLEX, 2.0, (255, 255, 255), 2)
	
	cv2.imshow('Face Recognition System', frame) 

	if person_found != None: 
		k = cv2.waitKey(800) & 0xFF
		break

	if(cv2.waitKey(1) & 0xFF == ord('q')):
		break

video_capture.release()
cv2.destroyAllWindows()

