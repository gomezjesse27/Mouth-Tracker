import cv2
import pygame
import numpy as np
import joblib
import warnings 

pca_model = joblib.load('pca_model.pkl')
multioutput_linear_regression_model = joblib.load('multioutput_linear_regression_model.pkl')
downsized_dimension = 24 # Make this as small as possible for better training

def predict_target(frame):
    #print("Predicting!")
    # Save a datapoint to the CSV file
    normalized_data_frame = np.round(frame / 255.0, 3)
    datapoint = list(normalized_data_frame.flatten())
    with warnings.catch_warnings(): # TODO: actually solve the warning. it's about X not having feature names even though it was trained with feature names (pix0 ... pix783)
        warnings.filterwarnings("ignore")        
        predictions = multioutput_linear_regression_model.predict(pca_model.transform([datapoint]))[0] # idk why I have to put the [0] here but I do. then you can index predictions with [0] and [1] etc
    #print(f'Predicted target: {predictions[0]}, {predictions[1]}')
    return predictions

def main():
    predicted_target_values = [0, 0]
    predict = False

    # Create a VideoCapture object to capture the webcam feed
    cap = cv2.VideoCapture(0)

    # Initialize Pygame and the display window
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("The Predictor")

    # Create a font object for rendering text
    font = pygame.font.Font(None, 36)

    clock = pygame.time.Clock()
    running = True
    while running:
        # Read the current frame from the webcam
        ret, frame = cap.read()

        # Resize the frame to training size
        resized_frame = cv2.resize(frame, (downsized_dimension, downsized_dimension))
        datapoint_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

        # Convert grayscale frame to RGB again for Pygame
        rgb_frame = cv2.cvtColor(datapoint_frame, cv2.COLOR_GRAY2RGB)
        #pygame_frame = pygame.image.frombuffer(rgb_frame.tostring(), rgb_frame.shape[1::-1], "RGB")
        pygame_frame = pygame.image.frombuffer(rgb_frame.tobytes(), rgb_frame.shape[1::-1], "RGB")
        pygame_frame = pygame.transform.scale(pygame_frame, (300, 300))

        screen.fill((50, 10, 0))
        # Draw the frame to the Pygame window
        screen.blit(pygame_frame, (0, 0))

        # Render the target value as text and draw it to the Pygame window
        target_text = font.render(f'Prediction: {predicted_target_values[0]}', True, (255, 255, 255))
        screen.blit(target_text, (350, 10))
        target_text = font.render(f'Prediction: {predicted_target_values[1]}', True, (255, 255, 255))
        screen.blit(target_text, (350, 30))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("how are you")
        predicted_target_values = predict_target(datapoint_frame)

        clock.tick(30)

    # Close
    print("Closing")
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()