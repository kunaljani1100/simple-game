import pygame
import sys
import math
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))

circle_position = (1280 / 2, 720 / 2)

font = pygame.font.Font(None, 30)

score = 0

def check_circle_position() -> bool:
    mouse_pos = pygame.mouse.get_pos()
    if math.sqrt((mouse_pos[0] - circle_position[0]) ** 2 + (mouse_pos[0] - circle_position[0]) ** 2 <= 50):
        return True
    return False

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            if check_circle_position():
                score += 1
                circle_position = (random.randint(0, 1280), random.randint(0, 720))

    score_surface = font.render(f'Score: {score}', True, 'black')
    screen.fill('lightblue')
    pygame.draw.circle(screen, 'red', circle_position, 100)
    screen.blit(score_surface, (50, 50))
    pygame.display.update()