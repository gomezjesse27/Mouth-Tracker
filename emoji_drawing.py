import math
import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
LINE_COLOR = (255, 255, 255)
LINE_WIDTH = 2

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Your points
points_basis = [(0.219, -0.543), (0.241, -0.602), (0.174, -0.607), (0.106, -0.61), (-0.0, -0.612), (-0.106, -0.61), (-0.174, -0.607), (-0.241, -0.602), (-0.219, -0.543), (-0.119, -0.532), (-0.0, -0.532), (0.119, -0.532), (0.195, 0.981), (0.556, 0.831), (0.831, 0.556), (0.981, 0.195), (0.981, -0.195), (0.831, -0.556), (0.556, -0.831), (0.195, -0.981), (-0.195, -0.981), (-0.556, -0.831), (-0.831, -0.556), (-0.981, -0.195), (-0.981, 0.195), (-0.831, 0.556), (-0.556, 0.831), (-0.195, 0.981), (-0.144, 0.607), (-0.144, 0.009), (-0.262, 0.009), (-0.262, 0.607), (0.144, 0.607), (0.262, 0.607), (0.262, 0.009), (0.144, 0.009)]
relative_points_open_mouth = [(0.03, 0.312), (0.005, 0.101), (0.037, -0.31), (0.015, -0.383), (0.0, -0.422), (-0.015, -0.383), (-0.037, -0.31), (-0.005, 0.101), (-0.03, 0.312), (0.0, 0.516), (0.0, 0.516), (0.0, 0.516), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, -0.221), (0.0, -0.221), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.082), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.082)]
relative_points_smile = [(0.546, 0.373), (0.557, 0.404), (0.242, 0.065), (0.033, -0.041), (0.0, -0.047), (-0.033, -0.041), (-0.242, 0.065), (-0.557, 0.404), (-0.546, 0.373), (-0.221, 0.039), (0.0, -0.059), (0.221, 0.039), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.076, 0.024), (0.119, 0.017), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (-0.119, 0.017), (-0.076, 0.024), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (-0.009, 0.032), (-0.021, 0.038), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.021, 0.038), (0.009, 0.032)]
points = points_basis
mouth_begin_index = 0
mouth_end_index = 11
head_begin_index = 12
head_end_index = 27
eye_l_begin_index = 28
eye_l_end_index = 31
eye_r_begin_index = 32
eye_r_end_index = 35

DRAW_WIDTH, DRAW_HEIGHT = 256, 256

def draw_emoji(x_pos, y_pos, size, morph_values):
    smile_amount = morph_values[0]
    open_mouth_amount = morph_values[1]
    # Transform the points
    transformed_points = []
    for i in range(len(points)):
        x = points[i][0] + relative_points_open_mouth[i][0] * open_mouth_amount + relative_points_smile[i][0] * smile_amount
        y = points[i][1] + relative_points_open_mouth[i][1] * open_mouth_amount + relative_points_smile[i][1] * smile_amount
        transformed_points.append((x, y))
    scaled_points = [(x * size / 2 + size / 2 + x_pos, -y * size / 2 + size / 2 + y_pos) for x, y in transformed_points]
    mouth_points = scaled_points[mouth_begin_index:mouth_end_index+1]
    head_points = scaled_points[head_begin_index:head_end_index+1]
    eye_l_points = scaled_points[eye_l_begin_index:eye_l_end_index+1]
    eye_r_points = scaled_points[eye_r_begin_index:eye_r_end_index+1]
    
    # Draw the mouth and head
    if len(mouth_points) > 1:
        pygame.draw.polygon(screen, LINE_COLOR, mouth_points, LINE_WIDTH)
    if len(head_points) > 1:
        pygame.draw.polygon(screen, LINE_COLOR, head_points, LINE_WIDTH)
    if len(eye_l_points) > 1:
        pygame.draw.polygon(screen, LINE_COLOR, eye_l_points, LINE_WIDTH)
    if len(eye_r_points) > 1:
        pygame.draw.polygon(screen, LINE_COLOR, eye_r_points, LINE_WIDTH)

def main():
    # Game loop
    font = pygame.font.Font(None, 36)
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background
        screen.fill(BACKGROUND_COLOR)

        mouth_open = (math.sin(pygame.time.get_ticks() * 0.002) + 1) / 2
        smile = (math.cos(pygame.time.get_ticks() * 0.002) + 1) / 2
        draw_emoji(200, 200, 256, [smile, mouth_open])

        pygame.draw.rect(screen, (200, 0, 255), (350, 10, int(200 * smile), 30))
        target_text = font.render(f'Smiling: {round(smile, 3)}', True, (255, 255, 255))
        screen.blit(target_text, (350, 10))
        pygame.draw.rect(screen, (200, 0, 255), (350, 30, int(200 * mouth_open), 30))        
        target_text = font.render(f'MouthOpen: {round(mouth_open, 3)}', True, (255, 255, 255))
        screen.blit(target_text, (350, 30))

        # Flip the display
        pygame.display.flip()

        clock.tick(30)

    pygame.quit()
    sys.exit()