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
numAlgos = Algorithms.ALL

def prediction_all_init():
    global pca_model, lr_model, cnn_model, ann_model, predicted_target_values, done, ann_nopca_model, numAlgos
    done = False
    numAlgos = Algorithms.ALL
    predicted_target_values = [[0 for _ in range(TARGET_COUNT)] for _ in range(numAlgos)]
    pca_model = joblib.load('pca_model.pkl')
    lr_model = joblib.load('lr_model.pkl')
    cnn_model = load_model('cnn_model.h5')
    ann_model = load_model('ann_model.h5')
    ann_nopca_model = load_model('ann_nopca_model.h5')

def predict_target(frame):
    normalized_data_frame = frame / 255.0
    datapoint = normalized_data_frame.flatten()
    predictions = [[0 for _ in range(TARGET_COUNT)] for _ in range(numAlgos)]
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        transformed_datapoint = pca_model.transform([datapoint])
        predictions[Algorithms.LINEAR_REGRESSION] = lr_model.predict(transformed_datapoint)[0]
    
        reshaped_datapoint = datapoint.reshape(1, RESOLUTION, RESOLUTION, 1)  # Add batch dimension
        predictions[Algorithms.CNN] = cnn_model.predict(reshaped_datapoint)[0]  # Predict
    
        transformed_datapoint = pca_model.transform([datapoint])
        predictions[Algorithms.ANN] = ann_model.predict(transformed_datapoint)[0]

        reshaped_datapoint = datapoint = datapoint.reshape(1, -1)
        predictions[Algorithms.ANN_NOPCA] = ann_nopca_model.predict(reshaped_datapoint)[0]
    return predictions



def get_average_predictions(predictions):
    # Calculate the average prediction across all models
    num_models = len(predictions)
    num_targets = len(predictions[0])
    average_prediction = [sum(predictions[j][i] for j in range(num_models)) / num_models for i in range(num_targets)]
    return average_prediction




def prediction_all_update(screen, events, cap):
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

    
    average_prediction = get_average_predictions(predicted_target_values)

    #### DRAW ########################################################
    screen.fill((50, 10, 0))
    # Draw the frame to the Pygame window
    screen.blit(pygame_frame, (0, 0))

    # Adjust loop to avoid indexing errors
    # num_values = len(predicted_target_values)
    # for i in range(num_values):  # Only loop through the actual number of predictions
    #     pygame.draw.rect(screen, (200, 0, 255), (350, 10 + 20 * i, int(200 * predicted_target_values[i]), 30))
    #     target_text = font.render(f'{TARGET_NAMES[i]}: {round(predicted_target_values[i], 3)}', True, (255, 255, 255))
    #     screen.blit(target_text, (350, 10 + 20 * i))
    
    for i in range(numAlgos):
        draw_emoji(360, i * 150, 128, predicted_target_values[i])
        # Write what algo it is
        algo_text = font.render(f'{algo_to_string(i)}', True, (255, 255, 255))
        screen.blit(algo_text, (500, i * 150 + 40))

    # Draw the average prediction
    draw_emoji(80, 400, 128, average_prediction)
    average_text = font.render('Average Prediction', True, (255, 255, 255))
    screen.blit(average_text, (50, 550))

    return done