import pygame
import random

pygame.init()

# --- Constantes ---
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Bad Circles")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (30, 30, 200)
AMARILLO = (255, 255, 0)

# Fuentes
BIG_FONT = pygame.font.Font(None, 56)
FONT = pygame.font.Font(None, 32)

clock = pygame.time.Clock()

# --- Carga imágenes ---
jugador_rojo_img = pygame.image.load("img/jugador1.png").convert_alpha()
jugador_rojo_img = pygame.transform.scale(jugador_rojo_img, (50, 50))
jugador_azul_img = pygame.image.load("img/jugador2.png").convert_alpha()
jugador_azul_img = pygame.transform.scale(jugador_azul_img, (50, 50))
villano_img = pygame.image.load("img/villano.png").convert_alpha()
villano_img = pygame.transform.scale(villano_img, (60, 60))
fruta_img = pygame.image.load("img/fruta.png").convert_alpha()
fruta_img = pygame.transform.scale(fruta_img, (30, 30))
fondo_img = pygame.image.load("img/fondo.png").convert()
fondo_img = pygame.transform.scale(fondo_img, (ANCHO, ALTO))

logo_colegio = pygame.image.load("img/logo_colegio.png").convert_alpha()
logo_colegio = pygame.transform.scale(logo_colegio, (80, 40))
logo_sistemas = pygame.image.load("img/logo_sistemas.png").convert_alpha()
logo_sistemas = pygame.transform.scale(logo_sistemas, (80, 40))

# --- Funciones ---
def mostrar_splash_screen():
    tiempo_inicio = pygame.time.get_ticks()
    while pygame.time.get_ticks() - tiempo_inicio < 4000:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        pantalla.fill(AZUL)
        pantalla.blit(logo_colegio, (5, 5))
        pantalla.blit(logo_sistemas, (ANCHO - logo_sistemas.get_width() - 5, 5))

        titulo = BIG_FONT.render("Bad Circles", True, BLANCO)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, ALTO//2 - 80))

        creditos = FONT.render("Sorteh Jhull Florez Peñaloza, Nicolle Daniela Macias Piracon y Jorge Luis Silva Morales", True, AMARILLO)
        pantalla.blit(creditos, (ANCHO//2 - creditos.get_width()//2, ALTO//2))

        pygame.display.flip()
        clock.tick(60)

def mostrar_menu_principal():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return

        pantalla.fill(AZUL)
        titulo = BIG_FONT.render("Bad Circles", True, BLANCO)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 100))

        instrucciones = [
            "Instrucciones:",
            "- Jugador 1: usa WASD para moverse",
            "- Jugador 2: usa flechas para moverse",
            "- Recoge frutas para ganar puntos",
            "- Evita al villano que persigue",
            "- Al recolectar 30 frutas, subes de nivel",
            "",
            "Presiona ENTER para seleccionar personajes"
        ]

        for i, linea in enumerate(instrucciones):
            texto = FONT.render(linea, True, BLANCO)
            pantalla.blit(texto, (50, 180 + i * 30))

        pygame.display.flip()
        clock.tick(60)

