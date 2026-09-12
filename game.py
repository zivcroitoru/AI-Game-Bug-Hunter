import pygame
import time

from game_logic import take_damage


pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GameBug Hunter - Combat Demo")

clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 26)
small_font = pygame.font.SysFont("arial", 20)
big_font = pygame.font.SysFont("arial", 42, bold=True)
huge_font = pygame.font.SysFont("arial", 56, bold=True)

MAX_HEALTH = 100

player_health = MAX_HEALTH
enemy_health = 100

player_x = 230
player_y = 330

enemy_x = 760
enemy_y = 330

last_hit_time = 0
hit_flash = False

floating_texts = []


def add_floating_text(text, x, y, color):
    floating_texts.append(
        {
            "text": text,
            "x": x,
            "y": y,
            "color": color,
            "created": time.time(),
        }
    )


def draw_health_bar(x, y, health, max_health, width=300):
    height = 30

    pygame.draw.rect(
        screen,
        (60, 65, 75),
        (x, y, width, height),
    )

    ratio = health / max_health

    # Keep visual bar inside bounds,
    # even if the underlying health value is broken.
    visual_ratio = max(0, min(ratio, 1))

    health_width = int(width * visual_ratio)

    if health > max_health:
        color = (80, 170, 255)
    elif health > 50:
        color = (70, 220, 110)
    elif health > 20:
        color = (255, 190, 70)
    else:
        color = (240, 70, 80)

    pygame.draw.rect(
        screen,
        color,
        (x, y, health_width, height),
    )

    pygame.draw.rect(
        screen,
        (235, 235, 235),
        (x, y, width, height),
        3,
    )

    text = font.render(
        f"HP: {health}",
        True,
        (255, 255, 255),
    )

    screen.blit(
        text,
        (x + 95, y - 2),
    )


def draw_player():
    body_color = (70, 160, 255)

    if hit_flash:
        body_color = (255, 90, 90)

    pygame.draw.circle(
        screen,
        body_color,
        (player_x, player_y),
        55,
    )

    # Eyes
    pygame.draw.circle(
        screen,
        (255, 255, 255),
        (player_x - 18, player_y - 12),
        8,
    )

    pygame.draw.circle(
        screen,
        (255, 255, 255),
        (player_x + 18, player_y - 12),
        8,
    )

    # Sword
    pygame.draw.line(
        screen,
        (210, 220, 230),
        (player_x + 40, player_y + 20),
        (player_x + 95, player_y - 40),
        12,
    )

    label = font.render(
        "PLAYER",
        True,
        (180, 210, 255),
    )

    screen.blit(
        label,
        (player_x - 55, player_y + 80),
    )


def draw_enemy():
    pygame.draw.circle(
        screen,
        (230, 70, 70),
        (enemy_x, enemy_y),
        60,
    )

    # Angry eyes
    pygame.draw.circle(
        screen,
        (255, 240, 230),
        (enemy_x - 20, enemy_y - 15),
        9,
    )

    pygame.draw.circle(
        screen,
        (255, 240, 230),
        (enemy_x + 20, enemy_y - 15),
        9,
    )

    # Weapon
    pygame.draw.line(
        screen,
        (180, 180, 180),
        (enemy_x - 40, enemy_y + 10),
        (enemy_x - 110, enemy_y - 50),
        15,
    )

    label = font.render(
        "ENEMY",
        True,
        (255, 190, 190),
    )

    screen.blit(
        label,
        (enemy_x - 55, enemy_y + 85),
    )


def draw_attack_arrow():
    if time.time() - last_hit_time > 0.35:
        return

    start_x = enemy_x - 70
    start_y = enemy_y

    end_x = player_x + 70
    end_y = player_y

    arrow_color = (255, 80, 80)

    # Main line
    pygame.draw.line(
        screen,
        arrow_color,
        (start_x, start_y),
        (end_x, end_y),
        12,
    )

    # Arrow head
    pygame.draw.polygon(
        screen,
        arrow_color,
        [
            (end_x, end_y),
            (end_x + 35, end_y - 25),
            (end_x + 35, end_y + 25),
        ],
    )

    label = big_font.render(
        "20 DAMAGE",
        True,
        (255, 100, 100),
    )

    screen.blit(
        label,
        (
            (start_x + end_x) // 2 - 110,
            end_y - 80,
        ),
    )


