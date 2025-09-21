import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((1280, 720))
x = 50
y = 50
rectangle = (x, y, 50, 50)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    print(keys)
    if keys[pygame.K_LEFT]:
        if x >= 0:
            x -= 1
    elif keys[pygame.K_RIGHT]:
        if x <= 1280 - 50:
            x += 1
    elif keys[pygame.K_UP]:
        if y >= 0:
            y -= 1
    elif keys[pygame.K_DOWN]:
        if y <= 720 - 50:
            y += 1

    rectangle = (x, y, 50, 50)
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, 'red', rectangle)
    pygame.display.flip()