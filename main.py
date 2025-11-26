import pygame
import sys
import random
import subprocess

pygame.init()

# --- Налаштування ---
WIDTH, HEIGHT = 512, 320
TILE_SIZE = 64
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tile Map + Dialog + Puzzle Demo")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
YELLOW = (200, 200, 0)
PURPLE = (180, 0, 180)

clock = pygame.time.Clock()

# --- Карта ---
tile_map = [
    ["1", "1", "1", "1", "1", "1", "1", "1"],
    ["1", "0", "0", "0", "0", "0", "T", "1"],  # T - телефон
    ["1", "0", "0", "0", "0", "0", "C", "1"],  # C - комп
    ["1", "0", "0", "0", "0", "0", "0", "1"],
    ["1", "1", "1", "1", "1", "1", "1", "1"],
]

# --- Персонаж ---
tile_x, tile_y = 1, 1
pixel_x = tile_x * TILE_SIZE
pixel_y = tile_y * TILE_SIZE
move_speed = 8
player_state = "standing"
move_dir = (0, 0)

# --- Діалоги ---
dialog_active = False
dialog_text = ""

# --- Головоломка ---
puzzles = ["Puzzle 1", "Puzzle 2", "Puzzle 3"]
current_puzzle = random.choice(puzzles)
talked_on_phone = False

# --- Основний цикл ---
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Standing: підказка та взаємодія
        if player_state == "standing" and not dialog_active:
            # Підказка активна, якщо тайл для взаємодії
            if tile_map[tile_y][tile_x] in ["C", "T"]:
                hint_active = True
            else:
                hint_active = False

            if event.type == pygame.KEYDOWN:
                dx, dy = 0, 0
                if event.key == pygame.K_w:
                    dx, dy = 0, -1
                elif event.key == pygame.K_s:
                    dx, dy = 0, 1
                elif event.key == pygame.K_a:
                    dx, dy = -1, 0
                elif event.key == pygame.K_d:
                    dx, dy = 1, 0
                elif event.key == pygame.K_e:
                    # Взаємодія з телефоном
                    if tile_map[tile_y][tile_x] == "T":
                        dialog_active = True
                        talked_on_phone = True
                        if current_puzzle == "Puzzle 1":
                            dialog_text = "Телефон: Спробуй головоломку 1!"
                        elif current_puzzle == "Puzzle 2":
                            dialog_text = "Телефон: Спробуй головоломку 2!"
                        else:
                            dialog_text = "Телефон: Спробуй головоломку 3!"
                    # Взаємодія з компом
                    elif tile_map[tile_y][tile_x] == "C":
                        if talked_on_phone:
                            dialog_active = False  # закриваємо діалог перед запуском
                            pygame.display.flip()
                            pygame.time.wait(200)

                            # Запускаємо puzzle1.py
                            subprocess.run([sys.executable, "puzzle1.py"])

                            # Після завершення puzzle1 повертаємось в main.py
                            print("Головоломка завершена. Повертаємось у світ.")

                        else:
                            dialog_active = True
                            dialog_text = "Спочатку поговори по телефону!"

                # Рух
                target_x = tile_x + dx
                target_y = tile_y + dy
                if 0 <= target_x < len(tile_map[0]) and 0 <= target_y < len(tile_map):
                    if tile_map[target_y][target_x] in ["0", "C", "T"]:
                        move_dir = (dx, dy)
                        player_state = "moving"

        # Закриття діалогу
        if dialog_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                dialog_active = False

    # --- Оновлення руху ---
    if player_state == "moving":
        target_pixel_x = tile_x * TILE_SIZE + move_dir[0] * TILE_SIZE
        target_pixel_y = tile_y * TILE_SIZE + move_dir[1] * TILE_SIZE

        # рух по x
        if pixel_x < target_pixel_x:
            pixel_x += move_speed
            if pixel_x > target_pixel_x:
                pixel_x = target_pixel_x
        elif pixel_x > target_pixel_x:
            pixel_x -= move_speed
            if pixel_x < target_pixel_x:
                pixel_x = target_pixel_x

        # рух по y
        if pixel_y < target_pixel_y:
            pixel_y += move_speed
            if pixel_y > target_pixel_y:
                pixel_y = target_pixel_y
        elif pixel_y > target_pixel_y:
            pixel_y -= move_speed
            if pixel_y < target_pixel_y:
                pixel_y = target_pixel_y

        # завершення руху
        if pixel_x == target_pixel_x and pixel_y == target_pixel_y:
            tile_x += move_dir[0]
            tile_y += move_dir[1]
            player_state = "standing"

    # --- Малювання ---
    screen.fill(BLACK)
    for y, row in enumerate(tile_map):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == "1":
                pygame.draw.rect(screen, GRAY, rect)
            elif tile == "C":
                pygame.draw.rect(screen, YELLOW, rect)
            elif tile == "T":
                pygame.draw.rect(screen, PURPLE, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

    # Малюємо персонажа
    rect = pygame.Rect(pixel_x, pixel_y, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, BLUE, rect)

    # Підказка
    if player_state == "standing" and not dialog_active:
        if tile_map[tile_y][tile_x] in ["C", "T"]:
            font = pygame.font.SysFont(None, 24)
            hint_surface = font.render("E - взаємодіяти", True, WHITE)
            screen.blit(hint_surface, (pixel_x, pixel_y - 20))

    # Малюємо діалог
    if dialog_active:
        dialog_rect = pygame.Rect(50, HEIGHT - 100, WIDTH - 100, 80)
        pygame.draw.rect(screen, WHITE, dialog_rect)
        pygame.draw.rect(screen, BLACK, dialog_rect, 2)
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(dialog_text, True, BLACK)
        screen.blit(text_surface, (dialog_rect.x + 10, dialog_rect.y + 10))

    pygame.display.flip()
    clock.tick(60)
