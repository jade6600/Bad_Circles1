import pygame
import random
import math
import os
import time

# Inicializar Pygame
pygame.init()

# Splash Screm
def mostrar_splash_screen():
    ancho_ventana = 800
    alto_ventana = 600
    ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))
    pygame.display.set_caption("Bad Circles")

    BLANCO = (255, 255, 255)
    GRIS_CLARO = (200, 200, 200)
    AMARILLO = (255, 255, 0)
    AZUL = (135,206,150)

    fuente = pygame.font.Font(None, 48)
    fuente_pequena = pygame.font.Font(None, 30)
    fuente_extra_pequena = pygame.font.Font(None, 24)

    texto_principal = "Bad Circles"
    superficie_principal = fuente.render(texto_principal, True, BLANCO)
    rect_principal = superficie_principal.get_rect(center=(ancho_ventana // 2, alto_ventana // 2 - 50))

    superficie_bloque1 = fuente_pequena.render("Colegio San José de Guanentá", True, GRIS_CLARO)
    rect_bloque1 = superficie_bloque1.get_rect(midtop=(rect_principal.centerx, rect_principal.bottom + 10))

    superficie_bloque2 = fuente_pequena.render("Especialidad en Sistemas", True, GRIS_CLARO)
    rect_bloque2 = superficie_bloque2.get_rect(midtop=(rect_principal.centerx, rect_bloque1.bottom + 5))

    texto_creditos = "Sorteh Jhull Florez Peñaloza, Nicolle Daniela Macias Piracon y Jorge Luis Silva Morales"
    superficie_bloque3 = fuente_extra_pequena.render(texto_creditos, True, AMARILLO)
    rect_bloque3 = superficie_bloque3.get_rect(midtop=(rect_principal.centerx, rect_bloque2.bottom + 15))

    ejecutando = True
    reloj = pygame.time.Clock()

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                ejecutando = False  

        ventana.fill(AZUL)
        ventana.blit(superficie_principal, rect_principal)
        ventana.blit(superficie_bloque1, rect_bloque1)
        ventana.blit(superficie_bloque2, rect_bloque2)
        ventana.blit(superficie_bloque3, rect_bloque3)

        pygame.display.flip()
        reloj.tick(60)

# funciones
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bad Circles")

# Colores
RED = (255, 0, 0)
BLUE = (0, 150, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREEN = (0, 100, 0)
DARK_RED = (100, 0, 0)

clock = pygame.time.Clock()
FPS = 60

FONT = pygame.font.Font(None, 36)
BIG_FONT = pygame.font.Font(None, 60)

def draw_player(x, y, radius, color):
    pygame.draw.circle(screen, color, (x, y), radius)

def draw_monster(x, y, size):
    pygame.draw.rect(screen, (0, 255, 0), (x, y, size, size))

def draw_fruits(fruits):
    for fruit in fruits:
        pygame.draw.circle(screen, WHITE, fruit, 12)

def draw_button(text, y_offset, color_bg):
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + y_offset, 200, 50)
    pygame.draw.rect(screen, color_bg, button_rect, border_radius=10)
    label = FONT.render(text, True, WHITE)
    screen.blit(label, (button_rect.x + 100 - label.get_width() // 2, button_rect.y + 10))
    return button_rect

def save_highscore(score):
    try:
        with open("highscores.txt", "a") as f:
            f.write(f"{score}\n")
    except:
        pass

def show_highscores():
    screen.fill(BLACK)
    title = BIG_FONT.render("🏆 Mejores Puntajes", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 40))
    try:
        with open("highscores.txt", "r") as f:
            scores = sorted([int(x.strip()) for x in f.readlines()], reverse=True)[:5]
            for i, score in enumerate(scores):
                line = FONT.render(f"{i+1}. {score} puntos", True, WHITE)
                screen.blit(line, (WIDTH//2 - 80, 120 + i*40))
    except:
        error = FONT.render("No hay puntajes guardados.", True, WHITE)
        screen.blit(error, (WIDTH//2 - 120, 150))
    pygame.display.flip()
    pygame.time.wait(3000)

def show_instructions():
    screen.fill(BLACK)
    lines = [
        "Jugador 1: Flechas (← ↑ ↓ →)",
        "Jugador 2: W A S D",
        "Recolecten TODAS las frutas para avanzar.",
        "¡Eviten al monstruo! Si uno es atrapado, pierden los dos.",
        "",
        "Presiona ESC para volver al menú."
    ]
    for i, line in enumerate(lines):
        text = FONT.render(line, True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 100 + i * 40))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False

def run_level(level_number, monster_speed, fruit_count):
    player_radius = 25
    p1_x, p1_y = 100, HEIGHT//2
    p2_x, p2_y = 150, HEIGHT//2
    speed = 4
    monster_size = 40
    monster_x = WIDTH - 100
    monster_y = random.randint(0, HEIGHT - monster_size)
    fruits = [(random.randint(100, 700), random.randint(100, 500)) for _ in range(fruit_count)]
    score = 0
    game_over = False
    level_complete = False

    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if level_complete and draw_button("Siguiente", 50, DARK_GREEN).collidepoint(mx, my):
                    return "next", score
                if game_over and draw_button("Reintentar", 50, DARK_RED).collidepoint(mx, my):
                    return "retry", score

        keys = pygame.key.get_pressed()
        if not level_complete and not game_over:
            # Movimiento jugador 1
            if keys[pygame.K_LEFT]: p1_x -= speed
            if keys[pygame.K_RIGHT]: p1_x += speed
            if keys[pygame.K_UP]: p1_y -= speed
            if keys[pygame.K_DOWN]: p1_y += speed
            # Movimiento jugador 2
            if keys[pygame.K_a]: p2_x -= speed
            if keys[pygame.K_d]: p2_x += speed
            if keys[pygame.K_w]: p2_y -= speed
            if keys[pygame.K_s]: p2_y += speed

            # Movimiento monstruo hacia jugador más cercano
            target_x, target_y = (p1_x, p1_y) if math.hypot(p1_x - monster_x, p1_y - monster_y) < math.hypot(p2_x - monster_x, p2_y - monster_y) else (p2_x, p2_y)
            dx, dy = target_x - monster_x, target_y - monster_y
            dist = math.hypot(dx, dy)
            if dist != 0:
                dx, dy = dx / dist, dy / dist
            monster_x += dx * monster_speed
            monster_y += dy * monster_speed

            # Colisión con monstruo
            if math.hypot(p1_x - monster_x, p1_y - monster_y) < player_radius + monster_size/2 or \
               math.hypot(p2_x - monster_x, p2_y - monster_y) < player_radius + monster_size/2:
                game_over = True
                save_highscore(score)

            # Recolectar frutas
            for fruit in fruits[:]:
                if any(math.hypot(px - fruit[0], py - fruit[1]) < player_radius + 12 for px, py in [(p1_x, p1_y), (p2_x, p2_y)]):
                    fruits.remove(fruit)
                    score += 10

            if not fruits:
                level_complete = True
                save_highscore(score)

        # Dibujitos
        draw_player(p1_x, p1_y, player_radius, RED)
        draw_player(p2_x, p2_y, player_radius, BLUE)
        draw_monster(monster_x, monster_y, monster_size)
        draw_fruits(fruits)

        # Puntaje
        score_text = FONT.render(f"Puntaje: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if level_complete:
            text = BIG_FONT.render(f"¡Nivel {level_number} Completado!", True, WHITE)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 60))
            draw_button("Siguiente", 50, DARK_GREEN)
        elif game_over:
            text = BIG_FONT.render("¡Han perdido!", True, RED)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 60))
            draw_button("Reintentar", 50, DARK_RED)

        pygame.display.flip()
        clock.tick(FPS)

def main_menu():
    while True:
        screen.fill(BLACK)
        title = BIG_FONT.render("BAD CIRCLES", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        btn1 = draw_button("Jugar", 0, DARK_GREEN)
        btn2 = draw_button("Instrucciones", 70, (50, 50, 150))
        btn3 = draw_button("Mejores Puntajes", 140, (150, 100, 0))
        btn4 = draw_button("Salir", 210, DARK_RED)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if btn1.collidepoint(mx, my): return
                elif btn2.collidepoint(mx, my): show_instructions()
                elif btn3.collidepoint(mx, my): show_highscores()
                elif btn4.collidepoint(mx, my): pygame.quit(); exit()

def main():
    # Mostrar Splash Screen
    mostrar_splash_screen()

    # mostrar el menú principal
    main_menu()

    # juego
    level = 1
    while True:
        result, score = run_level(level, 0.5 + level * 0.3, 3 + level * 2)
        if result == "next":
            level += 1
        elif result == "retry":
            continue

if __name__ == "__main__":
    main()

