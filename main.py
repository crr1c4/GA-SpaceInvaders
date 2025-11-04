import pygame
import sys

from game.spaceship import Spaceship

_ = pygame.init()

# Colores
GREY = (29, 29, 27)

# Dimensiones y configuracion de la ventana de la ventana.
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Proyecto Algoritmos Genéticos - Space Invaders")

# Sirve para controlar el tiempo de actualización del renderizado del juego.
clock = pygame.time.Clock()

# Entidades
spaceship = Spaceship(SCREEN_WIDTH, SCREEN_HEIGHT)

# Los grupos sirven para agrupar las entidades y poder renderizarlas mas facil.
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add(spaceship)


while True:  # Loop principal del juego.
    for event in pygame.event.get():  # Manejo de eventos.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Actualizando las entidades.
    spaceship_group.update()

    # Dibujos y coloreados.
    _ = screen.fill(GREY)
    _ = spaceship_group.draw(screen)

    pygame.display.update()  # Actualiza las entidades del juego (graficos).
    _ = clock.tick(60)  # El juego ira a 60 fps.
