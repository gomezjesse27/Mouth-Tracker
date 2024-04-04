import cv2
import pygame
import numpy as np
import random
import csv

training_set_name = 'training_set.csv'
downsized_dimension = 24 # Make this as small as possible for better training

def save_datapoint(frame, target_value):
    # Save a datapoint to the CSV file
    normalized_training_frame = np.round(frame / 255.0, 3)
    datapoint = list(normalized_training_frame.flatten())
    datapoint.append(target_value)
    with open(training_set_name, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(datapoint)

def main():
    target_value = 0
    calibrating = False
    calibration_start_time = 0
    calibration_length_ms = 5000

    # Create a VideoCapture object to capture the webcam feed
    cap = cv2.VideoCapture(0)

    # Initialize Pygame and the display window
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Webcam Feed")

    # Create a font object for rendering text
    font = pygame.font.Font(None, 36)

    # Create a header for the CSV file
    header = [f'pix{i}' for i in range(downsized_dimension * downsized_dimension)] + ['target0']
    with open(training_set_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

    clock = pygame.time.Clock()
    running = True
    while running:
        # Read the current frame from the webcam
        ret, frame = cap.read()

        # Resize the frame to training size
        resized_frame = cv2.resize(frame, (downsized_dimension, downsized_dimension))
        training_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

        # Convert grayscale frame to RGB again for Pygame
        rgb_frame = cv2.cvtColor(training_frame, cv2.COLOR_GRAY2RGB)
        pygame_frame = pygame.image.frombuffer(rgb_frame.tostring(), rgb_frame.shape[1::-1], "RGB")
        pygame_frame = pygame.transform.scale(pygame_frame, (300, 300))

        screen.fill((0, 0, 30))
        # Draw the frame to the Pygame window
        screen.blit(pygame_frame, (0, 0))

        # Render the target value as text and draw it to the Pygame window
        target_text = font.render(f'Target: {target_value}', True, (255, 255, 255))
        screen.blit(target_text, (350, 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    calibrating = True
                    calibration_start_time = pygame.time.get_ticks()
        
        if calibrating and pygame.time.get_ticks() - calibration_start_time > calibration_length_ms:
            calibrating = False
        
        if calibrating:
            target_value = (pygame.time.get_ticks() - calibration_start_time) / calibration_length_ms
            save_datapoint(training_frame, target_value)
        
        clock.tick(30)

    # Close
    print("Closing")
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()