import cv2
import numpy as np
from pyray import *

webcam_dimension = 24

def resize_frame(frame, width, height):
    return cv2.resize(frame, (width, height))

def convert_to_grayscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def main():
    set_config_flags(ConfigFlags.FLAG_VSYNC_HINT)
    init_window(800, 600, "Webcam Feed")

    # Open the webcam
    cap = cv2.VideoCapture(0)

    while not window_should_close():
        # Capture webcam frame
        ret, frame = cap.read()
        # less pixels for less features
        resized_frame = resize_frame(frame, webcam_dimension, webcam_dimension)
        # Convert frame to grayscale
        grayscale_frame = convert_to_grayscale(resized_frame)

        begin_drawing()
        clear_background(WHITE)
        # Draw the frame
        draw_texture(load_texture_from_image(grayscale_frame), 0, 0, WHITE)

        end_drawing()

    close_window()
    # Release the webcam
    cap.release()

if __name__ == "__main__":
    main()