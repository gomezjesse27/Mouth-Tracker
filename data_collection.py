import sys
import cv2
import pygame
import numpy as np
import random
import csv
from config import *
from emoji_drawing import draw_emoji

training_set_name = 'training_set.csv'

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
    target_values = [0 for _ in range(TARGET_COUNT)]
    calibrating = False

    # Create a VideoCapture object to capture the webcam feed
    cap = cv2.VideoCapture(WEBCAM_ID)

    # Initialize Pygame and the display window
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Data collector")

    # Create a font object for rendering text
    font = pygame.font.Font(None, 36)

    # Create a header for the CSV file
    header = [f'pix{i}' for i in range(RESOLUTION * RESOLUTION)] + TARGET_NAMES[:TARGET_COUNT]
    with open(training_set_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

    clock = pygame.time.Clock()
    running = True
    escape = False
    while running:
        # Read the current frame from the webcam
        ret, frame = cap.read()

        # Resize the frame to training size
        resized_frame = cv2.resize(frame, (RESOLUTION, RESOLUTION))
        training_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

        # Convert grayscale frame to RGB again for Pygame
        rgb_frame = cv2.cvtColor(training_frame, cv2.COLOR_GRAY2RGB)
        pygame_frame = pygame.image.frombuffer(rgb_frame.tobytes(), rgb_frame.shape[1::-1], "RGB")
        pygame_frame = pygame.transform.scale(pygame_frame, (300, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                escape = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n: # N for "Next". Quits it.
                    running = False
                elif event.key == pygame.K_BACKSPACE: # Backspace for "try again". Clears the training set.
                    with open(training_set_name, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(header)
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    escape = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                calibrating = True
            elif event.type == pygame.MOUSEBUTTONUP:
                calibrating = False
        
        # Your mouse controls the two target values. Hold click to save datapoints.
        screen_width, screen_height = pygame.display.get_surface().get_size()
        mouse_position = pygame.mouse.get_pos()
        normalized_mouse_position = (mouse_position[0] / screen_width, mouse_position[1] / screen_height)
        target_values = normalized_mouse_position

        if calibrating:
            save_datapoint(training_frame, target_values)

        #### DRAW ########################################################
        screen.fill((0, 0, 30))
        # Draw the frame to the Pygame window
        screen.blit(pygame_frame, (0, 0))

        # Render the target value as text and draw it to the Pygame window
        for i in range(TARGET_COUNT):
            pygame.draw.rect(screen, (200, 0, 255), (350, 10 + 20 * i, int(200 * target_values[i]), 30))
            target_text = font.render(f'{TARGET_NAMES[i]}: {round(target_values[i], 3)}', True, (255, 255, 255))
            screen.blit(target_text, (350, 10 + 20 * i))
        calibrating_text = font.render(f'Calibrating: {calibrating}', True, (255, 255, 255))
        screen.blit(calibrating_text, (350, 50))
        # print instructions
        instructions = font.render("Press N to go to next script, Backspace to clear, ESC to abort", True, (255, 255, 255))
        screen.blit(instructions, (0, 500))
        
        draw_emoji(400, 200, 256, target_values)

        pygame.display.flip()

        clock.tick(30)

    # Close
    print("Closing")
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()
    if escape:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()