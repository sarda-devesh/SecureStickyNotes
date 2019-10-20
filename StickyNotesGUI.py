import cv2 
import os 
import numpy as np

class Note: 

    def __init__(self, startingnote, x_cord, y_cord): 
        self.note = startingnote
        self.x = x_cord
        self.y = y_cord

    def set_text(self, updated): 
        self.note = updated
    
    def update_coords(self, new_x, new_y): 
        self.x = new_x
        self.y = new_y

width = 1000
height = 800

ENTER = 13
BACKSPACE = 8
ESPACE = 27
UPARROW = 61
DOWNARROW = 45

white = (255, 255, 255)
blue = (255, 0, 0)
locations = []

x_start = 40
y_start = 25
y_increment = 50
circle_radius = 5
current_index = 0

locations.append(Note("", x_start, y_start))

while(True): 
    k = cv2.waitKey(1) & 0xFF
    if k == ESPACE: 
        break
    elif k == UPARROW: 
        current_index = min(len(locations) - 1, current_index + 1)
    elif k == DOWNARROW: 
        current_index = max(0, current_index - 1)
    elif k == BACKSPACE: 
        if len(locations[current_index].note) > 0:
            last = locations[current_index].note
            last = last[:-1]
            locations[current_index].set_text(last)
        if len(locations[current_index].note) == 0 and current_index > 0: 
            old_stuff = locations.pop(current_index)
            for index in range(current_index, len(locations)): 
                point = locations[index]
                new_x = point.x
                new_y = point.y - y_increment
                point.update_coords(new_x, new_y)
            current_index = min(current_index, len(locations) - 1)
    elif k == ENTER: 
        text_to_put = ""
        x_cord = x_start
        y_cord = locations[len(locations) - 1].y + y_increment
        locations.append(Note(text_to_put, x_cord, y_cord))
        current_index += 1
    elif (k >= 97 and k <= 122) or (k >= 65 and k <= 90) or (k >= 48 and k <= 57) or k == 32:
        add = str(chr(k))
        current = locations[current_index].note
        updated = current + add
        locations[current_index].set_text(updated)

    frame = np.zeros((height, width, 3), np.uint8)
    for index in range(len(locations)): 
        point = locations[index]
        color = white
        text_to_write = point.note
        if index == current_index:
            color = blue
            text_to_write += "|"
        circle_center_x = point.x - 4 * circle_radius
        circle_center_y = point.y - circle_radius
        cv2.circle(frame, (circle_center_x, circle_center_y), circle_radius, color, -1)
        cv2.putText(frame, text_to_write, (point.x, point.y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
    cv2.imshow("Notes section", frame)

cv2.destroyAllWindows()