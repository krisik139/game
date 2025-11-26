import pygame
import sys
import json

pygame.init()

# --- Налаштування головоломки ---
WIDTH, HEIGHT = 640, 640
TILE_SIZE = 64
ROWS, COLS = 10, 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Puzzle 1 - Walk Blue Field")

# Кольори
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0,0,0)

clock = pygame.time.Clock()

# --- Генеруємо поле ---
# B = синій (прохідний), O = оранжевий (змінюється на зелений після дотику), R = червоний (непрохідний)
import random
field = []
for y in range(ROWS):
    row = []
    for x in range(COLS):
        r = random.random()
        if r < 0.1:
            row.append("R")
        elif r < 0.4:
            row.append("O")
        else:
            row.append("B")
    field.append(row)

# --- Персонаж ---
player_x, player_y = 0, 0

# --- Лічильник для завершення ---
total_orange = sum(row.count("O") for row in field)
touched_orange = 0

# --- Основний цикл ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            dx, dy = 0, 0
            if event.key == pygame.K_w: dy = -1
            elif event.key == pygame.K_s: dy = 1
            elif event.key == pygame.K_a: dx = -1
            elif event.key == pygame.K_d: dx = 1

            new_x = player_x + dx
            new_y = player_y + dy
            if 0 <= new_x < COLS and 0 <= new_y < ROWS:
                tile = field[new_y][new_x]
                if tile == "B" or tile == "O":
                    player_x, player_y = new_x, new_y
                    if tile == "O":
                        field[player_y][player_x] = "G"  # Оранжевий стає зеленим
                elif tile == "G" or tile == "R":
                    # Дотику до зеленого або червоного - гра одразу закінчується
                    running = False

    # --- Малювання ---
    screen.fill(BLACK)
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if field[y][x] == "B":
                pygame.draw.rect(screen, BLUE, rect)
            elif field[y][x] == "O":
                pygame.draw.rect(screen, ORANGE, rect)
            elif field[y][x] == "G":
                pygame.draw.rect(screen, GREEN, rect)
            elif field[y][x] == "R":
                pygame.draw.rect(screen, RED, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

    # Малюємо персонажа
    rect = pygame.Rect(player_x*TILE_SIZE, player_y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, (255,255,255), rect)

    pygame.display.flip()
    clock.tick(60)

    # --- Перевірка завершення ---
    if touched_orange == total_orange:
        running = False

# --- Зберігаємо результат у JSON ---
score = {"Puzzle1": touched_orange}
with open("score.json", "w") as f:
    json.dump(score, f)

# --- Повертаємося в main.py ---
pygame.quit()
