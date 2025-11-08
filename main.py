################ ALGORITMO GENÉTICO #################

# 1. Calcular la adaptación
# 2. Seleccionar a los padres
# 3. Crossover y mutación
# 4. Regresa al paso 1

import pygame
import sys
import numpy as np

from game.game import Game
from gen.population import Population, LEFT, RIGHT, SHOOT
from ui.manager import UIManager
from utils import (
    CELL_SIZE,
    COLUMNS,
    LIGHT_GREY,
    ROWS,
    load_population,
    save_population,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    GREY,
    POPULATION_SIZE,
    CHROMOSOME_SIZE,
    GENERATIONS,
)

# Población inicial (generación 0)
population = load_population()

if population is None:
    population = Population(POPULATION_SIZE, CHROMOSOME_SIZE, GENERATIONS)

pygame.init()

font = pygame.font.Font("game/assets/monogram.ttf", 40)
ui_manager = UIManager(font)


screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    # pygame.RESIZABLE,
)

pygame.display.set_caption("Proyecto Algoritmos Genéticos - Invasores del Espacio.")


# Función para dibujar la cuadricula
def draw_grid():
    for x in range(0, ROWS * CELL_SIZE, CELL_SIZE):
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            _ = pygame.draw.rect(screen, LIGHT_GREY, rect, 1)


clock_speed = 10
clock = pygame.time.Clock()


# Instancia del nucleo del juego.
game = Game(CELL_SIZE, ROWS, COLUMNS)

# Ciclo para cada generación.
for generation in range(population.generations):
    #     print(f"\n{'=' * 60}")
    #     print(f"  GENERACIÓN {generation + 1} / {GENERATIONS}")
    #     print(f"{'=' * 60}\n")
    # Contadores de victorias y derrotas para la gráfica de esta generación

    current_gen_wins = 0
    current_gen_losses = 0

    # 1. Calcular la adaptación, realizar la ejecucion del juego para cada individuo.
    for index in range(population.size):
        game.reset()  # Reinicia los elementos del juego.

        # Obtención del cromosoma del individuo.
        chromosome = population.get_chromosome(index)

        # Itera sobre cada uno de las acciones del cromosoma.
        for action_index, action in enumerate(chromosome):
            # Manejo de eventos.
            for event in pygame.event.get():
                # Verifica si el usuario cerro la ventana.
                if event.type == pygame.QUIT:
                    save_population(population)
                    pygame.quit()
                    sys.exit()

                # Cambia la velocidad del jeugo
                keys = pygame.key.get_pressed()
                if keys[pygame.K_PLUS] and game.run and clock_speed < 120:
                    clock_speed += 10

                elif keys[pygame.K_MINUS] and game.run and clock_speed > 10:
                    clock_speed -= 10

            # Actualizar las entidades del juego.
            # Checa si el juego termino: Continua con el siguiente individuo
            if not game.run:
                break

            # Ejecución de la accion.
            if action == LEFT:
                game.spaceship.sprite.move_left()
            elif action == RIGHT:
                game.spaceship.sprite.move_right()
            elif action == SHOOT:
                game.spaceship.sprite.shoot()

            # Actualizacion de los estados de los sprites del juego
            game.spaceship.update()
            game.spaceship.sprite.laser.update()
            game.move_alien()
            game.alien_laser.update()
            game.alien_shoot_laser()

            # 🧮 Cálculo de la adaptación (fitness)
            game.calculate_fitness_step(action)
            game.check_for_collisions()

            # Dibuja las entidades.
            screen.fill(GREY)
            draw_grid()

            ui_manager.draw(screen, population, generation + 1, index + 1)

            game.spaceship.draw(screen)
            game.spaceship.sprite.laser.draw(screen)
            game.alien.draw(screen)
            game.alien_laser.draw(screen)

            pygame.display.update()
            clock.tick(clock_speed)

        # Penalizacion por timeout
        if game.run and not game.victory:
            game.fitness += 50_000
            current_gen_losses += 1

        # Actualizar el contador de victorias y derrotas.
        if game.victory:
            current_gen_wins += 1
        elif game.defeat:
            current_gen_losses += 1

        population.set_fitness(index, game.fitness)

    best_fitness_index = np.argmin(population.fitness)
    best_fitness = population.fitness[best_fitness_index]

    ui_manager.update_generation_stats(
        best_fitness, current_gen_wins, current_gen_losses
    )
    # 2. Seleccion de los padres.
    # 3. Crossover y mutación.
    population.evolve()
    save_population(population)

print("Algoritmo genético completado")
pygame.quit()
sys.exit()