def draw_floating_texts():
    now = time.time()

    for item in floating_texts[:]:
        age = now - item["created"]

        if age > 1.2:
            floating_texts.remove(item)
            continue

        item["y"] -= 0.6

        text_surface = big_font.render(
            item["text"],
            True,
            item["color"],
        )

        screen.blit(
            text_surface,
            (item["x"], item["y"]),
        )


def draw_status():
    messages = []

    if player_health > MAX_HEALTH:
        messages.append(
            "BUG 1: DAMAGE IS HEALING THE PLAYER"
        )

    if player_health < 0:
        messages.append(
            "BUG 2: PLAYER HP WENT BELOW ZERO"
        )

    if not messages and player_health < MAX_HEALTH:
        messages.append(
            "DAMAGE LOGIC WORKING CORRECTLY"
        )

    y = 165

    for message in messages:
        color = (
            (255, 90, 90)
            if "BUG" in message
            else (90, 235, 130)
        )

        text = big_font.render(
            message,
            True,
            color,
        )

        screen.blit(
            text,
            (
                WIDTH // 2 - text.get_width() // 2,
                y,
            ),
        )

        y += 50


def draw_background():
    screen.fill(
        (18, 22, 32)
    )

    pygame.draw.rect(
        screen,
        (30, 36, 48),
        (0, 420, WIDTH, 180),
    )

    pygame.draw.line(
        screen,
        (75, 85, 100),
        (0, 420),
        (WIDTH, 420),
        4,
    )


def draw_instructions():
    line1 = small_font.render(
        "SPACE = enemy attacks player",
        True,
        (220, 220, 230),
    )

    line2 = small_font.render(
        "R = reset health",
        True,
        (220, 220, 230),
    )

    line3 = small_font.render(
        "H = set player HP to 10 (test below-zero bug)",
        True,
        (255, 210, 120),
    )

    screen.blit(
        line1,
        (40, 520),
    )

    screen.blit(
        line2,
        (350, 520),
    )

    screen.blit(
        line3,
        (520, 520),
    )


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                old_health = player_health

                player_health = take_damage(
                    player_health,
                    20,
                )

                last_hit_time = time.time()
                hit_flash = True

                delta = (
                    player_health - old_health
                )

                if delta > 0:
                    add_floating_text(
                        f"+{delta} HP",
                        player_x - 65,
                        player_y - 120,
                        (100, 220, 255),
                    )

                else:
                    add_floating_text(
                        f"{delta} HP",
                        player_x - 65,
                        player_y - 120,
                        (255, 100, 100),
                    )

            if event.key == pygame.K_r:
                player_health = MAX_HEALTH
                floating_texts.clear()

            if event.key == pygame.K_h:
                player_health = 10

    if time.time() - last_hit_time > 0.15:
        hit_flash = False

    draw_background()

    title = huge_font.render(
        "GAMEBUG HUNTER",
        True,
        (235, 240, 255),
    )

    screen.blit(
        title,
        (
            WIDTH // 2 - title.get_width() // 2,
            25,
        ),
    )

    subtitle = small_font.render(
        "Autonomous Gameplay Debugging Demo",
        True,
        (150, 180, 220),
    )

    screen.blit(
        subtitle,
        (
            WIDTH // 2 - subtitle.get_width() // 2,
            90,
        ),
    )

    draw_health_bar(
        80,
        120,
        player_health,
        MAX_HEALTH,
    )

    draw_health_bar(
        620,
        120,
        enemy_health,
        100,
    )

    draw_player()
    draw_enemy()

    draw_attack_arrow()
    draw_floating_texts()
    draw_status()
    draw_instructions()

    pygame.display.flip()

    clock.tick(60)


pygame.quit()