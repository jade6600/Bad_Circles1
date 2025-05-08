import pygame
import random

pygame.init()

# Tamaño
WIDTH, HEIGHT = 640, 480
TILE = 32
ROWS = HEIGHT // TILE
COLS = WIDTH // TILE

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bad Circles - Nivel 1")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (70, 130, 255)
RED = (220, 60, 60)
GREEN = (60, 200, 100)
ORANGE = (255, 165, 0)
PURPLE = (160, 100, 255)
CYAN = (120, 255, 255)
GRAY = (220, 220, 220)
BGCOLOR = (240, 240, 255)

font = pygame.font.SysFont(None, 32)

player = {'x': 5, 'y': 5, 'dir': 'DOWN'}
score = 0
fruits = [(random.randint(2, COLS-3), random.randint(2, ROWS-3)) for _ in range(6)]
enemy = {'x': 15, 'y': 10}
ice_blocks = []
clock = pygame.time.Clock()

def draw_face(x, y):
    px, py = x * TILE, y * TILE
    center = (px + TILE//2, py + TILE//2)
    pygame.draw.circle(win, BLUE, center, 14)
    pygame.draw.circle(win, BLACK, (center[0] - 5, center[1] - 6), 2)
    pygame.draw.circle(win, BLACK, (center[0] + 5, center[1] - 6), 2)
    pygame.draw.line(win, BLACK, (center[0] - 8, center[1] - 10), (center[0] - 2, center[1] - 8), 2)
    pygame.draw.line(win, BLACK, (center[0] + 2, center[1] - 8), (center[0] + 8, center[1] - 10), 2)
    pygame.draw.arc(win, BLACK, (center[0] - 6, center[1] + 4, 12, 6), 3.14, 0, 2)

def draw_background():
    win.fill(BGCOLOR)
    for x in range(0, WIDTH, TILE):
        for y in range(0, HEIGHT, TILE):
            if (x//TILE + y//TILE) % 2 == 0:
                pygame.draw.rect(win, GRAY, (x, y, TILE, TILE), 1)

def draw():
    draw_background()
    for fx, fy in fruits:
        cx, cy = fx * TILE + TILE // 2, fy * TILE + TILE // 2
        color = random.choice([GREEN, ORANGE, PURPLE])
        pygame.draw.circle(win, color, (cx, cy), 10)
        pygame.draw.line(win, BLACK, (cx, cy - 10), (cx, cy - 15), 2)
    draw_face(player['x'], player['y'])
    ex, ey = enemy['x'], enemy['y']
    pygame.draw.circle(win, RED, (ex * TILE + TILE//2, ey * TILE + TILE//2), 14)
    for bx, by in ice_blocks:
        pygame.draw.rect(win, CYAN, (bx*TILE+4, by*TILE+4, TILE-8, TILE-8))
    score_text = font.render(f"Puntos: {score}", True, BLACK)
    win.blit(score_text, (10, 10))
    pygame.display.update()

def mensaje(texto, color):
    msg = font.render(texto, True, color)
    rect = msg.get_rect(center=(WIDTH//2, HEIGHT//2))
    win.blit(msg, rect)
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

def mover(entidad, dx, dy):
    nx, ny = entidad['x'] + dx, entidad['y'] + dy
    if 0 <= nx < COLS and 0 <= ny < ROWS and (nx, ny) not in ice_blocks:
        entidad['x'], entidad['y'] = nx, ny

def mover_enemigo_lento(e, paso):
    if paso % 2 != 0:
        return
    dx = 1 if e['x'] < player['x'] else -1 if e['x'] > player['x'] else 0
    dy = 1 if e['y'] < player['y'] else -1 if e['y'] > player['y'] else 0
    opciones = [(dx, 0), (0, dy), (dx, dy)]
    random.shuffle(opciones)
    for ox, oy in opciones:
        nx, ny = e['x'] + ox, e['y'] + oy
        if 0 <= nx < COLS and 0 <= ny < ROWS and (nx, ny) not in ice_blocks:
            e['x'], e['y'] = nx, ny
            break

run = True
paso = 0
while run:
    clock.tick(8)
    paso += 1
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            colocar_hielo()
    if keys[pygame.K_UP]:
        player['dir'] = 'UP'
        mover(player, 0, -1)
    elif keys[pygame.K_DOWN]:
        player['dir'] = 'DOWN'
        mover(player, 0, 1)
    elif keys[pygame.K_LEFT]:
        player['dir'] = 'LEFT'
        mover(player, -1, 0)
    elif keys[pygame.K_RIGHT]:
        player['dir'] = 'RIGHT'
        mover(player, 1, 0)
    mover_enemigo_lento(enemy, paso)
    new_fruits = []
    for fx, fy in fruits:
        if not (fx == player['x'] and fy == player['y']):
            new_fruits.append((fx, fy))
        else:
            score += 1
    fruits = new_fruits
    if player['x'] == enemy['x'] and player['y'] == enemy['y']:
        mensaje("¡Perdiste!", RED)
        run = False
    if not fruits:
        mensaje("¡Ganaste!", GREEN)
        run = False
    draw()

pygame.quit()
