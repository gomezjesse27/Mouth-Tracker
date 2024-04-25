import cv2
import pygame
import numpy as np
from tensorflow.keras.models import load_model

downsized_dimension = 64  # Adjust resolution here as needed, I have been going with 64 for the CNN model

cnn_model = load_model('cnn_model.h5')

def predict_target(frame):
    normalized_data_frame = frame / 255.0
    normalized_data_frame = normalized_data_frame.reshape(1, downsized_dimension, downsized_dimension, 1)
    predictions = cnn_model.predict(normalized_data_frame)
    return predictions[0]

def main():
    cap = cv2.VideoCapture(0)
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("The CNN Predictor")
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    running = True
    while running:
        ret, frame = cap.read()
        if not ret:
            break
        resized_frame = cv2.resize(frame, (downsized_dimension, downsized_dimension))
        datapoint_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
        predicted_mouth_open, predicted_smiling = predict_target(datapoint_frame)
        prediction_mouth_open_text = f'Predicted Mouth Open: {predicted_mouth_open:.9f}'
        prediction_smiling_text = f'Predicted Smiling: {predicted_smiling:.9f}'
        rgb_frame = cv2.cvtColor(datapoint_frame, cv2.COLOR_GRAY2RGB)
        pygame_frame = pygame.image.frombuffer(rgb_frame.tobytes(), rgb_frame.shape[1::-1], "RGB")
        pygame_frame = pygame.transform.scale(pygame_frame, (300, 300))
        screen.fill((50, 10, 0))
        screen.blit(pygame_frame, (0, 0))
        mouth_open_text = font.render(prediction_mouth_open_text, True, (255, 255, 255))
        smiling_text = font.render(prediction_smiling_text, True, (255, 255, 255))
        screen.blit(mouth_open_text, (350, 10))
        screen.blit(smiling_text, (350, 50))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running = False
        clock.tick(30)
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()
