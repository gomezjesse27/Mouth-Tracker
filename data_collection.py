import sys
import cv2
import pygame
import numpy as np
import random
import csv
import pygame_widgets
from pygame_widgets.button import ButtonArray
from pygame_widgets.slider import Slider
from config import *
from emoji_drawing import draw_emoji

training_set_name = 'training_set.csv'
header = [f'pix{i}' for i in range(RESOLUTION * RESOLUTION)] + TARGET_NAMES[:TARGET_COUNT] # The first row of the CSV file
done = False

# The face will morph according to these keyframes when calibration starts
# cal_keyframes = [
#     # (seconds, [smile, mouth_open, puff, frown])
#     (0, [0, 0, 0]),
#     (2, [1, 0, 0]),
#     (4, [1, 1, 0]),
#     (6, [0, 0, 0]),
#     (8, [0, 0, 1]),
#     (10, [0, 0, 0]),
#     ]  # For calibration
cal_keyframe_timescale = 2 # seconds between keyframes
cal_keyframes = [
    # (seconds (generated lol), [smile, mouth_open, puff, frown])
    [0, [0, 0, 0]],
    [2, [1, 0, 0]],
    [4, [1, 1, 0]],
    [6, [0, 0, 0]],
    [8, [0, 1, 0]],
    [10, [0, 0, 0]],
    [12, [0, 0, 1]],
    [14, [0, 0, 0]],
    ]  # For calibration
# The time of the latest keyframe
cal_length = cal_keyframes[-1][0]

target_values = [0 for _ in range(TARGET_COUNT)]
calibrating = False
calibration_start_time = 0
font = pygame.font.Font(None, 36)


def get_interpolated_values(time):
    # Find the two keyframes
    keyframe_before = max((t for t in cal_keyframes if t[0] <= time), key=lambda t: t[0])
    try:
        keyframe_after = min((t for t in cal_keyframes if t[0] >= time), key=lambda t: t[0])
    except ValueError:
        # Handle the case where there are no keyframes after 'time'
        keyframe_after = None
        return [0 for _ in range(TARGET_COUNT)]

    # Calculate the ratio
    if keyframe_before == keyframe_after:
        return keyframe_before[1]
    else:
        ratio = (time - keyframe_before[0]) / (keyframe_after[0] - keyframe_before[0])

    # Interpolate the values
    return [v_before + ratio * (v_after - v_before) for v_before, v_after in zip(keyframe_before[1], keyframe_after[1])]

