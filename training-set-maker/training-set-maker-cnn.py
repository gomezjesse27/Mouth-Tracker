import cv2
import pygame
import numpy as np
import csv

# Global resolution setting
downsized_dimension = 64  # Adjust resolution here as needed

training_set_name = 'training_set_cnn.csv'
collection_duration = 10  # Duration in seconds for each phase


#For training I found that saving a ton of datapoints at 0, .5, and 1 for both mouth_open and smiling was helpful. and of course a few in between.
def save_datapoint(frame, mouth_open, smiling):
    normalized_training_frame = np.round(frame / 255.0, 3)
    datapoint = normalized_training_frame.flatten().tolist()
    datapoint.extend([mouth_open, smiling])
    with open(training_set_name, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(datapoint)

def main():
    cap = cv2.VideoCapture(0)
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.Font(None, 36)
    instructions = "Use mouse Y for 'Mouth Open' and mouse X for 'Smiling'. Click to save data point."
    instructions_text = font.render(instructions, True, (255, 255, 0))
    header = ['pix_{}_{}'.format(i, j) for i in range(downsized_dimension) for j in range(downsized_dimension)] + ['mouth_open', 'smiling']
    with open(training_set_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

    running = True
    while running:
        ret, frame = cap.read()
        resized_frame = cv2.resize(frame, (downsized_dimension, downsized_dimension))
        training_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
        rgb_frame = cv2.cvtColor(training_frame, cv2.COLOR_GRAY2RGB)
        pygame_frame = pygame.image.frombuffer(rgb_frame.tostring(), rgb_frame.shape[1::-1], "RGB")
        screen.fill((0, 0, 30))
        screen.blit(pygame.transform.scale(pygame_frame, (300, 300)), (0, 0))
        screen.blit(instructions_text, (10, 560))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouth_open = mouse_y / 600
        smiling = mouse_x / 800
        label_text = font.render(f'Mouth Open: {mouth_open:.2f}, Smiling: {smiling:.2f}', True, (255, 255, 255))
        screen.blit(label_text, (10, 530))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                save_datapoint(training_frame, mouth_open, smiling)
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()
