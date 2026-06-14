import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((1280, 720))
# original player position
x = 50
y = 50
player_size = 50
player_rect = pygame.Rect(x, y, player_size, player_size)

# final destination (goal)
goal_size = 50
goal_x = 1280 - goal_size - 50  # offset from right edge
goal_y = 720 - goal_size - 50   # offset from bottom edge
goal_rect = pygame.Rect(goal_x, goal_y, goal_size, goal_size)

font = pygame.font.SysFont(None, 72)
clock = pygame.time.Clock()
won = False

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not won:
        keys = pygame.key.get_pressed()
        # simple movement with bounds checking
        if keys[pygame.K_LEFT]:
            if player_rect.x > 0:
                player_rect.x -= 5
        if keys[pygame.K_RIGHT]:
            if player_rect.x < 1280 - player_size:
                player_rect.x += 5
        if keys[pygame.K_UP]:
            if player_rect.y > 0:
                player_rect.y -= 5
        if keys[pygame.K_DOWN]:
            if player_rect.y < 720 - player_size:
                player_rect.y += 5

        # check if player reached the goal
        if player_rect.colliderect(goal_rect):
            won = True
            win_time = pygame.time.get_ticks()

    # draw
    screen.fill((30, 30, 30))
    # draw goal in green
    pygame.draw.rect(screen, (0, 200, 0), goal_rect)
    # draw player in red
    pygame.draw.rect(screen, (200, 0, 0), player_rect)

    if won:
        text = font.render("You Win!", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=(640, 360)))
        # exit after 2 seconds so the player can see the message
        if pygame.time.get_ticks() - win_time > 2000:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(60)