def character_selection_menu():
    selected_p1 = None
    selected_p2 = None
    options = ["Rojo", "Azul"]
    while selected_p1 is None or selected_p2 is None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for i, opt in enumerate(options):
                    rect1 = pygame.Rect(150, 150 + i * 100, 200, 60)
                    rect2 = pygame.Rect(450, 150 + i * 100, 200, 60)
                    if rect1.collidepoint(mx, my):
                        selected_p1 = opt
                    elif rect2.collidepoint(mx, my):
                        selected_p2 = opt

        pantalla.fill(NEGRO)
        title = BIG_FONT.render("Selecciona tu personaje", True, BLANCO)
        pantalla.blit(title, (ANCHO//2 - title.get_width()//2, 40))

        for i, opt in enumerate(options):
            color = (200, 30, 30) if opt == "Rojo" else (30, 30, 200)
            label1 = FONT.render(f"Jugador 1: {opt}", True, BLANCO)
            label2 = FONT.render(f"Jugador 2: {opt}", True, BLANCO)
            rect1 = pygame.Rect(150, 150 + i * 100, 200, 60)
            rect2 = pygame.Rect(450, 150 + i * 100, 200, 60)
            pygame.draw.rect(pantalla, color, rect1, border_radius=10)
            pygame.draw.rect(pantalla, color, rect2, border_radius=10)
            pantalla.blit(label1, (rect1.x + 20, rect1.y + 15))
            pantalla.blit(label2, (rect2.x + 20, rect2.y + 15))
            if selected_p1 == opt:
                pygame.draw.rect(pantalla, BLANCO, rect1, 4)
            if selected_p2 == opt:
                pygame.draw.rect(pantalla, BLANCO, rect2, 4)

        pygame.display.flip()
        clock.tick(60)

    return selected_p1, selected_p2

def juego(p1, p2):
    img_j1 = jugador_rojo_img if p1 == "Rojo" else jugador_azul_img
    img_j2 = jugador_rojo_img if p2 == "Rojo" else jugador_azul_img

    jugador1_x, jugador1_y = 100, 100
    jugador2_x, jugador2_y = 200, 100
    villano_x, villano_y = 400, 300

    jugador1_vivo = True
    jugador2_vivo = True

    score = 0
    frutas_recolectadas = 0
    nivel = 1

    frutas = []
    def generar_frutas():
        for _ in range(5 + nivel):
            frutas.append([random.randint(50, ANCHO - 50), random.randint(50, ALTO - 50)])

    generar_frutas()

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if jugador1_vivo:
            if keys[pygame.K_a]: jugador1_x -= 5
            if keys[pygame.K_d]: jugador1_x += 5
            if keys[pygame.K_w]: jugador1_y -= 5
            if keys[pygame.K_s]: jugador1_y += 5
        if jugador2_vivo:
            if keys[pygame.K_LEFT]: jugador2_x -= 5
            if keys[pygame.K_RIGHT]: jugador2_x += 5
            if keys[pygame.K_UP]: jugador2_y -= 5
            if keys[pygame.K_DOWN]: jugador2_y += 5

        jugador1_x = max(0, min(ANCHO - img_j1.get_width(), jugador1_x))
        jugador1_y = max(0, min(ALTO - img_j1.get_height(), jugador1_y))
        jugador2_x = max(0, min(ANCHO - img_j2.get_width(), jugador2_x))
        jugador2_y = max(0, min(ALTO - img_j2.get_height(), jugador2_y))

        objetivo = None
        if jugador1_vivo and jugador2_vivo:
            dist1 = abs(villano_x - jugador1_x) + abs(villano_y - jugador1_y)
            dist2 = abs(villano_x - jugador2_x) + abs(villano_y - jugador2_y)
            objetivo = (jugador1_x, jugador1_y) if dist1 < dist2 else (jugador2_x, jugador2_y)
        elif jugador1_vivo:
            objetivo = (jugador1_x, jugador1_y)
        elif jugador2_vivo:
            objetivo = (jugador2_x, jugador2_y)
        else:
            corriendo = False
            break

        dx = objetivo[0] - villano_x
        dy = objetivo[1] - villano_y
        dist = max(1, (dx**2 + dy**2) ** 0.5)
        villano_x += dx / dist * nivel * 0.4
        villano_y += dy / dist * nivel * 0.4

        rect_j1 = pygame.Rect(jugador1_x, jugador1_y, img_j1.get_width(), img_j1.get_height())
        rect_j2 = pygame.Rect(jugador2_x, jugador2_y, img_j2.get_width(), img_j2.get_height())
        rect_v = pygame.Rect(villano_x, villano_y, villano_img.get_width(), villano_img.get_height())

        frutas_para_borrar = []
        for i, (fx, fy) in enumerate(frutas):
            rect_f = pygame.Rect(fx, fy, fruta_img.get_width(), fruta_img.get_height())
            if jugador1_vivo and rect_j1.colliderect(rect_f):
                frutas_para_borrar.append(i)
                score += 1
                frutas_recolectadas += 1
            elif jugador2_vivo and rect_j2.colliderect(rect_f):
                frutas_para_borrar.append(i)
                score += 1
                frutas_recolectadas += 1

        for i in reversed(frutas_para_borrar):
            frutas.pop(i)

        if frutas_recolectadas >= 30:
            nivel += 1
            frutas_recolectadas = 0
            generar_frutas()

        if rect_j1.colliderect(rect_v): jugador1_vivo = False
        if rect_j2.colliderect(rect_v): jugador2_vivo = False

        pantalla.blit(fondo_img, (0, 0))
        for (fx, fy) in frutas:
            pantalla.blit(fruta_img, (fx, fy))
        if jugador1_vivo:
            pantalla.blit(img_j1, (jugador1_x, jugador1_y))
        if jugador2_vivo:
            pantalla.blit(img_j2, (jugador2_x, jugador2_y))
        pantalla.blit(villano_img, (villano_x, villano_y))
        pantalla.blit(FONT.render(f"Puntaje: {score}", True, BLANCO), (10, ALTO - 40))
        pantalla.blit(FONT.render(f"Nivel: {nivel}", True, BLANCO), (ANCHO - 120, ALTO - 40))

        pygame.display.flip()
        clock.tick(60)

    tiempo_fin = pygame.time.get_ticks()
    while pygame.time.get_ticks() - tiempo_fin < 4000:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
        pantalla.fill(NEGRO)
        texto_fin = BIG_FONT.render(f"Juego Terminado! Puntaje Final: {score}", True, BLANCO)
        pantalla.blit(texto_fin, (ANCHO//2 - texto_fin.get_width()//2, ALTO//2 - texto_fin.get_height()//2))
        pygame.display.flip()
        clock.tick(60)

def main():
    mostrar_splash_screen()
    mostrar_menu_principal()
    p1, p2 = character_selection_menu()
    juego(p1, p2)
    pygame.quit()

if __name__ == "__main__":
    main()