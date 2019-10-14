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
from imutils.face_utils import FaceAligner
import tkinter as tk
import shutil
from threading import Thread
import dlib

refresh = False
FR_model = load_model('nn4.small2.v1.h5')
face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
T = None
data = []

def display_text(): 
    T.delete(1.0,tk.END)
    value = ""
    for index, item in enumerate(data):
        value += str(index + 1) + ". " + str(item) + "\n"
    T.insert(tk.END, value)

def callback(e):
    data.append(str(e.get()))
    display_text()
    e.delete(0, tk.END)

def update_past_notes(user_name): 
    global data
    file_name = user_name + ".txt"
    with open(file_name, 'w+') as output_file: 
        for line in data: 
            output_file.write(str(line) + "\n")

def clear_dir(dir_to_clear):
	dir_to_clear = os.path.join(os.getcwd(), dir_to_clear)
	for item in os.listdir(dir_to_clear): 
		shutil.rmtree(os.path.join(dir_to_clear, item))

def remove_text(second, user_name): 
	try:
		name = str(second.get())
		value = int(name) - 1
		if value < 0: 
			update_past_notes(user_name)
			if refresh:
				clear_dir("images")
			exit()
		if value >= 0 and value < len(data): 
			data.pop(value)
		display_text()
		second.delete(0, tk.END)
	except Exception as error_message:
		print(error_message)

def get_past_user_data(user_name, data): 
	file_name = user_name + ".txt"
	if os.path.exists(file_name): 
		with open(file_name) as past_data: 
			lines = past_data.readlines()
			for line in lines: 
				line = line.strip()
				base = line
				if '\n' in line:
					base = line[:line.index('\n')]
				data.append(base)
			if len(data) > 0: 
				display_text()

def runner(user_name):
    global T, data

    master = tk.Tk()
    master.title(user_name)
    size = 50

    separator = tk.Frame(height=10, bd=1, relief=tk.SUNKEN)
    separator.pack(fill=tk.X, padx=5, pady=5)

    e = tk.Entry(master, width = size)
    e.pack()
    e.focus_set()

    b = tk.Button(master, text="Add Note", width=10, command= lambda: callback(e))
    b.pack(pady = 10)

    separator = tk.Frame(height=10, bd=1, relief=tk.SUNKEN)
    separator.pack(fill=tk.X, padx=5, pady=5)

    buffer = tk.Text(master, height = 1, width = size)
    buffer.insert(tk.INSERT, "Enter index to remove (-1 to quit):")
    buffer.pack()

    separatorthree = tk.Frame(height=10, bd=1, relief=tk.SUNKEN)
    separatorthree.pack(fill=tk.X, padx=5, pady=5)

    second = tk.Entry(master, width = size)
    second.pack()
    second.focus_set()
    
    remove_button = tk.Button(master, text="Remove", width=10, command= lambda: remove_text(second, user_name))
    remove_button.pack(pady = 10)

    separatordoes = tk.Frame(height=10, bd=1, relief=tk.SUNKEN)
    separatordoes.pack(fill=tk.X, padx=5, pady=5)

    S = tk.Scrollbar(master)
    T = tk.Text(master, height = 4, width = 50)
    S.pack(side=tk.RIGHT, fill=tk.Y)
    T.pack(side=tk.LEFT, fill=tk.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)

    get_past_user_data(user_name, data)

    tk.mainloop() 

def add_image_for_user(): 
	
	base_stuff =  []

	def capture_name(entry_box, root, base_stuff): 
		text = str(entry_box.get())
		base_stuff.append(text)
		root.destroy()

	def add_seperator():
		separator = tk.Frame(height=10, bd=1, relief=tk.SUNKEN)
		separator.pack(fill=tk.X, padx=5, pady=5)
	
	def user_gui(base_stuff):
		width_of_box = 40
		master = tk.Tk()
		buffer = tk.Text(master, height = 1, width = width_of_box)
		buffer.insert(tk.INSERT, "Enter name of new user:")
		buffer.pack()
		add_seperator()
		second = tk.Entry(master, width = width_of_box)
		second.pack()
		second.focus_set()
		add_seperator()
		remove_button = tk.Button(master, text="Submit", width=int(width_of_box/5), command= lambda: capture_name(second, master, base_stuff))
		remove_button.pack()
		tk.mainloop()
	
	t = Thread(target= user_gui, args = (base_stuff, ))
	t.start()
	detector = dlib.get_frontal_face_detector()
	shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
	face_aligner = FaceAligner(shape_predictor, desiredFaceWidth=200)
	face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
	video_capture = cv2.VideoCapture(0)
	t.join()

	name = str(base_stuff[0])
	path = 'images'
	directory = os.path.join(path, name)
	if not os.path.exists(directory):
		os.makedirs(directory, exist_ok = 'True')

	number_of_images = 0
	MAX_NUMBER_OF_IMAGES = 25
	count = 0

	while number_of_images < MAX_NUMBER_OF_IMAGES:
		ret, frame = video_capture.read()

		frame = cv2.flip(frame, 1)

		frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		#faces = face_cascade.detectMultiScale(frame, 1.3, 5)
		faces = detector(frame_gray)
		if len(faces) == 1:
			face = faces[0]
			(x, y, w, h) = face_utils.rect_to_bb(face)
			face_img = frame_gray[y-50:y + h+100, x-50:x + w+100]
			face_aligned = face_aligner.align(frame, frame_gray, face)

			if count == 5:
				cv2.imwrite(os.path.join(directory, str(name + "_" + str(number_of_images)+'.jpg')), face_aligned)
				number_of_images += 1
				count = 0
			count+=1
		
		display = cv2.copyMakeBorder(frame, 0, 1, 0, 0, cv2.BORDER_CONSTANT, value= (0, 0, 0))
		height, width, depth = display.shape
		bottom_y, top_y = int(height - 50), int(height)
		bottom_x, top_x = int(0), int((width * number_of_images)/MAX_NUMBER_OF_IMAGES)
		cv2.rectangle(display, (bottom_x, bottom_y), (top_x, top_y), (255, 255, 255), -1)
		cv2.putText(display, "Please look at the camera ", (30, 45), cv2.FONT_HERSHEY_COMPLEX, 1.25, (255, 255, 255), 2)
		cv2.imshow('Video', display)

		if(cv2.waitKey(1) & 0xFF == ord('q')):
			break

	video_capture.release()
	cv2.destroyAllWindows()

	return name

def main_method():
	threshold = 0.5
	face_database = {}
	return_value = -1
	pause = False

	for name in os.listdir('images'):
		for image in os.listdir(os.path.join('images',name)):
			identity = os.path.splitext(os.path.basename(image))[0]
			face_database[identity] = img_path_to_encoding(os.path.join('images',name,image), FR_model)

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
			cv2.putText(frame, "Press A to add user", (20, frame.shape[0] - 15), cv2.FONT_HERSHEY_DUPLEX, 1.5, (255, 255, 255), 1)
		cv2.imshow('Face Recognition System', frame) 

		if person_found != None: 
			pause = True
			break

		actual_reading = cv2.waitKey(1) & 0xFF
		if(actual_reading == ord('q')):
			break
		if(actual_reading == ord('a')): 
			person_found = "-1"
			break

	video_capture.release()
	
	if pause: 
		k = cv2.waitKey(450) & 0xFF

	cv2.destroyAllWindows() 

	return person_found


if __name__ == "__main__":
	user_name = main_method()
	while(user_name == "-1"): 
		add_image_for_user()
		user_name = main_method()
	runner(user_name)
	