def save_datapoint(frame, target_values):
    # Save a datapoint to the CSV file
    normalized_training_frame = np.round(frame / 255.0, 3)
    datapoint = list(normalized_training_frame.flatten())
    for value in target_values:
        datapoint.append(value)
    with open(training_set_name, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(datapoint)

def clear_training_set():
    with open(training_set_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

def two_target_calibration():
    # Your mouse controls the two target values. Hold click to save datapoints.
    screen_width, screen_height = pygame.display.get_surface().get_size()
    mouse_position = pygame.mouse.get_pos()
    normalized_mouse_position = (mouse_position[0] / screen_width, mouse_position[1] / screen_height)
    return normalized_mouse_position # use [0] and [1] as your two target values

def newCsv():
    # Start the CSV file with the header
    with open(training_set_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

def data_collection_init():
    global done
    done = False

def doneButtonClick():
    global done
    done = True

def calButtonClick():
    global calibrating, calibration_start_time
    if not calibrating:
        calibrating = True
        calibration_start_time = pygame.time.get_ticks()
        newCsv()
    else:
        calibrating = False
    print(cal_keyframes)

def update_config(variable, increment):
    global WEBCAM_ID, RESOLUTION, TARGET_COUNT
    if variable == 'WEBCAM_ID':
        WEBCAM_ID += increment
        if WEBCAM_ID < 0:
            WEBCAM_ID = 0
    elif variable == 'RESOLUTION':
        RESOLUTION += increment * 8
        if RESOLUTION < 8:
            RESOLUTION = 8
        print(f'Resolution: {RESOLUTION}')
    elif variable == 'TARGET_COUNT':
        TARGET_COUNT += increment
        if TARGET_COUNT < 1:
            TARGET_COUNT = 1
        elif TARGET_COUNT > len(TARGET_NAMES):
            TARGET_COUNT = len(TARGET_NAMES)

def get_config_var(variable):
    if variable == 'WEBCAM_ID':
        return WEBCAM_ID
    elif variable == 'RESOLUTION':
        return RESOLUTION
    elif variable == 'TARGET_COUNT':
        return TARGET_COUNT

def make_config_control(screen, events, x, y, variable, update_func):
    # Make - and + button
    b = ButtonArray(screen, x, y, 60, 32, (2, 1), border=2,
        texts=('-', '+'),
        onClicks=(lambda: update_func(variable, -1), lambda: update_func(variable, 1)),
    )
    # Text above
    font = pygame.font.Font(None, 16)
    text = font.render(f"{variable}: {get_config_var(variable)}", True, (255, 255, 255))
    screen.blit(text, (x, y - 15))
    pygame_widgets.update(events)

def data_collection_update(screen, events, cap):
    global calibrating, calibration_start_time, target_values, done
    # Read the current frame from the webcam
    ret, frame = cap.read()

    # Resize the frame to training size
    resized_frame = cv2.resize(frame, (RESOLUTION, RESOLUTION))
    training_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

    # Convert grayscale frame to RGB again for Pygame
    rgb_frame = cv2.cvtColor(training_frame, cv2.COLOR_GRAY2RGB)
    pygame_frame = pygame.image.frombuffer(rgb_frame.tobytes(), rgb_frame.shape[1::-1], "RGB")
    pygame_frame = pygame.transform.scale(pygame_frame, (300, 300))

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                calButtonClick()
            elif event.key == pygame.K_BACKSPACE: # Backspace for "try again". Clears the training set.
                clear_training_set()
            elif event.key == pygame.K_RETURN:
                done = True

    if calibrating:
        time_passed = (pygame.time.get_ticks() - calibration_start_time) / 1000
        target_values = get_interpolated_values(time_passed)
        if time_passed > cal_length:
            calibrating = False
        save_datapoint(training_frame, target_values)

    #### DRAW ########################################################
    screen.fill((0, 0, 30))
    # Draw the camera image
    screen.blit(pygame_frame, (350, 40))
    
    draw_emoji(16, 40, 256, target_values)

    # Render the target value as text and draw it
    for i in range(TARGET_COUNT):
        pygame.draw.rect(screen, (200, 0, 255), (450, 360 + 20 * i, int(200 * target_values[i]), 30))
        target_text = font.render(f'{TARGET_NAMES[i]}: {round(target_values[i], 3)}', True, (255, 255, 255))
        screen.blit(target_text, (450, 360 + 20 * i))
    
    # Controls ----
    buttonArray = ButtonArray(screen, 800 - 130, 2, 130, 60, (1, 2), border=2,
        texts=('Start Cal' if not calibrating else 'Stop Cal', 'Done'),
        onClicks=(calButtonClick, doneButtonClick),
    )
    cfg_x, cfg_y = 0, 400
    # Only the first one will even respond to clicks... idk why
    make_config_control(screen, events, cfg_x, cfg_y, 'WEBCAM_ID', update_config)
    make_config_control(screen, events, cfg_x, cfg_y + 50, 'RESOLUTION', update_config)
    make_config_control(screen, events, cfg_x, cfg_y + 100, 'TARGET_COUNT', update_config)
    make_config_control(screen, events, cfg_x, cfg_y + 150, 'ALGORITHM', update_config)

    pygame_widgets.update(events)  # Call once every loop to allow widgets to render and listen
    return done