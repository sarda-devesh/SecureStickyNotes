import cv2
import numpy as np
import os
import dlib
from imutils import face_utils
from imutils.face_utils import FaceAligner
import tkinter as tk
import shutil

def add_image_for_user(): 
	
	detector = dlib.get_frontal_face_detector()
	shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
	face_aligner = FaceAligner(shape_predictor, desiredFaceWidth=200)

	face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

	base_stuff =  []

	def capture_name(entry_box, root, base_stuff): 
		text = str(entry_box.get())
		base_stuff.append(text)
		root.destroy()

	def add_seperator():
		separator = tk.Frame(height=10, bd=1, relief=tk.SUNKEN)
		separator.pack(fill=tk.X, padx=5, pady=5)

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

	name = str(base_stuff[0])
	video_capture = cv2.VideoCapture(0)

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

		cv2.imshow('Video', display)

		if(cv2.waitKey(1) & 0xFF == ord('q')):
			break

	video_capture.release()
	cv2.destroyAllWindows()

	return name

if __name__ == '__main__': 
	new_user_name = add_image_for_user()
	print(new_user_name)
	