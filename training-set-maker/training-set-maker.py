import cv2
import pygame
import numpy as np
import random
import csv

training_set_name = 'training_set.csv'
downsized_dimension = 24 # Make this as small as possible for better training

def save_datapoint(frame, target_values):
    # Save a datapoint to the CSV file
    normalized_training_frame = np.round(frame / 255.0, 3)
    datapoint = list(normalized_training_frame.flatten())
    for value in target_values:
        datapoint.append(value)
    with open(training_set_name, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(datapoint)

def main():
    target0_value = 0
    target1_value = 0
    calibrating = False

    # Create a VideoCapture object to capture the webcam feed
    cap = cv2.VideoCapture(0)

    # Initialize Pygame and the display window
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Webcam Feed")

    # Create a font object for rendering text
    font = pygame.font.Font(None, 36)

    # Create a header for the CSV file
    header = [f'pix{i}' for i in range(downsized_dimension * downsized_dimension)] + ['target0'] + ['target1']
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
        target0_text = font.render(f'Target0: {target0_value}', True, (255, 255, 255))
        target1_text = font.render(f'Target1: {target1_value}', True, (255, 255, 255))
        calibrating_text = font.render(f'Calibrating: {calibrating}', True, (255, 255, 255))
        screen.blit(target0_text, (350, 10))
        screen.blit(target1_text, (350, 30))
        screen.blit(calibrating_text, (350, 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n: # N for "Next". Quits it.
                    running = False
                elif event.key == pygame.K_BACKSPACE: # Backspace for "try again". Clears the training set.
                    with open(training_set_name, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(header)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                calibrating = True
            elif event.type == pygame.MOUSEBUTTONUP:
                calibrating = False
        
        # Your mouse controls the two target values. Hold click to save datapoints.
        screen_width, screen_height = pygame.display.get_surface().get_size()
        mouse_position = pygame.mouse.get_pos()
        normalized_mouse_position = (mouse_position[0] / screen_width, mouse_position[1] / screen_height)
        target0_value = normalized_mouse_position[0]
        target1_value = normalized_mouse_position[1]

        if calibrating:
            save_datapoint(training_frame, [target0_value, target1_value])
        
        clock.tick(30)

    # Close
    print("Closing")
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()