import pygame
import random

# Inicializar Pygame
pygame.init()

# Pantalla
WIDTH, HEIGHT = 640, 480
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BAD CIRCLES - Nivel 1")

# Colores
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Jugador
player_radius = 15
player_x, player_y = 100, 100
player_speed = 4

# Frutas
fruit_size = 10
fruits = [(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)) for _ in range(5)]

# Enemigo
enemy_x, enemy_y = 300, 300
enemy_radius = 15
enemy_speed = 2
enemy_dir = 1

# Reloj
clock = pygame.time.Clock()

# Funciones
def draw_game():
    win.fill(BLACK)
    # Dibujar frutas
    for fx, fy in fruits:
        pygame.draw.rect(win, GREEN, (fx, fy, fruit_size, fruit_size))
    # Dibujar jugador
    pygame.draw.circle(win, BLUE, (player_x, player_y), player_radius)
    # Dibujar enemigo
    pygame.draw.circle(win, RED, (enemy_x, enemy_y), enemy_radius)
    pygame.display.update()

# Loop principal
run = True
while run:
    clock.tick(60)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Movimiento jugador
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Movimiento enemigo (va de lado a lado)
    enemy_x += enemy_dir * enemy_speed
    if enemy_x <= 0 or enemy_x >= WIDTH:
        enemy_dir *= -1

    # Colisión jugador con frutas
    fruits = [f for f in fruits if not (abs(player_x - f[0]) < 15 and abs(player_y - f[1]) < 15)]

    # Colisión jugador con enemigo
    if abs(player_x - enemy_x) < player_radius + enemy_radius and abs(player_y - enemy_y) < player_radius + enemy_radius:
        print("¡Perdiste!")
        run = False

    # Nivel completo
    if not fruits:
        print("¡Nivel completado!")
        run = False

    draw_game()

pygame.quit()