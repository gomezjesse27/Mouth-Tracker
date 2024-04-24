import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
LINE_COLOR = (255, 255, 255)
LINE_WIDTH = 1

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Your points
points = [(0.219, -0.543), (0.241, -0.602), (0.174, -0.607), (0.106, -0.61), (-0.0, -0.612), (-0.106, -0.61), (-0.174, -0.607), (-0.241, -0.602), (-0.219, -0.543), (-0.119, -0.532), (-0.0, -0.532), (0.119, -0.532), (0.195, 0.981), (0.556, 0.831), (0.831, 0.556), (0.981, 0.195), (0.981, -0.195), (0.831, -0.556), (0.556, -0.831), (0.195, -0.981), (-0.195, -0.981), (-0.556, -0.831), (-0.831, -0.556), (-0.981, -0.195), (-0.981, 0.195), (-0.831, 0.556), (-0.556, 0.831), (-0.195, 0.981), (-0.144, 0.607), (-0.144, 0.009), (-0.262, 0.009), (-0.262, 0.607), (0.144, 0.607), (0.262, 0.607), (0.262, 0.009), (0.144, 0.009)]
mouth_begin_index = 0
mouth_end_index = 11
head_begin_index = 12
head_end_index = 27
eye_l_begin_index = 28
eye_l_end_index = 31
eye_r_begin_index = 32
eye_r_end_index = 35

# Scale and translate points to fit the screen
DRAW_WIDTH, DRAW_HEIGHT = 256, 256
scaled_points = [(x * DRAW_WIDTH / 2 + DRAW_WIDTH / 2, -y * DRAW_HEIGHT / 2 + DRAW_HEIGHT / 2) for x, y in points]
mouth_points = scaled_points[mouth_begin_index:mouth_end_index+1]
head_points = scaled_points[head_begin_index:head_end_index+1]
eye_l_points = scaled_points[eye_l_begin_index:eye_l_end_index+1]
eye_r_points = scaled_points[eye_r_begin_index:eye_r_end_index+1]

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background
    screen.fill(BACKGROUND_COLOR)

    # Draw the mouth and head
    if len(mouth_points) > 1:
        pygame.draw.polygon(screen, LINE_COLOR, mouth_points, LINE_WIDTH)
    if len(head_points) > 1:
        pygame.draw.polygon(screen, LINE_COLOR, head_points, LINE_WIDTH)
    if len(eye_l_points) > 1:
        pygame.draw.polygon(screen, LINE_COLOR, eye_l_points, LINE_WIDTH)
    if len(eye_r_points) > 1:
        pygame.draw.polygon(screen, LINE_COLOR, eye_r_points, LINE_WIDTH)

    # Flip the display
    pygame.display.flip()

    clock.tick(15)

pygame.quit()
sys.exit()