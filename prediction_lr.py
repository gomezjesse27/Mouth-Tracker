import cv2
import pygame
import numpy as np
import joblib
import warnings 
from config import *
from emoji_drawing import draw_emoji

pca_model = joblib.load('pca_model.pkl')
lr_model = joblib.load('lr_model.pkl') # Multi output linear regression

def predict_target(frame):
    #print("Predicting!")
    normalized_data_frame = np.round(frame / 255.0, 3)
    datapoint = list(normalized_data_frame.flatten())
    with warnings.catch_warnings(): # TODO: actually solve the warning. it's about X not having feature names even though it was trained with feature names (pix0 ... pix783)
        warnings.filterwarnings("ignore")        
        transformed_datapoint = pca_model.transform([datapoint])
        predictions = lr_model.predict(transformed_datapoint)[0] # idk why I have to put the [0] here but I do. then you can index predictions with [0] and [1] etc
    #print(f'Predicted target: {predictions[0]}, {predictions[1]}')
    return predictions

def main():
    predicted_target_values = [0 for _ in range(TARGET_COUNT)]

    # Create a VideoCapture object to capture the webcam feed
    cap = cv2.VideoCapture(WEBCAM_ID)

    # Initialize Pygame and the display window
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("The Predictor")

    # Create a font object for rendering text
    font = pygame.font.Font(None, 36)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
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

        # Render the target value as text and draw it to the Pygame window
        for i in range(TARGET_COUNT):
            pygame.draw.rect(screen, (200, 0, 255), (350, 10 + 20 * i, int(200 * predicted_target_values[i]), 30))
            target_text = font.render(f'{TARGET_NAMES[i]}: {round(predicted_target_values[i], 3)}', True, (255, 255, 255))
            screen.blit(target_text, (350, 10 + 20 * i))
        draw_emoji(500, 200, 256, predicted_target_values)

        pygame.display.flip()

        clock.tick(30)

    print("Closing")
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()