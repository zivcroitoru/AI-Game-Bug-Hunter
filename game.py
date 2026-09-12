import pygame
import random
import time

from game_logic import take_damage


pygame.init()

WIDTH, HEIGHT = 900, 520
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GameBug Hunter - Combat Demo")

clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 26)
small_font = pygame.font.SysFont("arial", 20)
big_font = pygame.font.SysFont("arial", 42, bold=True)

MAX_HEALTH = 100
health = MAX_HEALTH

player_x = 170
player_y = 300

enemy_x = 660
enemy_y = 295

last_hit_time = 0
hit_flash = False
floating_texts = []


def add_floating_text(text, x, y):
    floating_texts.append({
        "text": text,
        "x": x,
        "y": y,
        "created": time.time(),
    })


def draw_health_bar():
    bar_x = 70
    bar_y = 90
    bar_w = 330
    bar_h = 34

    pygame.draw.rect(screen, (70, 70, 80), (bar_x, bar_y, bar_w, bar_h))

    ratio = max(0, min(health / MAX_HEALTH, 1))
    health_w = int(bar_w * ratio)

    if health > MAX_HEALTH:
        bar_color = (120, 200, 255)
    elif health > 50:
        bar_color = (80, 220, 110)
    elif health > 25:
        bar_color = (250, 190, 70)
    else:
        bar_color = (230, 70, 70)

    pygame.draw.rect(
        screen,
        bar_color,
        (bar_x, bar_y, health_w, bar_h),
    )

    pygame.draw.rect(
        screen,
        (240, 240, 240),
        (bar_x, bar_y, bar_w, bar_h),
        3,
    )

    text = font.render(
        f"HP: {health}",
        True,
        (255, 255, 255),
    )

    screen.blit(text, (bar_x + 110, bar_y + 2))


def draw_player():
    body_color = (80, 170, 255)

    if hit_flash:
        body_color = (255, 100, 100)

    pygame.draw.circle(
        screen,
        body_color,
        (player_x, player_y),
        45,
    )

    pygame.draw.circle(
        screen,
        (230, 240, 255),
        (player_x - 15, player_y - 10),
        7,
    )

    pygame.draw.circle(
        screen,
        (230, 240, 255),
        (player_x + 15, player_y - 10),
        7,
    )

    pygame.draw.line(
        screen,
        (20, 40, 70),
        (player_x - 15, player_y + 15),
        (player_x + 15, player_y + 15),
        4,
    )

    label = small_font.render(
        "PLAYER",
        True,
        (220, 230, 255),
    )

    screen.blit(
        label,
        (player_x - 35, player_y + 60),
    )


def draw_enemy():
    pygame.draw.circle(
        screen,
        (230, 80, 80),
        (enemy_x, enemy_y),
        50,
    )

    pygame.draw.circle(
        screen,
        (255, 230, 230),
        (enemy_x - 16, enemy_y - 12),
        8,
    )

    pygame.draw.circle(
        screen,
        (255, 230, 230),
        (enemy_x + 16, enemy_y - 12),
        8,
    )

    pygame.draw.line(
        screen,
        (80, 10, 10),
        (enemy_x - 18, enemy_y + 18),
        (enemy_x + 18, enemy_y + 8),
        5,
    )

    label = small_font.render(
        "ENEMY",
        True,
        (255, 210, 210),
    )

    screen.blit(
        label,
        (enemy_x - 35, enemy_y + 65),
    )


def draw_attack_line():
    if time.time() - last_hit_time < 0.2:
        pygame.draw.line(
            screen,
            (255, 220, 80),
            (enemy_x - 55, enemy_y),
            (player_x + 45, player_y),
            8,
        )


def draw_floating_texts():
    now = time.time()

    for item in floating_texts[:]:
        age = now - item["created"]

        if age > 1.2:
            floating_texts.remove(item)
            continue

        item["y"] -= 0.5

        text_surface = big_font.render(
            item["text"],
            True,
            (255, 230, 90),
        )

        screen.blit(
            text_surface,
            (item["x"], item["y"]),
        )


def draw_status():
    if health > MAX_HEALTH:
        bug = big_font.render(
            "BUG DETECTED: DAMAGE HEALS YOU!",
            True,
            (255, 90, 90),
        )

        screen.blit(
            bug,
            (210, 155),
        )

    elif health < MAX_HEALTH:
        ok = big_font.render(
            "DAMAGE WORKS CORRECTLY",
            True,
            (100, 240, 140),
        )

        screen.blit(
            ok,
            (260, 155),
        )


def draw_instructions():
    line1 = small_font.render(
        "SPACE = enemy attack",
        True,
        (210, 210, 220),
    )

    line2 = small_font.render(
        "R = reset health",
        True,
        (210, 210, 220),
    )

    line3 = small_font.render(
        "Run GameBug Hunter to repair game_logic.py",
        True,
        (180, 200, 255),
    )

    screen.blit(line1, (65, 445))
    screen.blit(line2, (305, 445))
    screen.blit(line3, (500, 445))


def draw_background():
    screen.fill((24, 26, 35))

    pygame.draw.rect(
        screen,
        (35, 40, 55),
        (0, 390, WIDTH, 130),
    )

    pygame.draw.line(
        screen,
        (90, 100, 120),
        (0, 390),
        (WIDTH, 390),
        4,
    )


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                old_health = health

                health = take_damage(
                    health,
                    20,
                )

                last_hit_time = time.time()
                hit_flash = True

                delta = health - old_health

                if delta > 0:
                    add_floating_text(
                        f"+{delta} HP",
                        player_x - 55,
                        player_y - 95,
                    )
                else:
                    add_floating_text(
                        f"{delta} HP",
                        player_x - 55,
                        player_y - 95,
                    )

            if event.key == pygame.K_r:
                health = MAX_HEALTH
                floating_texts.clear()

    if time.time() - last_hit_time > 0.15:
        hit_flash = False

    draw_background()
    draw_health_bar()
    draw_player()
    draw_enemy()
    draw_attack_line()
    draw_floating_texts()
    draw_status()
    draw_instructions()

    title = big_font.render(
        "GAMEBUG HUNTER",
        True,
        (235, 240, 255),
    )

    subtitle = small_font.render(
        "AI Gameplay Debugging Demo",
        True,
        (150, 175, 220),
    )

    screen.blit(title, (560, 45))
    screen.blit(subtitle, (590, 95))

    pygame.display.flip()

    clock.tick(60)


pygame.quit()