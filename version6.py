import pygame
import random
import math
import time

pygame.init()

# Configuración de la pantalla y título
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Bad Circles")

# Colores
FONDO = (180, 240, 255) 
PASTO = (110, 200, 80) 
NEGRO = (0, 0, 0)
ROJO = (255, 100, 100)
ENEMIGO_COLOR = (100, 30, 30)
FRUTAS_COLORES = [(255, 0, 0), (255, 165, 0), (138, 43, 226)] # manzana, naranja, uva

# Jugador y enemigo
jugador = pygame.Rect(400, 300, 40, 40)
enemigo = pygame.Rect(100, 100, 40, 40)
vel_jugador = 4
vel_enemigo = 1

# Frutas
frutas = [pygame.Rect(random.randint(50, 750), random.randint(50, 550), 20, 25) for _ in range(5)]
puntos = 0
nivel = 1
obstaculos = []

# Fuentes y reloj
fuente = pygame.font.Font(None, 36)
reloj = pygame.time.Clock()

# Función para dibujar el fondo tipo pasto
def dibujar_fondo():
    pantalla.fill(FONDO)
    for x in range(0, ANCHO, 40):
        for y in range(0, ALTO, 40):
            pygame.draw.rect(pantalla, PASTO, (x, y, 35, 35), 1)

# Función para dibujar el jugador
def dibujar_jugador():
    pygame.draw.circle(pantalla, ROJO, jugador.center, 20) # Círculo rojo
    cx, cy = jugador.center
    pygame.draw.circle(pantalla, NEGRO, (cx - 8, cy - 6), 3) # ojo izquierdo
    pygame.draw.circle(pantalla, NEGRO, (cx + 8, cy - 6), 3) # ojo derecho
    pygame.draw.arc(pantalla, NEGRO, (cx - 10, cy + 5, 20, 10), math.pi, 2 * math.pi, 2) # boca enojada

# Función para dibujar el enemigo
def dibujar_enemigo():
    pygame.draw.rect(pantalla, ENEMIGO_COLOR, enemigo) # enemigo



# Función para mover al enemigo
def mover_enemigo():
    dx, dy = jugador.centerx - enemigo.centerx, jugador.centery - enemigo.centery
    dist = math.hypot(dx, dy)
    if dist > 0:
        enemigo.x += int(vel_enemigo * dx / dist)
        enemigo.y += int(vel_enemigo * dy / dist)

# Función para dibujar las frutas
def dibujar_frutas():
    for i, fruta in enumerate(frutas):
        color = FRUTAS_COLORES[i % len(FRUTAS_COLORES)]
        pygame.draw.ellipse(pantalla, color, fruta) # Cuerpo de la fruta
        pygame.draw.line(pantalla, (34, 139, 34), (fruta.centerx, fruta.top), (fruta.centerx, fruta.top - 5), 2) # Tallo

# Función para dibujar obstáculos
def dibujar_obstaculos():
    for obs in obstaculos:
        pygame.draw.rect(pantalla, (139, 69, 19), obs) 

# Función para mover los obstáculos
def mover_obstaculos():
    global obstaculos
    for obs in obstaculos:
        obs.x -= 2 # Obstáculos izquierda
        if obs.right < 0: # Si sale de la pantalla se reubica
            obstaculos.remove(obs)
            obstaculos.append(pygame.Rect(ANCHO, random.randint(50, ALTO - 50), 40, 40))

# Función para comprobar las colisiones con las frutas
def comprobar_frutas():
    global puntos
    for i, fruta in enumerate(frutas):
        if jugador.colliderect(fruta):
            puntos += 1
            frutas[i].x = random.randint(50, 750)
            frutas[i].y = random.randint(50, 550)

# Función para comprobar la colisión con el enemigo
def comprobar_enemigo():
    global nivel
    if jugador.colliderect(enemigo):
        nivel = 1 # Reiniciar el nivel
        return True
    return False

# Función para aumentar la dificultad del juego (más rápido, más obstáculos)
def aumentar_dificultad():
    global vel_enemigo, obstaculos, nivel
    if puntos >= 5 and nivel == 1:
        nivel = 2
        vel_enemigo = 2 # Aumentar la velocidad del enemigo
        obstaculos.append(pygame.Rect(ANCHO, random.randint(50, ALTO - 50), 40, 40)) # Añadir un obstáculo
    elif puntos >= 10 and nivel == 2:
        nivel = 3
        vel_enemigo = 3 # Aumentar aún más la velocidad del enemigo
        obstaculos.append(pygame.Rect(ANCHO, random.randint(50, ALTO - 50), 40, 40)) # Añadir más obstáculos

# Función para mostrar los puntos y el nivel
def mostrar_puntos():
    texto = fuente.render(f"Puntos: {puntos} Nivel: {nivel}", True, NEGRO)
    pantalla.blit(texto, (10, 10))

# Función para mostrar el mensaje de Game Over
def mostrar_game_over():
    texto = fuente.render(f"¡Perdiste! Puntos: {puntos}", True, NEGRO)
    pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2))
    pygame.display.flip()
    pygame.time.wait(3000) # Esperar 3 segundos
# Función principal del juego
def juego():
    global puntos, nivel, obstaculos
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movimiento del jugador
        teclas = pygame.key.get_pressed()
        jugador.x += (teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]) * vel_jugador
        jugador.y += (teclas[pygame.K_DOWN] - teclas[pygame.K_UP]) * vel_jugador

        # Aumentando la dificultad
        aumentar_dificultad()

        # Mover al enemigo
        mover_enemigo()
        mover_obstaculos()

        # Comprobar colisiones
        comprobar_frutas()
        if comprobar_enemigo():
            mostrar_game_over()
            break

        # Dibujar todo en pantalla
        dibujar_fondo()
        dibujar_jugador()
        dibujar_enemigo()
        dibujar_frutas()
        dibujar_obstaculos()
        mostrar_puntos()

        # Actualizar pantalla
        pygame.display.flip()
        reloj.tick(60)

# Ejecutar el juego
juego()

pygame.quit()