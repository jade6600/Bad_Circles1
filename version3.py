import pygame
import sys
import pygame
import random

# Inicializar Pygame
pygame.init()

WIDTH, HEIGHT = 640, 480
TILE = 32
ROWS = HEIGHT // TILE
COLS = WIDTH // TILE

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bad Circles - Nivel 1")
# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 100, 255)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
CYAN = (100, 255, 255)
GRAY = (150, 150, 150)

font = pygame.font.SysFont(None, 36)

player = {'x': 5, 'y': 5, 'dir': 'DOWN'}
fruits = [(random.randint(1, COLS-2), random.randint(1, ROWS-2)) for _ in range(6)]
enemies = [{'x': 15, 'y': 10}, {'x': 10, 'y': 13}]
ice_blocks = []

clock = pygame.time.Clock()

def draw_face(x, y):
    px, py = x * TILE, y * TILE
    center = (px + TILE//2, py + TILE//2)
    pygame.draw.circle(win, BLUE, center, 14)

    # Ojos
    pygame.draw.circle(win, BLACK, (center[0] - 5, center[1] - 5), 2)
    pygame.draw.circle(win, BLACK, (center[0] + 5, center[1] - 5), 2)

    # Boca enojada
    rect = pygame.Rect(center[0] - 6, center[1] + 2, 12, 8)
    pygame.draw.arc(win, BLACK, rect, 3.14, 0, 2)

def draw():
    win.fill(BLACK)
    for x in range(0, WIDTH, TILE):
        pygame.draw.line(win, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILE):
        pygame.draw.line(win, GRAY, (0, y), (WIDTH, y))

    for fx, fy in fruits:
        pygame.draw.rect(win, GREEN, (fx*TILE+8, fy*TILE+8, 16, 16))

    draw_face(player['x'], player['y'])

    for e in enemies:
        pygame.draw.circle(win, RED, (e['x']*TILE + TILE//2, e['y']*TILE + TILE//2), 14)

    for bx, by in ice_blocks:
        pygame.draw.rect(win, CYAN, (bx*TILE+4, by*TILE+4, TILE-8, TILE-8))

    pygame.display.update()

def mostrar_mensaje(texto, color):
    mensaje = font.render(texto, True, color)
    rect = mensaje.get_rect(center=(WIDTH//2, HEIGHT//2))
    win.blit(mensaje, rect)
    pygame.display.update()
    pygame.time.delay(2000)

def colocar_hielo():
    dx, dy = 0, 0
    if player['dir'] == 'UP': dy = -1
    if player['dir'] == 'DOWN': dy = 1
    if player['dir'] == 'LEFT': dx = -1
    if player['dir'] == 'RIGHT': dx = 1
    nx, ny = player['x'] + dx, player['y'] + dy
    if (nx, ny) not in ice_blocks and 0 <= nx < COLS and 0 <= ny < ROWS:
        ice_blocks.append((nx, ny))

def mover_entidad(entidad, dx, dy):
    nx, ny = entidad['x'] + dx, entidad['y'] + dy
    if 0 <= nx < COLS and 0 <= ny < ROWS and (nx, ny) not in ice_blocks:
        entidad['x'], entidad['y'] = nx, ny

def mover_enemigo(e):
    dx = dy = 0
    if e['x'] < player['x']: dx = 1
    elif e['x'] > player['x']: dx = -1
    if e['y'] < player['y']: dy = 1
    elif e['y'] > player['y']: dy = -1

    opciones = [(dx, 0), (0, dy), (dx, dy)]
    random.shuffle(opciones)
    for ox, oy in opciones:
        nx, ny = e['x'] + ox, e['y'] + oy
        if 0 <= nx < COLS and 0 <= ny < ROWS and (nx, ny) not in ice_blocks:
            e['x'], e['y'] = nx, ny
            break

run = True
while run:
    clock.tick(8)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                colocar_hielo()

    # Movimiento jugador
    if keys[pygame.K_UP]:
        player['dir'] = 'UP'
        mover_entidad(player, 0, -1)
    elif keys[pygame.K_DOWN]:
        player['dir'] = 'DOWN'
        mover_entidad(player, 0, 1)
    elif keys[pygame.K_LEFT]:
        player['dir'] = 'LEFT'
        mover_entidad(player, -1, 0)
    elif keys[pygame.K_RIGHT]:
        player['dir'] = 'RIGHT'
        mover_entidad(player, 1, 0)

    # Movimiento enemigos inteligentes
    for e in enemies:
        mover_enemigo

    fruits = [(fx, fy) for fx, fy in fruits if not (fx == player['x'] and fy == player['y'])]

    for e in enemies:
        if e['x'] == player['x'] and e['y'] == player['y']:
            mostrar_mensaje("¡Perdiste!", WHITE)
            run = False

    if not fruits:
        mostrar_mensaje("¡Nivel completado!", GREEN)
        run = False

    draw()

pygame.quit()
