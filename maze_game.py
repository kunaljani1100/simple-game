import pygame
import sys

# Shared layout — imported by maze_bot without opening a window.
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_SIZE = 50
PLAYER_START = (50, 50)
GOAL_SIZE = 50
GOAL_POS = (SCREEN_WIDTH - GOAL_SIZE - 50, SCREEN_HEIGHT - GOAL_SIZE - 50)
OBSTACLES = [
    (100, 100, 100, 100),
    (600, 400, 150, 150),
    (900, 50, 120, 120),
]
MOVE_SPEED = 5


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Game")

    player_rect = pygame.Rect(*PLAYER_START, PLAYER_SIZE, PLAYER_SIZE)
    goal_rect = pygame.Rect(*GOAL_POS, GOAL_SIZE, GOAL_SIZE)
    obstacles = [pygame.Rect(*obs) for obs in OBSTACLES]

    font = pygame.font.SysFont(None, 72)
    clock = pygame.time.Clock()
    won = False
    win_time = 0

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not won:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if player_rect.x > 0:
                    player_rect.x -= MOVE_SPEED
                    if any(player_rect.colliderect(o) for o in obstacles):
                        player_rect.x += MOVE_SPEED
            if keys[pygame.K_RIGHT]:
                if player_rect.x < SCREEN_WIDTH - PLAYER_SIZE:
                    player_rect.x += MOVE_SPEED
                    if any(player_rect.colliderect(o) for o in obstacles):
                        player_rect.x -= MOVE_SPEED
            if keys[pygame.K_UP]:
                if player_rect.y > 0:
                    player_rect.y -= MOVE_SPEED
                    if any(player_rect.colliderect(o) for o in obstacles):
                        player_rect.y += MOVE_SPEED
            if keys[pygame.K_DOWN]:
                if player_rect.y < SCREEN_HEIGHT - PLAYER_SIZE:
                    player_rect.y += MOVE_SPEED
                    if any(player_rect.colliderect(o) for o in obstacles):
                        player_rect.y -= MOVE_SPEED

            if player_rect.colliderect(goal_rect):
                won = True
                win_time = pygame.time.get_ticks()

        screen.fill((30, 30, 30))
        pygame.draw.rect(screen, (0, 200, 0), goal_rect)
        pygame.draw.rect(screen, (200, 0, 0), player_rect)
        for obstacle in obstacles:
            pygame.draw.rect(screen, (255, 165, 0), obstacle)

        if won:
            text = font.render("You Win!", True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
            if pygame.time.get_ticks() - win_time > 2000:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    run_game()
