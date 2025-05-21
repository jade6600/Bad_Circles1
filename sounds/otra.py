import pygame
import random
import sys
import os

# pantallita
ANCHO, ALTO = 800, 600
FPS = 60
PUNTOS_PARA_NIVEL = 10
ARCHIVO_PUNTAJES = "mejores_puntajes.txt"

# iniciar 
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Bad Circles")
clock = pygame.time.Clock()
fuente_titulo = pygame.font.SysFont("arial", 40, True)
fuente_menu = pygame.font.SysFont("arial", 30)
fuente_info = pygame.font.SysFont("arial", 24)
fuente_next = pygame.font.SysFont("arial", 80, True)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# sonidos
sonido_puntos = pygame.mixer.Sound("sounds/puntos.mp3")
sonido_perdida = pygame.mixer.Sound("sounds/Partida_perdida.mp3")
sonido_ganada = pygame.mixer.Sound("sounds/Partida_ganada.mp3")
sonido_nuevo_nivel = pygame.mixer.Sound("sounds/nuevo_nivel.mp3")
musica_nivel1 = "sounds/Musica_nivel1.mp3"
musica_nivel2 = "sounds/Musica_nivel2.mp3"
musica_nivel3 = "sounds/Musica_nivel3.mp3"
musica_menu = "sounds/musica_menu.mp3"

# imagnes
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

# cositasss
SPLASH, MENU, INSTRUCCIONES, PUNTAJES, OPCIONES, JUEGO, GAME_OVER, NEXT_LEVEL_SCREEN = range(8)
estado = SPLASH

# variables que varian
vel_jugador = 5
vel_villano_base = 0.7
nivel = 0
puntaje_total = 0

# Jugadores 
jugador1 = pygame.Rect(100, 100, 40, 40)
jugador2 = pygame.Rect(600, 100, 40, 40)
villano = pygame.Rect(400, 300, 50, 50)

# Frutas
frutas = []

# jugadores vivos
jugador1_vivo = True
jugador2_vivo = True

# mensajitos temporales
mensaje_temp = ""
mensaje_timer = 0

# Bandera para música del menú
musica_menu_activa = False

# Variables para pantalla NEXT
mostrar_next = False
timer_next = 0
NEXT_DURACION = 1500  # milisegundos que se muestra NEXT

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

# un monton de funciones 

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
    pygame.mixer.music.stop()  # Detiene música del menú
    pygame.mixer.music.load(musica_nivel1)
    pygame.mixer.music.play(-1)

def generar_frutas():
    frutas.clear()
    for _ in range(15 + nivel*5):
        x = random.randint(30, ANCHO - 30)
        y = random.randint(100, ALTO - 30)
        frutas.append(pygame.Rect(x, y, 30, 30))

def avanzar_nivel():
    global nivel, vel_villano, mostrar_next, timer_next, estado
    nivel += 1
    vel_villano = vel_villano_base + nivel * 0.7
    generar_frutas()
    sonido_nuevo_nivel.play()

    # Música según nivel
    if nivel == 1:
        pygame.mixer.music.load(musica_nivel2)
        pygame.mixer.music.play(-1)
    elif nivel == 2:
        pygame.mixer.music.load(musica_nivel3)
        pygame.mixer.music.play(-1)

    # Mostrar pantalla NEXT antes de pasar al nivel
    mostrar_next = True
    timer_next = pygame.time.get_ticks()
    estado = NEXT_LEVEL_SCREEN

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
    # Elegir el jugador más cercano que esté vivo
    dist_j1 = (jugador1.centerx - villano.centerx)**2 + (jugador1.centery - villano.centery)**2 if jugador1_vivo else float('inf')
    dist_j2 = (jugador2.centerx - villano.centerx)**2 + (jugador2.centery - villano.centery)**2 if jugador2_vivo else float('inf')

    if dist_j1 < dist_j2:
        objetivo = jugador1
    else:
        objetivo = jugador2

    if villano.centerx < objetivo.centerx:
        villano.x += vel_villano
    if villano.centerx > objetivo.centerx:
        villano.x -= vel_villano
    if villano.centery < objetivo.centery:
        villano.y += vel_villano
    if villano.centery > objetivo.centery:
        villano.y -= vel_villano

