import pygame
import random
import sys

pygame.init()

# Screen
WIDTH = 600
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CAR RACING GAME")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GREEN = (30, 150, 60)
RED = (230, 40, 40)
BLUE = (40, 100, 255)
YELLOW = (255, 220, 0)
GRAY = (80, 80, 80)

font = pygame.font.SysFont("Arial", 30, bold=True)
bigfont = pygame.font.SysFont("Arial", 55, bold=True)

# Player car
player = pygame.Rect(270, 560, 55, 90)

# Enemy cars
enemies = []

# Game variables
score = 0
speed = 6
game_over = False
road_line_y = 0

def draw_car(rect, color):
    # Shadow
    pygame.draw.rect(
        screen, BLACK,
        (rect.x + 5, rect.y + 5, rect.width, rect.height),
        border_radius=10
    )

    # Car body
    pygame.draw.rect(
        screen, color, rect,
        border_radius=10
    )

    # Windows
    pygame.draw.rect(
        screen, (150, 220, 255),
        (rect.x + 9, rect.y + 12, 37, 25),
        border_radius=5
    )

    pygame.draw.rect(
        screen, (150, 220, 255),
        (rect.x + 9, rect.y + 50, 37, 20),
        border_radius=5
    )

    # Wheels
    pygame.draw.rect(
        screen, BLACK,
        (rect.x - 5, rect.y + 15, 8, 22)
    )

    pygame.draw.rect(
        screen, BLACK,
        (rect.x + 52, rect.y + 15, 8, 22)
    )

    pygame.draw.rect(
        screen, BLACK,
        (rect.x - 5, rect.y + 60, 8, 22)
    )

    pygame.draw.rect(
        screen, BLACK,
        (rect.x + 52, rect.y + 60, 8, 22)
    )

def draw_road():
    global road_line_y

    screen.fill(GREEN)

    # Road
    pygame.draw.rect(
        screen, GRAY,
        (100, 0, 400, HEIGHT)
    )

    # Road borders
    pygame.draw.rect(
        screen, WHITE,
        (95, 0, 5, HEIGHT)
    )

    pygame.draw.rect(
        screen, WHITE,
        (500, 0, 5, HEIGHT)
    )

    # Moving road lines
    for y in range(-100, HEIGHT, 140):
        pygame.draw.rect(
            screen, YELLOW,
            (295, y + road_line_y, 10, 70)
        )

    road_line_y += speed

    if road_line_y >= 140:
        road_line_y = 0

def reset_game():
    global score, speed, game_over, enemies

    score = 0
    speed = 6
    enemies = []
    player.x = 270
    player.y = 560
    game_over = False

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if game_over and event.key == pygame.K_r:
                reset_game()

    if not game_over:

        # Player movement
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= 7

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += 7

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.y -= 5

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.y += 5

        # Keep car on road
        player.x = max(110, min(435, player.x))
        player.y = max(0, min(610, player.y))

        # Spawn enemy cars
        if random.randint(1, 35) == 1:
            enemy_x = random.choice([150, 230, 315, 400])

            enemies.append(
                pygame.Rect(enemy_x, -100, 55, 90)
            )

        # Move enemies
        for enemy in enemies[:]:

            enemy.y += speed

            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                score += 10

            # Collision
            if player.colliderect(enemy):
                game_over = True

        # Increase speed
        speed = min(15, 6 + score // 100)

    # Draw
    draw_road()

    for enemy in enemies:
        draw_car(enemy, RED)

    draw_car(player, BLUE)

    # Score
    score_text = font.render(
        "SCORE: " + str(score),
        True, WHITE
    )

    screen.blit(score_text, (15, 15))

    speed_text = font.render(
        "SPEED: " + str(speed),
        True, YELLOW
    )

    screen.blit(speed_text, (15, 55))

    # Game over
    if game_over:

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        text = bigfont.render(
            "GAME OVER", True, RED
        )

        screen.blit(
            text,
            text.get_rect(center=(WIDTH // 2, 280))
        )

        draw_text = font.render(
            "FINAL SCORE: " + str(score),
            True, WHITE
        )

        screen.blit(
            draw_text,
            draw_text.get_rect(center=(WIDTH // 2, 350))
        )

        restart = font.render(
            "PRESS R TO RESTART",
            True, YELLOW
        )

        screen.blit(
            restart,
            restart.get_rect(center=(WIDTH // 2, 420))
        )

    pygame.display.update()

pygame.quit()
sys.exit()


