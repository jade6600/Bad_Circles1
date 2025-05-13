import pygame
import sys

# Colores
negro = (0, 0, 0)
blanco = (255, 255, 255)
cian = (0, 255, 255)
gris = (130, 131, 128)
gris_oscuro = (63, 63, 63)
amarillo = (240, 255, 0)
rojo = (194, 11, 11)
dorado = (213, 173, 25)
marron = (218, 113, 15)
azul = (2, 6, 149)
blanco = (255,255,255)
rosado = (255,192,203)
negro = (0,0,0)
rojo = (255,0,0)
gris_claro = (185, 185, 185)
gris_oscuro = (139, 139, 139)
gris_m_oscuro = (113, 112, 112)
gris_m_claro =  (217, 217, 217)
negro = (0,0,0)
rosado_c =(238, 156, 156)
piel = (255, 210, 132)
cafe = (156, 117, 50)
lila = (227, 156, 238)
morado = (193, 0, 222)

#Colores del tren

rojo_tren = (255, 0, 0)
cafe_tren = (207, 130, 43)
azul_tren = (47, 91, 239)
verde_tren = (20, 175, 67)

pygame.init()

ventana = pygame.display.set_mode((500, 500))
pygame.display.set_caption("tren")

clock = pygame.time.Clock()

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ventana.fill(azul)

    fuente_arial = pygame.font.SysFont("Arial", 30, 1, 1)
    texto = fuente_arial.render("Colegio San Jose de Guanenta", 1, blanco)
    ventana.blit(texto, (35, 30))

    fuente_arial = pygame.font.SysFont("Arial", 20, 1, 0)
    texto = fuente_arial.render("Especialidad Sistemas", 1, blanco)
    ventana.blit(texto, (150, 70))

    YY = 230
    MOVIMIENTO = 10

    YY = YY + MOVIMIENTO

    if YY >= 150:
        YY = 150
        MOVIMIENTO = -10
    elif YY <= 0:
        YY = 0
        MOVIMIENTO = 10

    # Humo
    pygame.draw.circle(ventana, blanco, (175, YY), 19, 0)


    #frente(ciculo)
    pygame.draw.circle(ventana, verde_tren, (135, 360), 50, 0)

    # Tren
    pygame.draw.rect(ventana, rojo_tren, ((150, 300), (250, 130)), 100)
    pygame.draw.rect(ventana, gris_oscuro, ((290, 200), (100, 80)), 0)
    pygame.draw.rect(ventana, azul_tren, ((270, 200), (130, 100)), 20)


    fuente_arial = pygame.font.SysFont("Arial", 20, 1, 0)
    texto = fuente_arial.render("Mariquitas", 1, negro)
    ventana.blit(texto, (180, 360))


    pygame.draw.rect(ventana,blanco, ((50,100), (400,390)), 1)

    #techo 
    pygame.draw.rect(ventana, verde_tren, ((260, 180), (150, 30)), 0)
    pygame.draw.rect(ventana, verde_tren, ((280, 150), (110, 30)), 0)

    #Frente

    pygame.draw.rect(ventana, negro, ((130, 310), (20, 110)), 0)
    pygame.draw.rect(ventana, negro, ((110, 300), (30, 130)), 0)

    #popa
    pygame.draw.rect(ventana, cafe_tren, ((155, 250), (40, 50)), 0)
    pygame.draw.rect(ventana, cafe_tren, ((140, 250), (70, 20)), 0)

    #llantas
    pygame.draw.circle(ventana, cafe_tren, (200, 440), 35, 0)
    pygame.draw.circle(ventana, cafe_tren, (280, 440), 35, 0)
    pygame.draw.circle(ventana, cafe_tren, (360, 440), 35, 0)

    pygame.draw.rect(ventana, negro, ((200, 430), (70, 20)), 0)
    pygame.draw.rect(ventana, negro, ((290, 430), (70, 20)), 0)

    # Personita
    pygame.draw.circle(ventana, amarillo, (335, 245), 35, 0)

    # Ojos
    pygame.draw.circle(ventana, blanco, (320, 240), 12, 0)
    pygame.draw.circle(ventana, blanco, (350, 240), 12, 0)

    # Pupilas
    pygame.draw.circle(ventana, marron, (350, 240), 6, 0)
    pygame.draw.circle(ventana, marron, (320, 240), 6, 0)

    # Boca
    pygame.draw.circle(ventana, rojo, (335, 260), 9, 0)

    # Cejas
    pygame.draw.line(ventana, marron, (320, 220), (330, 230), 3)
    pygame.draw.line(ventana, marron, (350, 220), (340, 230), 3)

    pygame.display.flip()