def chequear_colisiones():
    global puntaje_total, jugador1_vivo, jugador2_vivo, estado, mensaje_temp, mensaje_timer
    # jugadores con frutas
    for fruta in frutas[:]:
        if jugador1.colliderect(fruta) and jugador1_vivo:
            frutas.remove(fruta)
            puntaje_total += 1
            sonido_puntos.play()
        elif jugador2.colliderect(fruta) and jugador2_vivo:
            frutas.remove(fruta)
            puntaje_total += 1
            sonido_puntos.play()

    # villano con frutas: elimina todas las frutas
    if villano.colliderect(jugador1) and jugador1_vivo:
        frutas.clear()
        jugador1_vivo = False
        mensaje_temp = "Jugador 1 eliminado!"
        mensaje_timer = pygame.time.get_ticks()
        sonido_perdida.play()

    if villano.colliderect(jugador2) and jugador2_vivo:
        frutas.clear()
        jugador2_vivo = False
        mensaje_temp = "Jugador 2 eliminado!"
        mensaje_timer = pygame.time.get_ticks()
        sonido_perdida.play()

    # si ambos muertos, game over
    if not jugador1_vivo and not jugador2_vivo:
        sonido_perdida.play()
        guardar_puntaje(puntaje_total)
        estado = GAME_OVER

