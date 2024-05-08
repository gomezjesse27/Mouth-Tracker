import math
import pygame
import sys
from config import *

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
points_basis = [(0.219, -0.547), (0.241, -0.55), (0.174, -0.55), (0.106, -0.55), (0.0, -0.55), (-0.106, -0.55), (-0.174, -0.55), (-0.241, -0.55), (-0.219, -0.547), (-0.119, -0.546), (0.0, -0.546), (0.119, -0.546), (0.195, 0.981), (0.556, 0.831), (0.831, 0.556), (0.981, 0.195), (0.981, -0.195), (0.831, -0.556), (0.556, -0.831), (0.195, -0.981), (-0.195, -0.981), (-0.556, -0.831), (-0.831, -0.556), (-0.981, -0.195), (-0.981, 0.195), (-0.831, 0.556), (-0.556, 0.831), (-0.195, 0.981), (-0.144, 0.607), (-0.144, 0.009), (-0.262, 0.009), (-0.262, 0.607), (0.144, 0.607), (0.262, 0.607), (0.262, 0.009), (0.144, 0.009)]
relative_points_open_mouth = [(0.086, 0.395), (0.061, 0.184), (0.093, -0.39), (0.071, -0.464), (0.0, -0.494), (-0.071, -0.464), (-0.093, -0.39), (-0.061, 0.184), (-0.086, 0.395), (-0.098, 0.636), (0.0, 0.683), (0.098, 0.636), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.028, -0.092), (0.08, -0.245), (-0.08, -0.245), (-0.028, -0.092), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (-0.03, 0.166), (-0.029, 0.227), (-0.029, 0.215), (-0.03, 0.166), (0.03, 0.166), (0.03, 0.166), (0.029, 0.215), (0.029, 0.227)]
relative_points_smile = [(0.546, 0.373), (0.557, 0.404), (0.242, 0.065), (0.033, -0.041), (-0.0, -0.047), (-0.033, -0.041), (-0.242, 0.065), (-0.557, 0.404), (-0.546, 0.373), (-0.221, 0.038), (-0.0, -0.059), (0.221, 0.038), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.076, 0.024), (0.119, 0.017), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (-0.119, 0.017), (-0.076, 0.024), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.04), (-0.009, 0.032), (-0.021, 0.038), (0.0, 0.0), (0.0, 0.04), (0.0, 0.0), (0.021, 0.038), (0.009, 0.032)]
relative_points_puff = [(0.218, 0.26), (0.213, 0.095), (0.22, 0.177), (0.021, 0.167), (0.0, 0.165), (-0.021, 0.167), (-0.22, 0.177), (-0.213, 0.095), (-0.218, 0.26), (-0.262, 0.165), (0.0, 0.134), (0.262, 0.165), (0.0, 0.0), (0.081, -0.063), (-0.003, -0.234), (0.261, -0.173), (0.269, -0.216), (0.114, -0.247), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (-0.114, -0.247), (-0.269, -0.216), (-0.261, -0.173), (0.003, -0.234), (-0.081, -0.063), (0.0, 0.0), (0.0, 0.0), (0.0, 0.085), (0.0, 0.085), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.085), (0.0, 0.085)]
relative_points_frown = [(0.278, -0.187), (0.276, -0.201), (0.215, 0.034), (0.098, 0.104), (0.0, 0.14), (-0.098, 0.104), (-0.215, 0.034), (-0.276, -0.201), (-0.278, -0.187), (-0.248, 0.039), (0.0, 0.131), (0.248, 0.039), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (-0.038, -0.017), (0.0, -0.131), (0.021, -0.09), (0.0, 0.0), (0.0, 0.0), (-0.021, -0.09), (0.0, -0.131), (0.038, -0.017), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (-0.024, -0.206), (-0.041, -0.018), (-0.042, -0.018), (-0.024, -0.206), (0.024, -0.206), (0.024, -0.206), (0.042, -0.018), (0.041, -0.018)]
relative_points_left = [(-0.341, -0.055), (-0.342, -0.061), (-0.34, -0.044), (-0.338, -0.027), (-0.334, 0.0), (-0.331, 0.027), (-0.329, 0.044), (-0.326, 0.061), (-0.327, 0.056), (-0.33, 0.03), (-0.333, 0.0), (-0.337, -0.031), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (-0.026, 0.0), (-0.048, -0.011), (-0.047, -0.012), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0)]
relative_points_right = [(0.346, 0.065), (0.346, 0.071), (0.348, 0.053), (0.351, 0.036), (0.354, 0.01), (0.357, -0.017), (0.36, -0.034), (0.362, -0.05), (0.36, -0.045), (0.357, -0.02), (0.353, 0.009), (0.35, 0.039), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.017, 0.0), (0.032, 0.008), (0.044, -0.025), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0)]
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
    # Make morph_values have 4 values. If it has less, fill the rest with 0
    morph_values = list(morph_values) + [0] * (len(TARGET_NAMES) - len(morph_values))
    smile_amount = morph_values[0]
    open_mouth_amount = morph_values[1]
    puff_amount = morph_values[2]
    frown_amount = morph_values[3]
    left_amount = morph_values[4]
    right_amount = morph_values[5]
    # Transform the points
    transformed_points = []
    for i in range(len(points)):
        x = points[i][0] + relative_points_open_mouth[i][0] * open_mouth_amount + relative_points_smile[i][0] * smile_amount + relative_points_puff[i][0] * puff_amount + relative_points_frown[i][0] * frown_amount + relative_points_left[i][0] * left_amount + relative_points_right[i][0] * right_amount
        y = points[i][1] + relative_points_open_mouth[i][1] * open_mouth_amount + relative_points_smile[i][1] * smile_amount + relative_points_puff[i][1] * puff_amount + relative_points_frown[i][1] * frown_amount + relative_points_left[i][1] * left_amount + relative_points_right[i][1] * right_amount
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