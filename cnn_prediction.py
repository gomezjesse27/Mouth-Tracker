import cv2
import pygame
import numpy as np
from tensorflow.keras.models import load_model

cnn_model = load_model('cnn_model.h5')
downsized_dimension = 24  # This should match the input size used during training.....

def predict_target(frame):
    print("Predicting!")
    # Normalize and reshape the frame for CNN
    normalized_data_frame = np.round(frame / 255.0, 3).reshape(1, downsized_dimension, downsized_dimension, 1)
    prediction = cnn_model.predict(normalized_data_frame)
    print(f'Predicted target: {prediction[0][0]}')
    return prediction[0][0]

def main():
    predicted_target_value = 0

    # Create a VideoCapture object to capture the webcam feed
    cap = cv2.VideoCapture(0)

    # initialize Pygame and the display window
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("The CNN Predictor")

    # font object for rendering text
    font = pygame.font.Font(None, 36)

    clock = pygame.time.Clock()
    running = True
    while running:
        # read current frame from webcam
        ret, frame = cap.read()

        # resize the frame to training size
        resized_frame = cv2.resize(frame, (downsized_dimension, downsized_dimension))
        datapoint_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

        # grayscale frame to RGB again for Pygame
        rgb_frame = cv2.cvtColor(datapoint_frame, cv2.COLOR_GRAY2RGB)
        pygame_frame = pygame.image.frombuffer(rgb_frame.tostring(), rgb_frame.shape[1::-1], "RGB")
        pygame_frame = pygame.transform.scale(pygame_frame, (300, 300))

        screen.fill((50, 10, 0))
        # Ddraw frame to Pygame window
        screen.blit(pygame_frame, (0, 0))

        # draw to pygame
        target_text = font.render(f'Prediction: {predicted_target_value:.2f}', True, (255, 255, 255))
        screen.blit(target_text, (350, 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running = False

        predicted_target_value = predict_target(datapoint_frame)

        clock.tick(30)

    # Close
    print("Closing")
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()
