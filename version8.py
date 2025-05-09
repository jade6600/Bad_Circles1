import pygame
import random
import math

pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("BAD CIRCLES")

# Colores
FONDO = (180, 240, 255)
PASTO = (110, 200, 80)
NEGRO = (0, 0, 0)
ROJO = (255, 100, 100)
ENEMIGO_COLOR = (100, 60, 60)
FRUTAS_COLORES = [(255, 0, 0), (255, 165, 0), (138, 43, 226)]

# Jugador y enemigo
jugador = pygame.Rect(400, 300, 40, 40)
enemigo = pygame.Rect(100, 100, 40, 40)
vel_jugador = 4
vel_enemigo = 1.5

# Obstáculos
bloques = [pygame.Rect(random.randint(0, ANCHO - 40), random.randint(0, ALTO - 40), 40, 40) for _ in range(30)]

# Frutas
frutas = [pygame.Rect(random.randint(50, 750), random.randint(50, 550), 20, 25) for _ in range(6)]

# Texto
fuente = pygame.font.Font(None, 36)
reloj = pygame.time.Clock()
puntos = 0

def dibujar_fondo():
    pantalla.fill(FONDO)
    for x in range(0, ANCHO, 40):
        for y in range(0, ALTO, 40):
            pygame.draw.rect(pantalla, PASTO, (x, y, 38, 38), 1)

def dibujar_jugador():
    pygame.draw.circle(pantalla, ROJO, jugador.center, 20)
    cx, cy = jugador.center
    pygame.draw.circle(pantalla, NEGRO, (cx - 8, cy - 6), 3)
    pygame.draw.circle(pantalla, NEGRO, (cx + 8, cy - 6), 3)
    pygame.draw.arc(pantalla, NEGRO, (cx - 10, cy + 5, 20, 10), math.pi, 2 * math.pi, 2)

def dibujar_enemigo():
    pygame.draw.rect(pantalla, ENEMIGO_COLOR, enemigo)

def dibujar_bloques():
    for b in bloques:
        pygame.draw.rect(pantalla, (90, 190, 90), b)

def dibujar_frutas():
    for i, fruta in enumerate(frutas):
        color = FRUTAS_COLORES[i % len(FRUTAS_COLORES)]
        pygame.draw.ellipse(pantalla, color, fruta)
        pygame.draw.line(pantalla, (34, 139, 34), (fruta.centerx, fruta.top), (fruta.centerx, fruta.top - 5), 2)

def mostrar_puntos():
    texto = fuente.render(f"Puntos: {puntos}", True, NEGRO)
    pantalla.blit(texto, (10, 10))

def mover_enemigo():
    dx = jugador.centerx - enemigo.centerx
    dy = jugador.centery - enemigo.centery
    dist = math.hypot(dx, dy)
    if dist != 0:
        dx, dy = dx / dist, dy / dist
        enemigo.x += dx * vel_enemigo
        enemigo.y += dy * vel_enemigo

    enemigo.x = int(enemigo.x)
    enemigo.y = int(enemigo.y)

    for b in bloques:
        if enemigo.colliderect(b):
            enemigo.x -= dx * vel_enemigo
            enemigo.y -= dy * vel_enemigo

def mover_jugador(teclas):
    mov_x = (teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]) * vel_jugador
    mov_y = (teclas[pygame.K_DOWN] - teclas[pygame.K_UP]) * vel_jugador

    jugador.x += mov_x
    for b in bloques:
        if jugador.colliderect(b):
            jugador.x -= mov_x

    jugador.y += mov_y
    for b in bloques:
        if jugador.colliderect(b):
            jugador.y -= mov_y

def comprobar_frutas():
    global puntos
    for i, fruta in enumerate(frutas):
        if jugador.colliderect(fruta):
            puntos += 1
            frutas[i].x = random.randint(50, 750)
            frutas[i].y = random.randint(50, 550)

def comprobar_derrota():
    return jugador.colliderect(enemigo)

def game_over():
    texto = fuente.render(f"¡Perdiste! Puntos: {puntos}", True, NEGRO)
    pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2))
    pygame.display.flip()
    pygame.time.wait(3000)

def juego():
    global puntos
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        teclas = pygame.key.get_pressed()
        mover_jugador(teclas)
        mover_enemigo()
        comprobar_frutas()

        if comprobar_derrota():
            game_over()
            corriendo = False

        dibujar_fondo()
        dibujar_bloques()
        dibujar_frutas()
        dibujar_jugador()
        dibujar_enemigo()
        mostrar_puntos()

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()

juego()