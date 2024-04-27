import cv2
import pygame
import numpy as np
import joblib
import warnings 
from config import *
from emoji_drawing import draw_emoji
from tensorflow.keras.models import load_model  # For cnn_model

pca_model = None
lr_model = None
cnn_model = None
ann_model = None
ann_nopca_model = None
predicted_target_values = []
done = False

def prediction_init():
    global pca_model, lr_model, cnn_model, ann_model, predicted_target_values, ann_nopca_model, done
    done = False
    predicted_target_values = [0 for _ in range(TARGET_COUNT)]
    if ALGORITHM == Algorithms.LINEAR_REGRESSION:
        pca_model = joblib.load('pca_model.pkl')
        lr_model = joblib.load('lr_model.pkl')
    elif ALGORITHM == Algorithms.CNN:
        cnn_model = load_model('cnn_model.h5')
    elif ALGORITHM == Algorithms.ANN:
        pca_model = joblib.load('pca_model.pkl')
        ann_model = load_model('ann_model.h5')
    elif ALGORITHM == Algorithms.ANN_NOPCA:
        ann_nopca_model = load_model('ann_nopca_model.h5')

def predict_target(frame):
    print("Predicting!")
    normalized_data_frame = frame / 255.0
    datapoint = normalized_data_frame.flatten()

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        if ALGORITHM == Algorithms.LINEAR_REGRESSION:
            transformed_datapoint = pca_model.transform([datapoint])
            predictions = lr_model.predict(transformed_datapoint)[0]
        elif ALGORITHM == Algorithms.CNN:
            reshaped_datapoint = datapoint.reshape(1, RESOLUTION, RESOLUTION, 1)  # Add batch dimension
            print(f"Input shape to CNN: {reshaped_datapoint.shape}")  # Debugging
            predictions = cnn_model.predict(reshaped_datapoint)[0]  # Predict
        elif ALGORITHM == Algorithms.ANN:
            transformed_datapoint = pca_model.transform([datapoint])
            predictions = ann_model.predict(transformed_datapoint)[0]
        elif ALGORITHM == Algorithms.ANN_NOPCA:
            reshaped_datapoint = datapoint = datapoint.reshape(1, -1)
            predictions = ann_nopca_model.predict(reshaped_datapoint)[0]
    print(f'Predicted target values: {predictions}')
    return predictions

def prediction_update(screen, events, cap):
    global done
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RETURN:
                done = True

    font = pygame.font.Font(None, 36)
    # Read the current frame from the webcam
    ret, frame = cap.read()

    # Resize the frame to training size
    resized_frame = cv2.resize(frame, (RESOLUTION, RESOLUTION))
    datapoint_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

    # Convert grayscale frame to RGB again for Pygame
    rgb_frame = cv2.cvtColor(datapoint_frame, cv2.COLOR_GRAY2RGB)
    pygame_frame = pygame.image.frombuffer(rgb_frame.tobytes(), rgb_frame.shape[1::-1], "RGB")
    pygame_frame = pygame.transform.scale(pygame_frame, (300, 300))

    predicted_target_values = predict_target(datapoint_frame)

    #### DRAW ########################################################
    screen.fill((50, 10, 0))
    # Draw the frame to the Pygame window
    screen.blit(pygame_frame, (0, 0))

    # Adjust loop to avoid indexing errors
    num_values = len(predicted_target_values)
    for i in range(num_values):  # Only loop through the actual number of predictions
        pygame.draw.rect(screen, (200, 0, 255), (350, 10 + 20 * i, int(200 * predicted_target_values[i]), 30))
        target_text = font.render(f'{TARGET_NAMES[i]}: {round(predicted_target_values[i], 3)}', True, (255, 255, 255))
        screen.blit(target_text, (350, 10 + 20 * i))
    draw_emoji(500, 200, 256, predicted_target_values)

    return done