def dibujar_juego():
    screen.blit(fondo_niveles[min(nivel, len(fondo_niveles)-1)], (0,0))
    # logos en pantalla de juego no se muestran según requerimiento
    # frutas
    for fruta in frutas:
        screen.blit(img_fruta, fruta.topleft)
    # villano
    screen.blit(img_villano, villano.topleft)
    # jugadores
    if jugador1_vivo:
        screen.blit(img_jugador1, jugador1.topleft)
    if jugador2_vivo:
        screen.blit(img_jugador2, jugador2.topleft)
    # puntaje
    txt_puntaje = fuente_info.render(f"Puntaje: {puntaje_total}", True, BLANCO)
    screen.blit(txt_puntaje, (10, 10))
    # mensajes temporales
    if mensaje_temp and pygame.time.get_ticks() - mensaje_timer < 2000:
        txt_msg = fuente_info.render(mensaje_temp, True, (255, 100, 100))
        screen.blit(txt_msg, (ANCHO//2 - txt_msg.get_width()//2, ALTO - 40))

def dibujar_splash():
    screen.fill(NEGRO)
    dibujar_texto_centrado(screen, "Bad Circles", fuente_titulo, BLANCO, 150)
    dibujar_texto_centrado(screen, "Soreth Florez, Nicolle Macias, Jorge Silva", fuente_info, BLANCO, 220)
    dibujar_texto_centrado(screen, "Especialidad de Sistemas", fuente_info, BLANCO, 260)
    dibujar_texto_centrado(screen, "Colegio San José de Guanentá", fuente_info, BLANCO, 300)
    # logos
    screen.blit(logo_colegio, (10, 10))
    screen.blit(logo_sistemas, (ANCHO - 90, 10))

def dibujar_menu():
    screen.fill((20, 20, 40))
    dibujar_texto_centrado(screen, "Bad Circles", fuente_titulo, BLANCO, 80)
    btn_instrucciones.dibujar(screen)
    btn_puntajes.dibujar(screen)
    btn_jugar.dibujar(screen)
    # logos en las esquinas
    screen.blit(logo_colegio, (10, 10))
    screen.blit(logo_sistemas, (ANCHO - 90, 10))

def dibujar_instrucciones():
    screen.fill((30, 30, 50))
    dibujar_texto_centrado(screen, "Instrucciones", fuente_titulo, BLANCO, 80)
    instrucciones = [
        "Jugador 1: usar flechas para moverse.",
        "Jugador 2: usar WASD para moverse.",
        "Recolecta frutas para sumar puntos.",
        "Evita que el villano te toque.",
        "Cuando recolectes suficientes frutas, avanzas de nivel.",
        "Si un jugador muere, el otro puede seguir.",
    ]
    y = 140
    for linea in instrucciones:
        txt = fuente_info.render(linea, True, BLANCO)
        screen.blit(txt, (50, y))
        y += 40
    btn_volver_menu.dibujar(screen)

def dibujar_puntajes():
    screen.fill((30, 30, 50))
    dibujar_texto_centrado(screen, "Mejores Puntajes", fuente_titulo, BLANCO, 80)
    puntajes = cargar_puntajes()
    puntajes.sort(reverse=True)
    y = 140
    for i, p in enumerate(puntajes[:10], 1):
        txt = fuente_info.render(f"{i}. {p}", True, BLANCO)
        screen.blit(txt, (ANCHO//2 - 50, y))
        y += 40
    btn_volver_menu.dibujar(screen)

def dibujar_game_over():
    screen.fill((50, 0, 0))
    dibujar_texto_centrado(screen, "GAME OVER", fuente_titulo, BLANCO, 150)
    dibujar_texto_centrado(screen, f"Puntaje Total: {puntaje_total}", fuente_info, BLANCO, 220)
    btn_reintentar.dibujar(screen)
    btn_volver_menu.dibujar(screen)

def dibujar_next_level():
    screen.fill(NEGRO)
    dibujar_texto_centrado(screen, "NEXT LEVEL", fuente_next, BLANCO, ALTO//2)

def main():
    global estado, puntaje_total, mostrar_next, timer_next

    running = True
    splash_timer = pygame.time.get_ticks()

    # Reproducir música menú al inicio (solo una vez)
    pygame.mixer.music.load(musica_menu)
    pygame.mixer.music.play(-1)

    while running:
        clock.tick(FPS)
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

            elif estado in (INSTRUCCIONES, PUNTAJES):
                if btn_volver_menu.clickeado(event):
                    estado = MENU

            elif estado == GAME_OVER:
                if btn_reintentar.clickeado(event):
                    reset_juego()
                    estado = JUEGO
                elif btn_volver_menu.clickeado(event):
                    estado = MENU

        teclas = pygame.key.get_pressed()

        if estado == SPLASH:
            dibujar_splash()
            # Mostrar splash 3 segundos
            if pygame.time.get_ticks() - splash_timer > 3000:
                estado = MENU

        elif estado == MENU:
            dibujar_menu()

        elif estado == INSTRUCCIONES:
            dibujar_instrucciones()

        elif estado == PUNTAJES:
            dibujar_puntajes()

        elif estado == JUEGO:
            # mover jugadores
            controles_j1 = {"izq":pygame.K_LEFT, "der":pygame.K_RIGHT, "arr":pygame.K_UP, "aba":pygame.K_DOWN}
            controles_j2 = {"izq":pygame.K_a, "der":pygame.K_d, "arr":pygame.K_w, "aba":pygame.K_s}

            mover_jugador(teclas, jugador1, controles_j1)
            mover_jugador(teclas, jugador2, controles_j2)
            mover_villano()
            chequear_colisiones()
            dibujar_juego()

            # Chequear si se pasa nivel
            if puntaje_total >= (nivel+1)*PUNTOS_PARA_NIVEL:
                avanzar_nivel()

        elif estado == GAME_OVER:
            dibujar_game_over()

        elif estado == NEXT_LEVEL_SCREEN:
            dibujar_next_level()
            if pygame.time.get_ticks() - timer_next > NEXT_DURACION:
                mostrar_next = False
                estado = JUEGO

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
