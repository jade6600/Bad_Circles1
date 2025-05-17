import pygame
import random
import sys
import os

# --- CONFIG ---
ANCHO, ALTO = 800, 600
FPS = 60
PUNTOS_PARA_NIVEL = 10
ARCHIVO_PUNTAJES = "mejores_puntajes.txt"

# --- INICIALIZACION ---
pygame.init()
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Bad Circles")
clock = pygame.time.Clock()
fuente_titulo = pygame.font.SysFont("arial", 40, True)
fuente_menu = pygame.font.SysFont("arial", 30)
fuente_info = pygame.font.SysFont("arial", 24)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# --- CARGAR IMAGENES ---
try:
    fondo_niveles = [pygame.transform.scale(pygame.image.load(f"img/fondo{i}.png"), (ANCHO, ALTO)) for i in range(1,4)]
    img_jugador1 = pygame.transform.scale(pygame.image.load("img/jugador1.png"), (40, 40))
    img_jugador2 = pygame.transform.scale(pygame.image.load("img/jugador2.png"), (40, 40))
    img_fruta = pygame.transform.scale(pygame.image.load("img/fruta.png"), (30, 30))
    img_villano = pygame.transform.scale(pygame.image.load("img/villano.png"), (50, 50))
    logo_colegio = pygame.transform.scale(pygame.image.load("img/logo_colegio.png"), (80, 80))
    logo_sistemas = pygame.transform.scale(pygame.image.load("img/logo_sistemas.png"), (80, 80))
except Exception as e:
    print("Error cargando imágenes:", e)
    pygame.quit()
    sys.exit()

# --- ESTADOS ---
SPLASH, MENU, INSTRUCCIONES, PUNTAJES, OPCIONES, JUEGO, GAME_OVER = range(7)
estado = SPLASH

# --- VARIABLES JUEGO ---
vel_jugador = 5
vel_villano_base = 0.7
nivel = 0
puntaje_total = 0

# Jugadores (Rect para posición y colisión)
jugador1 = pygame.Rect(100, 100, 40, 40)
jugador2 = pygame.Rect(600, 100, 40, 40)
villano = pygame.Rect(400, 300, 50, 50)

# Frutas
frutas = []

# Estados jugadores vivos
jugador1_vivo = True
jugador2_vivo = True

# Para mostrar mensajes temporales
mensaje_temp = ""
mensaje_timer = 0

