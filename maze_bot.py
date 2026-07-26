"""
Standalone bot that opens the maze, finds start/goal, pathfinds around
obstacles, and drives the red square to the green goal.
"""

from __future__ import annotations

import heapq
import sys
from typing import Iterable, List, Optional, Tuple

import pygame

from maze_game import (
    GOAL_POS,
    GOAL_SIZE,
    MOVE_SPEED,
    OBSTACLES,
    PLAYER_SIZE,
    PLAYER_START,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)

Pos = Tuple[int, int]
RectTuple = Tuple[int, int, int, int]


def collides(pos: Pos, obstacles: Iterable[RectTuple]) -> bool:
    px, py = pos
    player = pygame.Rect(px, py, PLAYER_SIZE, PLAYER_SIZE)
    return any(player.colliderect(pygame.Rect(*obs)) for obs in obstacles)


def in_bounds(pos: Pos) -> bool:
    x, y = pos
    return 0 <= x <= SCREEN_WIDTH - PLAYER_SIZE and 0 <= y <= SCREEN_HEIGHT - PLAYER_SIZE


def reaches_goal(pos: Pos) -> bool:
    player = pygame.Rect(*pos, PLAYER_SIZE, PLAYER_SIZE)
    goal = pygame.Rect(*GOAL_POS, GOAL_SIZE, GOAL_SIZE)
    return player.colliderect(goal)


def neighbors(pos: Pos) -> List[Pos]:
    x, y = pos
    return [
        (x - MOVE_SPEED, y),
        (x + MOVE_SPEED, y),
        (x, y - MOVE_SPEED),
        (x, y + MOVE_SPEED),
    ]


def heuristic(pos: Pos) -> float:
    gx, gy = GOAL_POS
    # Aim for the top-left of the goal; collision accepts any overlapping pose.
    return abs(pos[0] - gx) + abs(pos[1] - gy)


def find_path(start: Pos, obstacles: List[RectTuple]) -> Optional[List[Pos]]:
    """A* over MOVE_SPEED steps; returns list of positions including start."""
    if collides(start, obstacles):
        return None

    open_heap: List[Tuple[float, int, Pos]] = []
    counter = 0
    heapq.heappush(open_heap, (heuristic(start), counter, start))

    came_from: dict[Pos, Optional[Pos]] = {start: None}
    g_score: dict[Pos, float] = {start: 0.0}

    while open_heap:
        _, _, current = heapq.heappop(open_heap)

        if reaches_goal(current):
            path: List[Pos] = []
            node: Optional[Pos] = current
            while node is not None:
                path.append(node)
                node = came_from[node]
            path.reverse()
            return path

        for nxt in neighbors(current):
            if not in_bounds(nxt) or collides(nxt, obstacles):
                continue
            tentative = g_score[current] + MOVE_SPEED
            if tentative >= g_score.get(nxt, float("inf")):
                continue
            came_from[nxt] = current
            g_score[nxt] = tentative
            counter += 1
            heapq.heappush(open_heap, (tentative + heuristic(nxt), counter, nxt))

    return None


def run_bot() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Bot")

    start = PLAYER_START
    goal = GOAL_POS
    obstacles = list(OBSTACLES)

    print(f"Start (red square): {start}")
    print(f"Goal  (green square): {goal}")
    print(f"Obstacles: {obstacles}")

    path = find_path(start, obstacles)
    if path is None:
        print("No path found around obstacles.", file=sys.stderr)
        pygame.quit()
        sys.exit(1)

    print(f"Path length: {len(path)} steps")

    player_rect = pygame.Rect(*start, PLAYER_SIZE, PLAYER_SIZE)
    goal_rect = pygame.Rect(*goal, GOAL_SIZE, GOAL_SIZE)
    obstacle_rects = [pygame.Rect(*obs) for obs in obstacles]

    font = pygame.font.SysFont(None, 72)
    small = pygame.font.SysFont(None, 28)
    clock = pygame.time.Clock()

    path_index = 0
    won = False
    win_time = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not won and path_index < len(path):
            player_rect.topleft = path[path_index]
            path_index += 1
            if player_rect.colliderect(goal_rect):
                won = True
                win_time = pygame.time.get_ticks()
                print("Reached goal.")

        screen.fill((30, 30, 30))
        # Draw remaining path ahead of the player.
        for px, py in path[path_index:]:
            pygame.draw.rect(
                screen,
                (60, 60, 90),
                pygame.Rect(px + PLAYER_SIZE // 2 - 2, py + PLAYER_SIZE // 2 - 2, 4, 4),
            )
        pygame.draw.rect(screen, (0, 200, 0), goal_rect)
        for obstacle in obstacle_rects:
            pygame.draw.rect(screen, (255, 165, 0), obstacle)
        pygame.draw.rect(screen, (200, 0, 0), player_rect)

        status = small.render(
            f"Bot moving | step {min(path_index, len(path))}/{len(path)}",
            True,
            (200, 200, 200),
        )
        screen.blit(status, (16, 16))

        if won:
            text = font.render("You Win!", True, (255, 255, 255))
            screen.blit(
                text,
                text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)),
            )
            if pygame.time.get_ticks() - win_time > 2000:
                pygame.quit()
                sys.exit(0)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    run_bot()
