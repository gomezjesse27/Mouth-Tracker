import cv2
import pygame
import numpy as np

downsized_dimension = 24 # Make this as small as possible for better training

def main():
    # Create a VideoCapture object to capture the webcam feed
    cap = cv2.VideoCapture(0)

    # Initialize Pygame and the display window
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Webcam Feed")

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
        #pygame_frame = pygame.transform.rotate(pygame_frame, -90)
        pygame_frame = pygame.transform.scale(pygame_frame, (300, 300))

        # Draw the frame to the Pygame window
        screen.blit(pygame_frame, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    # Close
    print("Closing")
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()