# Botones del menú
class Boton:
    def __init__(self, texto, x, y, ancho=250, alto=50):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_base = (70,130,180)
        self.color_hover = (100,160,210)
    def dibujar(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.color_hover if self.rect.collidepoint(mouse_pos) else self.color_base
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        txt_surf = fuente_menu.render(self.texto, True, BLANCO)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surface.blit(txt_surf, txt_rect)
    def clickeado(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

btn_instrucciones = Boton("Instrucciones", ANCHO//2 - 125, 180)
btn_puntajes = Boton("Mejores Puntajes", ANCHO//2 - 125, 250)

btn_jugar = Boton("Jugar", ANCHO//2 - 125, 320)
btn_volver_menu = Boton("Volver al Menú", ANCHO//2 - 125, 520)
btn_reintentar = Boton("Volver a Intentar", ANCHO//2 - 125, 350)

# --- FUNCIONES ---

def cargar_puntajes():
    if not os.path.isfile(ARCHIVO_PUNTAJES):
        return []
    with open(ARCHIVO_PUNTAJES, "r") as f:
        lineas = f.readlines()
    puntajes = []
    for l in lineas:
        l = l.strip()
        if l.isdigit():
            puntajes.append(int(l))
    return puntajes

def guardar_puntaje(puntaje):
    with open(ARCHIVO_PUNTAJES, "a") as f:
        f.write(str(puntaje) + "\n")

def dibujar_texto_centrado(surface, texto, fuente, color, y):
    txt_surf = fuente.render(texto, True, color)
    txt_rect = txt_surf.get_rect(center=(ANCHO//2, y))
    surface.blit(txt_surf, txt_rect)

def reset_juego():
    global jugador1, jugador2, villano, frutas, nivel, puntaje_total, jugador1_vivo, jugador2_vivo, vel_villano
    jugador1.topleft = (100, 100)
    jugador2.topleft = (600, 100)
    villano.topleft = (ANCHO//2 - 25, ALTO//2 - 25)
    frutas.clear()
    nivel = 0
    puntaje_total = 0
    jugador1_vivo = True
    jugador2_vivo = True
    generar_frutas()
    vel_villano = vel_villano_base

def generar_frutas():
    frutas.clear()
    for _ in range(15 + nivel*5):  # más frutas cada nivel
        x = random.randint(30, ANCHO - 30)
        y = random.randint(100, ALTO - 30)
        frutas.append(pygame.Rect(x, y, 30, 30))

def avanzar_nivel():
    global nivel, vel_villano
    nivel += 1
    vel_villano = vel_villano_base + nivel * 0.7
    generar_frutas()

def mover_jugador(teclas, jugador_rect, controles):
    if not jugador1_vivo and jugador_rect == jugador1:
        return
    if not jugador2_vivo and jugador_rect == jugador2:
        return
    if teclas[controles["izq"]] and jugador_rect.left > 0:
        jugador_rect.x -= vel_jugador
    if teclas[controles["der"]] and jugador_rect.right < ANCHO:
        jugador_rect.x += vel_jugador
    if teclas[controles["arr"]] and jugador_rect.top > 0:
        jugador_rect.y -= vel_jugador
    if teclas[controles["aba"]] and jugador_rect.bottom < ALTO:
        jugador_rect.y += vel_jugador

def mover_villano():
    if not jugador1_vivo and not jugador2_vivo:
        return
    objetivo = None
    dist_j1 = (jugador1.centerx - villano.centerx)**2 + (jugador1.centery - villano.centery)**2 if jugador1_vivo else float('inf')
    dist_j2 = (jugador2.centerx - villano.centerx)**2 + (jugador2.centery - villano.centery)**2 if jugador2_vivo else float('inf')
    if dist_j1 < dist_j2:
        objetivo = jugador1 if jugador1_vivo else jugador2
    else:
        objetivo = jugador2 if jugador2_vivo else jugador1
    if villano.x < objetivo.x:
        villano.x += vel_villano
    if villano.x > objetivo.x:
        villano.x -= vel_villano
    if villano.y < objetivo.y:
        villano.y += vel_villano
    if villano.y > objetivo.y:
        villano.y -= vel_villano

def manejar_colisiones():
    global puntaje_total, jugador1_vivo, jugador2_vivo
    # Jugadores con frutas
    if jugador1_vivo:
        for f in frutas[:]:
            if jugador1.colliderect(f):
                frutas.remove(f)
                puntaje_total += 1
    if jugador2_vivo:
        for f in frutas[:]:
            if jugador2.colliderect(f):
                frutas.remove(f)
                puntaje_total += 1
    # Villano con jugadores
    if jugador1_vivo and villano.colliderect(jugador1):
        jugador1_vivo = False
    if jugador2_vivo and villano.colliderect(jugador2):
        jugador2_vivo = False

def dibujar_juego():
    screen.blit(fondo_niveles[nivel % len(fondo_niveles)], (0, 0))
    for f in frutas:
        screen.blit(img_fruta, f.topleft)
    if jugador1_vivo:
        screen.blit(img_jugador1, jugador1.topleft)
    if jugador2_vivo:
        screen.blit(img_jugador2, jugador2.topleft)
    screen.blit(img_villano, villano.topleft)
    texto = f"Puntaje Total: {puntaje_total}"
    txt_surf = fuente_menu.render(texto, True, BLANCO)
    screen.blit(txt_surf, (10, 10))

def dibujar_splash():
    screen.fill(NEGRO)
    dibujar_texto_centrado(screen, "Bad Circles", fuente_titulo, BLANCO, ALTO//2 - 100)
    dibujar_texto_centrado(screen, "Soreth Florez, Nicolle Macias, Jorge Silva", fuente_info, BLANCO, ALTO//2 - 50)
    dibujar_texto_centrado(screen, "Especialidad de Sistemas", fuente_info, BLANCO, ALTO//2 - 20)
    dibujar_texto_centrado(screen, "Colegio San José de Guanentá", fuente_info, BLANCO, ALTO//2 + 10)
    screen.blit(logo_colegio, (10, 10))
    screen.blit(logo_sistemas, (ANCHO - logo_sistemas.get_width() - 10, 10))

def dibujar_menu():
    screen.fill(NEGRO)
    dibujar_texto_centrado(screen, "Menú Principal", fuente_titulo, BLANCO, 100)
    btn_instrucciones.dibujar(screen)
    btn_puntajes.dibujar(screen)
   
    btn_jugar.dibujar(screen)
    screen.blit(logo_colegio, (10, 10))
    screen.blit(logo_sistemas, (ANCHO - logo_sistemas.get_width() - 10, 10))

def dibujar_instrucciones():
    screen.fill(NEGRO)
    dibujar_texto_centrado(screen, "Instrucciones", fuente_titulo, BLANCO, 80)
    lineas = [
        "Jugador 1: Flechas de dirección",
        "Jugador 2: Teclas W, A, S, D",
        "Recolecta frutas para sumar puntos.",
        "Evita al villano que te persigue.",
        "Al alcanzar puntos suficientes, avanzarás de nivel.",
        "Si un jugador es atrapado, el otro puede seguir.",
        "",
        "Presiona ESC para volver al menú."
    ]
    y = 150
    for linea in lineas:
        txt = fuente_info.render(linea, True, BLANCO)
        screen.blit(txt, (50, y))
        y += 30

def dibujar_puntajes():
    screen.fill(NEGRO)
    dibujar_texto_centrado(screen, "Mejores Puntajes", fuente_titulo, BLANCO, 80)
    puntajes = cargar_puntajes()
    puntajes = sorted(puntajes, reverse=True)[:10]
    y = 150
    if not puntajes:
        txt = fuente_info.render("No hay puntajes registrados.", True, BLANCO)
        screen.blit(txt, (ANCHO//2 - txt.get_width()//2, y))
    else:
        for i, p in enumerate(puntajes, start=1):
            texto = f"{i}. {p}"
            txt = fuente_info.render(texto, True, BLANCO)
            screen.blit(txt, (ANCHO//2 - txt.get_width()//2, y))
            y += 30
    btn_volver_menu.dibujar(screen)



def dibujar_game_over():
    screen.fill(NEGRO)
    dibujar_texto_centrado(screen, "Game Over", fuente_titulo, BLANCO, ALTO//2 - 100)
    texto = f"Puntaje Total: {puntaje_total}"
    dibujar_texto_centrado(screen, texto, fuente_menu, BLANCO, ALTO//2 - 50)
    btn_reintentar.dibujar(screen)
    btn_volver_menu.dibujar(screen)

# --- CONTROLES ---
controles_jugador1 = {"izq": pygame.K_LEFT, "der": pygame.K_RIGHT, "arr": pygame.K_UP, "aba": pygame.K_DOWN}
controles_jugador2 = {"izq": pygame.K_a, "der": pygame.K_d, "arr": pygame.K_w, "aba": pygame.K_s}

# --- VARIABLES DE VELOCIDAD ---
vel_villano = vel_villano_base

# --- TIEMPO PARA SPLASH ---
tiempo_splash = 3000
inicio_splash = pygame.time.get_ticks()

# --- BUCLE PRINCIPAL ---
running = True
while running:
    dt = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if estado == MENU:
            if btn_instrucciones.clickeado(event):
                estado = INSTRUCCIONES
            elif btn_puntajes.clickeado(event):
                estado = PUNTAJES
            
            elif btn_jugar.clickeado(event):
                reset_juego()
                estado = JUEGO

        elif estado in [INSTRUCCIONES, PUNTAJES, OPCIONES]:
            if btn_volver_menu.clickeado(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                estado = MENU

        elif estado == GAME_OVER:
            if btn_reintentar.clickeado(event):
                reset_juego()
                estado = JUEGO
            elif btn_volver_menu.clickeado(event):
                estado = MENU

        elif estado == JUEGO:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                estado = MENU

    teclas = pygame.key.get_pressed()

    if estado == SPLASH:
        dibujar_splash()
        if pygame.time.get_ticks() - inicio_splash > tiempo_splash:
            estado = MENU

    elif estado == MENU:
        dibujar_menu()

    elif estado == INSTRUCCIONES:
        dibujar_instrucciones()

    elif estado == PUNTAJES:
        dibujar_puntajes()

    elif estado == JUEGO:
        mover_jugador(teclas, jugador1, controles_jugador1)
        mover_jugador(teclas, jugador2, controles_jugador2)
        mover_villano()
        manejar_colisiones()
        dibujar_juego()

        if puntaje_total >= (nivel + 1) * PUNTOS_PARA_NIVEL:
            avanzar_nivel()

        if not jugador1_vivo and not jugador2_vivo:
            guardar_puntaje(puntaje_total)
            estado = GAME_OVER

    elif estado == GAME_OVER:
        dibujar_game_over()

    pygame.display.flip()

pygame.quit()
