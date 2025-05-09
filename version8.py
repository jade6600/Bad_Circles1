import pygame
import random
import math

# Inicialización de Pygame
pygame.init()

# ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bad Circles")

# Colores
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_RED = (128, 0, 0)
DARK_GREEN = (0, 100, 0)

# Reloj
clock = pygame.time.Clock()
FPS = 60

# Funciones 
def draw_player(x, y, radius):
    pygame.draw.circle(screen, RED, (x, y), radius)

def draw_monster(x, y, size):
    pygame.draw.rect(screen, GREEN, (x, y, size, size))

def draw_fruits(fruits):
    for fruit in fruits:
        pygame.draw.circle(screen, WHITE, fruit, 15)

def draw_button(text, y_offset, color_bg):
    font = pygame.font.Font(None, 48)
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + y_offset, 200, 50)
    pygame.draw.rect(screen, color_bg, button_rect)
    text_render = font.render(text, True, WHITE)
    screen.blit(text_render, (WIDTH // 2 - text_render.get_width() // 2, HEIGHT // 2 + y_offset + 10))
    return button_rect

# Lógica general del juego por nivel
def run_level(level_number, monster_speed, fruit_count):
    player_radius = 30
    player_x = 50
    player_y = HEIGHT // 2
    player_speed = 5

    monster_size = 40
    monster_x = WIDTH - 100
    monster_y = random.randint(0, HEIGHT - monster_size)

    fruits = [(random.randint(100, 700), random.randint(100, 500)) for _ in range(fruit_count)]

    score = 0
    level_complete = False
    game_over = False
    run_game = True

    while run_game:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if level_complete:
                    next_button = draw_button("Siguiente", 50, DARK_GREEN)
                    if next_button.collidepoint(mouse_x, mouse_y):
                        return "next"
                elif game_over:
                    retry_button = draw_button("Reintentar", 50, DARK_RED)
                    if retry_button.collidepoint(mouse_x, mouse_y):
                        return "retry"

        if not level_complete and not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_x -= player_speed
            if keys[pygame.K_RIGHT]:
                player_x += player_speed
            if keys[pygame.K_UP]:
                player_y -= player_speed
            if keys[pygame.K_DOWN]:
                player_y += player_speed

            # Movimiento del monstruo hacia el jugador 
            dx = player_x - monster_x
            dy = player_y - monster_y
            distance = math.hypot(dx, dy)
            if distance != 0:
                dx /= distance
                dy /= distance
            monster_x += dx * monster_speed
            monster_y += dy * monster_speed

            # Colisión jugador-monstruo
            if math.hypot(player_x - monster_x, player_y - monster_y) < player_radius + monster_size / 2:
                game_over = True

            # Recolección de frutas
            for fruit in fruits[:]:
                if player_x + player_radius > fruit[0] - 15 and player_x - player_radius < fruit[0] + 15 and player_y + player_radius > fruit[1] - 15 and player_y - player_radius < fruit[1] + 15:
                    fruits.remove(fruit)
                    score += 10

            if not fruits:
                level_complete = True

        # Dibujar todo
        draw_player(int(player_x), int(player_y), player_radius)
        draw_monster(int(monster_x), int(monster_y), monster_size)
        draw_fruits(fruits)

        # Puntaje
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Mensajes finales
        if level_complete:
            font = pygame.font.Font(None, 48)
            text = font.render(f"¡Nivel {level_number} Completado!", True, WHITE)
            screen.blit(text, (WIDTH // 2 - 170, HEIGHT // 2 - 50))
            draw_button("Siguiente", 50, DARK_GREEN)
        elif game_over:
            font = pygame.font.Font(None, 48)
            text = font.render("¡Has perdido!", True, RED)
            screen.blit(text, (WIDTH // 2 - 120, HEIGHT // 2 - 50))
            draw_button("Reintentar", 50, DARK_RED)

        pygame.display.update()
        clock.tick(FPS)

# Juego principal
def main():
    level = 1
    while True:
        result = run_level(level, monster_speed=0.5 + level, fruit_count=4 + level * 2)
        if result == "next":
            level += 1
        elif result == "retry":
            continue
        elif result == "quit" or result is False:
            break

main()