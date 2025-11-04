# TODO: PARA EL ALGORITMO GENETICO HABRA QUE REINICIAR EL JUEGO, ES DECIR SOLO TENDRA UNA VIDA
# TODO: CAMBIAR LA VELOCIDAD DE LOS LASERS
import pygame
import sys

from game.game import Game

pygame.init()

# Colores
GREY = (29, 29, 27)
YELLOW = (243, 216, 63)

# Fuente de la UI
font = pygame.font.Font("game/assets/monogram.ttf", 40)
level_surface = font.render("LEVEL 01", False, YELLOW)
game_over_surface = font.render("GAME OVER", False, YELLOW)
# Puntuación
score_text_surface = font.render("SCORE", False, YELLOW)
highscore_text_surface = font.render("HIGH-SCORE", False, YELLOW)

# Dimensiones y configuracion de la ventana de la ventana.
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700

# Espacio para colocar la UI
OFFSET = 50

screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2 * OFFSET))
pygame.display.set_caption("Proyecto Algoritmos Genéticos - Invasores del Espacio.")

# Sirve para controlar el tiempo de actualización del renderizado del juego.
clock = pygame.time.Clock()

# Evento para el laser de los aliens, le dice a pygame el tiempo entre cada disparo (300 ms).
SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER, 300)

# Instancia del nucleo del juego.
game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)

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
    # Los parametros no conocidos para el borde son:
    # La tupla es la posición del rect
    # 2 es la anchura del borde
    # 0 es para evitar que se rellene
    # Los 60s son los corner radius, para que se vea redondeado.
    pygame.draw.rect(screen, YELLOW, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
    # Linea para separar la UI:
    # La primera tupla es el punto inicial.
    # La segunda es el punto final.
    # 3 es el grosor de la linea.
    pygame.draw.line(screen, YELLOW, (20, 730), (775, 730), 3)

    # TODO: CAMBIAR ESTO A LA GENERACION DEL AG
    # Muestra el texto en la pantalla (UI)
    if game.run:
        screen.blit(level_surface, (570, 740, 50, 50))
    else:
        screen.blit(game_over_surface, (570, 740, 50, 50))

    # Sección de la UI que muestra la puntuación
    screen.blit(score_text_surface, (50, 15, 50, 50))
    formatted_score = str(game.score).zfill(5)
    score_surface = font.render(formatted_score, False, YELLOW)
    screen.blit(score_surface, (50, 40, 50, 50))
    screen.blit(highscore_text_surface, (600, 15, 50, 50))
    formatted_highscore = str(game.highscore).zfill(5)
    highscore_surface = font.render(formatted_highscore, False, YELLOW)
    screen.blit(highscore_surface, (675, 40, 50, 50))

    game.spaceship_group.draw(screen)
    game.spaceship_group.sprite.laser_group.draw(screen)
    game.aliens_group.draw(screen)
    game.alien_lasers_group.draw(screen)

    pygame.display.update()  # Actualiza las entidades del juego (graficos).
    _ = clock.tick(60)  # El juego ira a 60 fps.
