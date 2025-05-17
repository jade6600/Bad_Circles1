import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Pantalla
ANCHO = 800
ALTO = 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Rebota la Pelota")

# Colores
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
NEGRO = (0, 0, 0)
ROSA = (255,0,80)
# Fuente
fuente = pygame.font.SysFont(None, 48)

# Pelota
pelota_radio = 5
pelota_x = ANCHO // 2
pelota_y = ALTO // 2
pelota_vel_x = 4
pelota_vel_y = 4

# Barra
barra_ancho = 100
barra_alto = 15
barra_y = ALTO - 40
barra_x = (ANCHO - barra_ancho) // 2

# Reloj
clock = pygame.time.Clock()

# Función para mostrar texto centrado
def mostrar_texto(texto):
    render = fuente.render(texto, True, NEGRO)
    rect = render.get_rect(center=(ANCHO // 2, ALTO // 2))
    screen.blit(render, rect)
    pygame.display.flip()

# Bucle principal del juego
def jugar():
    global pelota_x, pelota_y, pelota_vel_x, pelota_vel_y

    corriendo = True
    while corriendo:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movimiento barra con mouse
        mouse_x, _ = pygame.mouse.get_pos()
        barra_x = mouse_x - barra_ancho // 2
        barra_x = max(0, min(barra_x, ANCHO - barra_ancho))

        # Movimiento pelota
        pelota_x += pelota_vel_x
        pelota_y += pelota_vel_y

        # Rebote en los bordes
        if pelota_x <= 0 or pelota_x >= ANCHO - pelota_radio:
            pelota_vel_x *= -1
        if pelota_y <= 0:
            pelota_vel_y *= -1

        # Colisiones
        barra_rect = pygame.Rect(barra_x, barra_y, barra_ancho, barra_alto)
        pelota_rect = pygame.Rect(pelota_x, pelota_y, pelota_radio*2, pelota_radio*2)

        if pelota_rect.colliderect(barra_rect):
            pelota_vel_y *= -1
            pelota_y = barra_y - pelota_radio * 2

        # Si se cae
        if pelota_y > ALTO:
            corriendo = False

        # Dibujar
        screen.fill(BLANCO)
        pygame.draw.circle(screen, ROSA, (pelota_x, pelota_y), pelota_radio)
        pygame.draw.rect(screen, AZUL, barra_rect)
        pygame.display.flip()

    game_over()

# Pantalla de Game Over
def game_over():
    mostrar_texto("¡Game Over! Presiona ESPACIO para reiniciar")

    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reiniciar()
                    esperando = False

# Reiniciar posiciones
def reiniciar():
    global pelota_x, pelota_y, pelota_vel_x, pelota_vel_y
    pelota_x = ANCHO // 2
    pelota_y = ALTO // 2
    pelota_vel_x = random.choice([-4, 4])
    pelota_vel_y = 4
    jugar()

# Iniciar juego
jugar()

