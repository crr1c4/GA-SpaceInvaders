# TODO: PARA EL ALGORITMO GENETICO HABRA QUE REINICIAR EL JUEGO, ES DECIR SOLO TENDRA UNA VIDA
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
pygame.display.set_caption("Proyecto Algoritmos Genéticos - Invasores del Espacio.")

# Sirve para controlar el tiempo de actualización del renderizado del juego.
clock = pygame.time.Clock()

# Evento para el laser de los aliens, le dice a pygame el tiempo entre cada disparo (300 ms).
SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER, 300)

# Instancia del nucleo del juego.
game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)

while True:  # Loop principal del juego.
    for event in pygame.event.get():  # Manejo de eventos.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Checa el evento del disparo de alien. Tambien debe checar que no haya perdido.
        if event.type == SHOOT_LASER and game.run:
            game.alien_shoot_laser()

        # TODO: CAMBIAR ESTO AL IMPLEMENTAR EL ALGORITMO GENETICO.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and game.run == False:
            game.reset()

    # Actualizar las entidades del juego.
    # Checa si el juego termino:
    if game.run:
        game.spaceship_group.update()
        game.move_aliens()
        game.alien_lasers_group.update()
        game.check_for_collisions()

    # Dibuja las entidades.
    screen.fill(GREY)
    game.spaceship_group.draw(screen)
    game.spaceship_group.sprite.laser_group.draw(screen)
    game.aliens_group.draw(screen)
    game.alien_lasers_group.draw(screen)

    pygame.display.update()  # Actualiza las entidades del juego (graficos).
    _ = clock.tick(60)  # El juego ira a 60 fps.
