import pygame
import sys
import random
# Inicialización
pygame.init()

# Pantalla
WIDTH, HEIGHT = 640, 480
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bad Circles - Nivel 1")

# Colores
WHITE = (255, 255, 255)
RED = (220, 50, 50)
GREEN = (50, 220, 50)
BLUE = (50, 100, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Jugador
player_radius = 15
player_x, player_y = 100, 100
player_speed = 4

# Frutas
fruit_size = 12
fruits = [(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)) for _ in range(8)]

# Enemigos
enemy1 = {'x': 300, 'y': 200, 'dir': 1, 'speed': 2}
enemy2 = {'x': 500, 'y': 350, 'dir': -1, 'speed': 1.5}

# Texto
font = pygame.font.SysFont(None, 40)

# Reloj
clock = pygame.time.Clock()

def draw_game():
    win.fill(BLACK)
    # Frutas
    for fx, fy in fruits:
        pygame.draw.rect(win, GREEN, (fx, fy, fruit_size, fruit_size))
    # Jugador
    pygame.draw.circle(win, BLUE, (player_x, player_y), player_radius)
    # Enemigos
    pygame.draw.circle(win, RED, (int(enemy1['x']), int(enemy1['y'])), player_radius)
    pygame.draw.circle(win, RED, (int(enemy2['x']), int(enemy2['y'])), player_radius)
    pygame.display.update()

def mostrar_mensaje(texto, color):
    mensaje = font.render(texto, True, color)
    rect = mensaje.get_rect(center=(WIDTH//2, HEIGHT//2))
    win.blit(mensaje, rect)
    pygame.display.update()
    pygame.time.delay(2000)

# Juego
run = True
while run:
    clock.tick(60)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Movimiento jugador
    if keys[pygame.K_LEFT]: player_x -= player_speed
    if keys[pygame.K_RIGHT]: player_x += player_speed
    if keys[pygame.K_UP]: player_y -= player_speed
    if keys[pygame.K_DOWN]: player_y += player_speed

    # Limitar al borde
    player_x = max(player_radius, min(WIDTH - player_radius, player_x))
    player_y = max(player_radius, min(HEIGHT - player_radius, player_y))

    # Movimiento enemigos
    enemy1['x'] += enemy1['dir'] * enemy1['speed']
    if enemy1['x'] <= 0 or enemy1['x'] >= WIDTH:
        enemy1['dir'] *= -1

    enemy2['y'] += enemy2['dir'] * enemy2['speed']
    if enemy2['y'] <= 0 or enemy2['y'] >= HEIGHT:
        enemy2['dir'] *= -1

    # Aumentar dificultad si quedan pocas frutas
    if len(fruits) <= 3:
        enemy1['speed'] = 3
        enemy2['speed'] = 2.5

    # Recolección de frutas
    fruits = [f for f in fruits if not (abs(player_x - f[0]) < 18 and abs(player_y - f[1]) < 18)]

    # Colisión con enemigos
    for enemy in [enemy1, enemy2]:
        if abs(player_x - enemy['x']) < player_radius * 2 and abs(player_y - enemy['y']) < player_radius * 2:
            mostrar_mensaje("¡Perdiste!", YELLOW)
            run = False

    # Fin del nivel
    if not fruits:
        mostrar_mensaje("¡Nivel Completado!", GREEN)
        run = False

    draw_game()

pygame.quit()

# Inicialización
pygame.init()

# Pantalla
WIDTH, HEIGHT = 640, 480
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bad Circles - Nivel 1")

# Colores
WHITE = (255, 255, 255)
RED = (220, 50, 50)
GREEN = (50, 220, 50)
BLUE = (50, 100, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Jugador
player_radius = 15
player_x, player_y = 100, 100
player_speed = 4

# Frutas
fruit_size = 12
fruits = [(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)) for _ in range(8)]

# Enemigos
enemy1 = {'x': 300, 'y': 200, 'dir': 1, 'speed': 2}
enemy2 = {'x': 500, 'y': 350, 'dir': -1, 'speed': 1.5}

# Texto
font = pygame.font.SysFont(None, 40)

# Reloj
clock = pygame.time.Clock()

def draw_game():
    win.fill(BLACK)
    # Frutas
    for fx, fy in fruits:
        pygame.draw.rect(win, GREEN, (fx, fy, fruit_size, fruit_size))
    # Jugador
    pygame.draw.circle(win, BLUE, (player_x, player_y), player_radius)
    # Enemigos
    pygame.draw.circle(win, RED, (int(enemy1['x']), int(enemy1['y'])), player_radius)
    pygame.draw.circle(win, RED, (int(enemy2['x']), int(enemy2['y'])), player_radius)
    pygame.display.update()

def mostrar_mensaje(texto, color):
    mensaje = font.render(texto, True, color)
    rect = mensaje.get_rect(center=(WIDTH//2, HEIGHT//2))
    win.blit(mensaje, rect)
    pygame.display.update()
    pygame.time.delay(2000)

# Juego
run = True
while run:
    clock.tick(60)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Movimiento jugador
    if keys[pygame.K_LEFT]: player_x -= player_speed
    if keys[pygame.K_RIGHT]: player_x += player_speed
    if keys[pygame.K_UP]: player_y -= player_speed
    if keys[pygame.K_DOWN]: player_y += player_speed

    # Limitar al borde
    player_x = max(player_radius, min(WIDTH - player_radius, player_x))
    player_y = max(player_radius, min(HEIGHT - player_radius, player_y))

    # Movimiento enemigos
    enemy1['x'] += enemy1['dir'] * enemy1['speed']
    if enemy1['x'] <= 0 or enemy1['x'] >= WIDTH:
        enemy1['dir'] *= -1

    enemy2['y'] += enemy2['dir'] * enemy2['speed']
    if enemy2['y'] <= 0 or enemy2['y'] >= HEIGHT:
        enemy2['dir'] *= -1

    # Aumentar dificultad si quedan pocas frutas
    if len(fruits) <= 3:
        enemy1['speed'] = 3
        enemy2['speed'] = 2.5

    # Recolección de frutas
    fruits = [f for f in fruits if not (abs(player_x - f[0]) < 18 and abs(player_y - f[1]) < 18)]

    # Colisión con enemigos
    for enemy in [enemy1, enemy2]:
        if abs(player_x - enemy['x']) < player_radius * 2 and abs(player_y - enemy['y']) < player_radius * 2:
            mostrar_mensaje("¡Perdiste!", YELLOW)
            run = False

    # Fin del nivel
    if not fruits:
        mostrar_mensaje("¡Nivel Completado!", GREEN)
        run = False

    draw_game()

pygame.quit()
