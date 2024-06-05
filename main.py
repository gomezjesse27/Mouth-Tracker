# It's the main deal!

import sys
import cv2
import pygame
import numpy as np
import random
import csv
import pygame_widgets
from pygame_widgets.button import Button
from enum import Enum
from config import *
from emoji_drawing import draw_emoji
from data_collection import data_collection_init, data_collection_update
from data_preprocessing import data_preprocessing_update, data_preprocessing_init
from modeling_lr import modeling_lr_init, modeling_lr_update
from modeling_cnn import modeling_cnn_init, modeling_cnn_update
from modeling_ann import modeling_ann_init, modeling_ann_update
from modeling_ann_nopca import modeling_ann_nopca_init, modeling_ann_nopca_update
from prediction import prediction_init, prediction_update
from prediction_all import prediction_all_init, prediction_all_update

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS_LIMIT = 30

# Globals -------------------------
cap = cv2.VideoCapture(WEBCAM_ID)


# Functions -----------------------

class ProgramState(Enum):
    DATA_COLLECTION = 1
    DATA_PREPROCESSING = 2
    MODELING = 3
    PREDICTION = 4
    MAX = 5
state = ProgramState.DATA_COLLECTION

def update_webcam():
    global cap
    cap = cv2.VideoCapture(WEBCAM_ID)

def state_to_string(state):
    match state:
        case ProgramState.DATA_COLLECTION:
            return "Data Collection"
        case ProgramState.DATA_PREPROCESSING:
            return "Data Preprocessing"
        case ProgramState.MODELING:
            return "Modeling"
        case ProgramState.PREDICTION:
            return "Prediction"
    return "Unknown"

def set_state(new_state):
    global state
    state = new_state
    match state:
        case ProgramState.DATA_COLLECTION:
            print("Data Collection")
            data_collection_init()
        case ProgramState.DATA_PREPROCESSING:
            print("Data Preprocessing")
            data_preprocessing_init()
        case ProgramState.MODELING:
            print("Modeling")
            if ALGORITHM == Algorithms.LINEAR_REGRESSION:
                modeling_lr_init()
            elif ALGORITHM == Algorithms.CNN:
                modeling_cnn_init()
            elif ALGORITHM == Algorithms.ANN:
                modeling_ann_init()
            elif ALGORITHM == Algorithms.ANN_NOPCA:
                modeling_ann_nopca_init()
            elif ALGORITHM == Algorithms.ALL:
                modeling_lr_init()
                modeling_cnn_init()
                modeling_ann_init()
                modeling_ann_nopca_init()
        case ProgramState.PREDICTION:
            print("Prediction")
            if ALGORITHM == Algorithms.ALL:
                prediction_all_init()
            else:
                prediction_init()

def main():
    # Graphical setup ----------------------------------------------------
    pygame.init()
    pygame.display.set_caption('Calibration-based Mouth Tracking')
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    running = True
    set_state(ProgramState.DATA_COLLECTION)
    # Main loop ---------------------------------------------------------------
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_4:
                    # skip to prediction
                    set_state(ProgramState.PREDICTION)

        screen.fill((0, 50, 50))
        # Update based on state ------------------------   
        match state:
            case ProgramState.DATA_COLLECTION:
                done = data_collection_update(screen, events, cap)
                if done:
                    if ALGORITHM == Algorithms.LINEAR_REGRESSION:
                        set_state(ProgramState.DATA_PREPROCESSING)
                    elif ALGORITHM == Algorithms.CNN:
                        set_state(ProgramState.MODELING) # CNN doesnt use PCA
                    elif ALGORITHM == Algorithms.ANN:
                        set_state(ProgramState.DATA_PREPROCESSING)
                    elif ALGORITHM == Algorithms.ANN_NOPCA:
                        set_state(ProgramState.MODELING)
                    elif ALGORITHM == Algorithms.ALL:
                        set_state(ProgramState.DATA_PREPROCESSING)
            case ProgramState.DATA_PREPROCESSING:
                done = data_preprocessing_update(screen, events)
                if done:
                    set_state(ProgramState.MODELING)
                pass
            case ProgramState.MODELING:
                done = False
                if ALGORITHM == Algorithms.LINEAR_REGRESSION:
                    done = modeling_lr_update(screen, events)
                elif ALGORITHM == Algorithms.CNN:
                    done = modeling_cnn_update(screen, events, cap)
                elif ALGORITHM == Algorithms.ANN:
                    done = modeling_ann_update(screen, events)
                elif ALGORITHM == Algorithms.ANN_NOPCA:
                    done = modeling_ann_nopca_update(screen, events)
                elif ALGORITHM == Algorithms.ALL: # haters gonna hate
                    done = modeling_lr_update(screen, events) and modeling_cnn_update(screen, events, cap) and modeling_ann_update(screen, events) and modeling_ann_nopca_update(screen, events)
                if done:
                    set_state(ProgramState.PREDICTION)
            case ProgramState.PREDICTION:
                if ALGORITHM == Algorithms.ALL:
                    done = prediction_all_update(screen, events, cap)
                else:
                    done = prediction_update(screen, events, cap)
                if done:
                    set_state(ProgramState.DATA_COLLECTION) # Loop back around
                pass
        # Between-frame stuff -----------------------
        # show current state
        title_text = font.render(f'{state_to_string(state)}', True, (255, 255, 255))
        screen.blit(title_text, (10, 10))
        # show what algorithm is being used
        algorithm_text = font.render(f'Algorithm: {algo_to_string(ALGORITHM)}', True, (255, 255, 255))
        screen.blit(algorithm_text, (400, 560))
        pygame.display.flip()
        clock.tick(FPS_LIMIT)
        #Going to add some stuff heres
    
    pygame.quit()

if __name__ == "__main__":
    main()