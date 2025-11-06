# TODO: PARA EL ALGORITMO GENETICO HABRA QUE REINICIAR EL JUEGO, ES DECIR SOLO TENDRA UNA VIDA
import pygame
import sys

from game.game import Game

_ = pygame.init()

# Colores
GREY = (29, 29, 27)
LIGHT_GREY = (40, 40, 36)
# LIGHT_GREY = (255, 255, 255)
YELLOW = (243, 216, 63)

# Cuadricula del GRID
ROWS, COLUMNS = 20, 15
CELL_SIZE = 50

# Dimensiones y configuracion de la ventana de la ventana.
SCREEN_WIDTH = ROWS * CELL_SIZE
SCREEN_HEIGHT = COLUMNS * CELL_SIZE

# Espacio para la información del algoritmo genetico.
GA_SCREEN_WIDTH = 500

# Espacio para colocar la UI
OFFSET = 0

screen = pygame.display.set_mode(
    # (SCREEN_WIDTH + OFFSET + GA_SCREEN_WIDTH, SCREEN_HEIGHT + 2 * OFFSET),
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    pygame.RESIZABLE,
)
pygame.display.set_caption("Proyecto Algoritmos Genéticos - Invasores del Espacio.")


# Función para dibujar la cuadricula
def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            _ = pygame.draw.rect(screen, LIGHT_GREY, rect, 1)


# Sirve para controlar el tiempo de actualización del renderizado del juego.
clock_speed = 5
clock = pygame.time.Clock()


# Instancia del nucleo del juego.
# game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET, CELL_SIZE)
game = Game(CELL_SIZE, ROWS, COLUMNS)

while True:  # Loop principal del juego.
    for event in pygame.event.get():  # Manejo de eventos.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Cambia la velocidad del jeugo
        keys = pygame.key.get_pressed()
        if keys[pygame.K_PLUS] and game.run:
            clock_speed += 5

        elif keys[pygame.K_MINUS] and game.run and clock_speed > 5:
            clock_speed -= 5

    # Actualizar las entidades del juego.
    # Checa si el juego termino:
    if game.run:
        game.spaceship.update()
        game.move_alien()
        game.alien_laser.update()
        game.alien_shoot_laser()
        game.check_for_collisions()

    # Dibuja las entidades.
    _ = screen.fill(GREY)
    draw_grid()

    game.spaceship.draw(screen)
    game.spaceship.sprite.laser.draw(screen)
    game.alien.draw(screen)
    game.alien_laser.draw(screen)

    pygame.display.update()
    _ = clock.tick(clock_speed)

# Fuente de la UI
# font = pygame.font.Font("game/assets/monogram.ttf", 40)
# level_surface = font.render("LEVEL 01", False, YELLOW)
# game_over_surface = font.render("GAME OVER", False, YELLOW)
# # Puntuación
# score_text_surface = font.render("SCORE", False, YELLOW)
# highscore_text_surface = font.render("HIGH-SCORE", False, YELLOW)
