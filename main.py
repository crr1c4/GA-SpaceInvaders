import pygame
import sys

from game.game import Game

pygame.init()

# Colores
GREY = (29, 29, 27)

# Dimensiones y configuracion de la ventana de la ventana.
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Proyecto Algoritmos Genéticos - Space Invaders")

# Sirve para controlar el tiempo de actualización del renderizado del juego.
clock = pygame.time.Clock()

# Instancia del nucleo del juego.
game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)

while True:  # Loop principal del juego.
    for event in pygame.event.get():  # Manejo de eventos.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Actualizar las entidades del juego.
    game.spaceship_group.update()

    # Dibujos y coloreados.
    screen.fill(GREY)
    game.spaceship_group.draw(screen)
    game.spaceship_group.sprite.laser_group.draw(screen)

    pygame.display.update()  # Actualiza las entidades del juego (graficos).
    _ = clock.tick(60)  # El juego ira a 60 fps.
