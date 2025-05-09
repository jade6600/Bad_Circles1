import pygame
import random
import math

pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("BAD CIRCLES")

# Colores
FONDO = (180, 240, 255)
AZUL_CLARO = (200, 240, 255)
AZUL_HIELO = (160, 210, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 100, 100)
ENEMIGO_COLOR = (100, 30, 30)
FRUTAS_COLORES = [(255, 0, 0), (255, 165, 0), (138, 43, 226)] # manzana, naranja, uva

# Jugador y enemigo
jugador = pygame.Rect(400, 300, 40, 40)
enemigo = pygame.Rect(100, 100, 40, 40)
vel_jugador = 4
vel_enemigo = 3

# Frutas
frutas = [pygame.Rect(random.randint(50, 750), random.randint(50, 550), 20, 25) for _ in range(5)]
puntos = 0
reloj = pygame.time.Clock()
fuente = pygame.font.Font(None, 36)

def dibujar_fondo():
    pantalla.fill(FONDO)
    for x in range(0, ANCHO, 40):
        for y in range(0, ALTO, 40):
            pygame.draw.rect(pantalla, AZUL_HIELO, (x, y, 35, 35), 1)

def dibujar_jugador():
    pygame.draw.circle(pantalla, ROJO, jugador.center, 20)
    cx, cy = jugador.center
    pygame.draw.circle(pantalla, NEGRO, (cx - 8, cy - 6), 3) # ojo izq
    pygame.draw.circle(pantalla, NEGRO, (cx + 8, cy - 6), 3) # ojo der
    pygame.draw.arc(pantalla, NEGRO, (cx - 10, cy + 5, 20, 10), math.pi, 2 * math.pi, 2) # boca enojada

def dibujar_enemigo():
    pygame.draw.circle(pantalla, ENEMIGO_COLOR, enemigo.center, 20)

def mover_enemigo():
    dx, dy = jugador.centerx - enemigo.centerx, jugador.centery - enemigo.centery
    dist = math.hypot(dx, dy)
    if dist > 0:
        enemigo.x += int(vel_enemigo * dx / dist)
        enemigo.y += int(vel_enemigo * dy / dist)

def dibujar_frutas():
    for i, fruta in enumerate(frutas):
        color = FRUTAS_COLORES[i % len(FRUTAS_COLORES)]
        pygame.draw.ellipse(pantalla, color, fruta) # cuerpo de fruta
        pygame.draw.line(pantalla, (34, 139, 34), (fruta.centerx, fruta.top), (fruta.centerx, fruta.top - 5), 2) # tallo

def mostrar_puntos():
    texto = fuente.render(f"Puntos: {puntos}", True, NEGRO)
    pantalla.blit(texto, (10, 10))

# Juego principal
ejecutando = True
while ejecutando:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            ejecutando = False

    teclas = pygame.key.get_pressed()
    jugador.x += (teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]) * vel_jugador
    jugador.y += (teclas[pygame.K_DOWN] - teclas[pygame.K_UP]) * vel_jugador

    mover_enemigo()

    for i, fruta in enumerate(frutas):
        if jugador.colliderect(fruta):
            puntos += 1
            frutas[i].x = random.randint(50, 750)
            frutas[i].y = random.randint(50, 550)

    if jugador.colliderect(enemigo):
        ejecutando = False

    # Dibujar
    dibujar_fondo()
    dibujar_jugador()
    dibujar_enemigo()
    dibujar_frutas()
    mostrar_puntos()
    pygame.display.flip()
    reloj.tick(60)

# Mensaje final
pantalla.fill(FONDO)
mensaje = fuente.render(f"¡Perdiste! Puntos: {puntos}", True, NEGRO)
pantalla.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2, ALTO//2))
pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()
