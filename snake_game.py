import pygame
import random
import sys
import os

def ruta_absoluta(relativa):
    """Devuelve la ruta absoluta del archivo, compatible con PyInstaller"""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relativa)


# Inicializar pygame
pygame.init()
pygame.mixer.init()

# sonidos
sonido_comer = pygame.mixer.Sound(ruta_absoluta("sounds/eat.wav"))
sonido_perder = pygame.mixer.Sound(ruta_absoluta("sounds/gameover.wav"))
pygame.mixer.music.load(ruta_absoluta("sounds/menu.mp3"))

# Tamaño de pantalla y bloques
ANCHO, ALTO = 600, 400
bloque = 20
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Snake 🐍 by Robinson David")

# Colores
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)

# Fuente y reloj
fuente = pygame.font.SysFont("Arial", 24)
titulo = pygame.font.SysFont("Arial", 36, bold=True)
reloj = pygame.time.Clock()
velocidad = 10

def mostrar_puntaje(puntaje):
    texto = fuente.render(f"Puntaje: {puntaje}", True, VERDE)
    pantalla.blit(texto, [10, 10])

def mostrar_mensaje(texto):
    mensaje = fuente.render(texto, True, ROJO)
    pantalla.blit(mensaje, [ANCHO // 4, ALTO // 2])
    pygame.display.flip()
    pygame.time.wait(2000)

##Generar Comida
def generar_comida(serpiente):
    while True:
        x = random.randint(0, (ANCHO - bloque) // bloque) * bloque
        y = random.randint(0, (ALTO - bloque) // bloque) * bloque
        if [x, y] not in serpiente:
            return [x, y]
        

#Menu Inicio     
def menu_inicio():
    # Reproducir música del menú
    pygame.mixer.music.load(ruta_absoluta("sounds/menu.mp3"))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Repetir en bucle
    esperando = True

    while esperando:
        pantalla.fill(NEGRO)
        texto_titulo = titulo.render("Snake 🐍", True, VERDE)
        texto_inicio = fuente.render("Presiona ESPACIO para jugar", True, BLANCO)
        texto_controles = fuente.render("Usa las flechas para moverte", True, BLANCO)

        pantalla.blit(texto_titulo, [ANCHO // 2 - 80, ALTO // 3])
        pantalla.blit(texto_inicio, [ANCHO // 2 - 140, ALTO // 2])
        pantalla.blit(texto_controles, [ANCHO // 2 - 150, ALTO // 2 + 40])

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pygame.mixer.music.stop() # Detiene música del menú al comenzar el juego
                    esperando = False
#Juego   
def juego():
    serpiente = [[100, 100], [80, 100], [60, 100]]
    direccion = "DERECHA"
    comida = generar_comida(serpiente)
    puntaje = 0
    en_juego = True

    while en_juego:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP and direccion != "ABAJO":
                    direccion = "ARRIBA"
                elif evento.key == pygame.K_DOWN and direccion != "ARRIBA":
                    direccion = "ABAJO"
                elif evento.key == pygame.K_LEFT and direccion != "DERECHA":
                    direccion = "IZQUIERDA"
                elif evento.key == pygame.K_RIGHT and direccion != "IZQUIERDA":
                    direccion = "DERECHA"

        # Mover la cabeza
        cabeza = list(serpiente[0])
        if direccion == "ARRIBA":
            cabeza[1] -= bloque
        elif direccion == "ABAJO":
            cabeza[1] += bloque
        elif direccion == "IZQUIERDA":
            cabeza[0] -= bloque
        elif direccion == "DERECHA":
            cabeza[0] += bloque
        serpiente.insert(0, cabeza)

        # Colisiones con sí misma o bordes
        if (
            cabeza in serpiente[1:] or
            cabeza[0] < 0 or cabeza[0] >= ANCHO or
            cabeza[1] < 0 or cabeza[1] >= ALTO
        ):
            sonido_perder.play()
            mostrar_mensaje(f"Perdiste. Puntaje: {puntaje}")
            return

        # Verificar si comió la comida (comparación exacta)
        if cabeza[0] == comida[0] and cabeza[1] == comida[1]:
            puntaje += 1
            comida = generar_comida(serpiente)
            sonido_comer.play()
        else:
            serpiente.pop()  # No comió: se mueve normal

        # Dibujar
        pantalla.fill(NEGRO)
        for segmento in serpiente:
            pygame.draw.rect(pantalla, VERDE, pygame.Rect(segmento[0], segmento[1], bloque, bloque))
        pygame.draw.rect(pantalla, ROJO, pygame.Rect(comida[0], comida[1], bloque, bloque))
        mostrar_puntaje(puntaje)

        pygame.display.flip()
        reloj.tick(velocidad)

# Loop del juego
while True:
    menu_inicio()
    juego()
