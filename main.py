# TODO: PARA EL ALGORITMO GENETICO HABRA QUE REINICIAR EL JUEGO, ES DECIR SOLO TENDRA UNA VIDA
import pygame
import sys
import random

from game.game import Game
from gen.individual import LEFT, RIGHT, SHOOT, Individual
from gen.population import Population


############### ALGORITMO GENÉTICO ***************
# FASES DEL ALGORITMO GENÉTICO.
# 1. Calcular la adaptación
# 2. Seleccionar a los padres
# 3. Crossover y mutación
# 4. Regresa al paso 1

CHROMOSOME_SIZE = 100
POPULATION_SIZE = 25
GENERATIONS = 50

# Población inicial (generación 0)
population = Population(POPULATION_SIZE, CHROMOSOME_SIZE, GENERATIONS)

# for individual in population.individuals:
#     print(individual.chromosome)


############### JUEGO ***************
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

# while True:  # Loop principal del juego.
# Ciclo para cada generación.
for generation in range(population.generations):
    print(f"--- Iniciando Generación {generation + 1} / {population.generations} ---")

    # 1. Calcular la adaptación, realizar la ejecucion del juego para cada individuo.
    for i, individual in enumerate(population.individuals):
        game.reset()  # Reinicia los elementos del juego.

        # Itera sobre cada uno de las acciones del cromosoma.
        for action in individual.chromosome:
            for event in pygame.event.get():  # Manejo de eventos.
                # Verifica si el usuario cerro la ventana.
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
            game.move_alien()
            game.alien_laser.update()
            game.alien_shoot_laser()

            # Cálculo del fitness
            game.calculate_fitness_step()

            game.check_for_collisions()

            # Dibuja las entidades.
            _ = screen.fill(GREY)
            draw_grid()
            game.spaceship.draw(screen)
            game.spaceship.sprite.laser.draw(screen)  # CHECAR .laser
            game.alien.draw(screen)
            game.alien_laser.draw(screen)

            pygame.display.update()
            _ = clock.tick(clock_speed)

        # Se guarda el fitness en el individuo
        individual.fitness = game.fitness

        # Si el alien sigue vivo, el fitness es mucho peor
        if game.alien.sprite:
            individual.fitness += 100_000  # "Castigo" por no matar al alien

    # Ahora se busca al mejor individuo
    best = min(population.individuals, key=lambda individual: individual.fitness)
    print(f"Mejor fitness de la generacion (Menor): {best.fitness}")

    # 2. Seleccion de los padres.
    parents = population.select_parents_by_tournament()

    # 3. Crossover y mutación.
    new_generation = []

    while len(new_generation) < population.size:
        # Eleccion de los 2 padres.
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)

        # Creación de los hijos.
        child1_chromosome, child2_chromosome = population.crossover(parent1, parent2)

        # Mutacíon de los hijos.
        population.mutate(child1_chromosome)
        population.mutate(child2_chromosome)

        # Se añaden a la generación.
        new_generation.append(
            Individual(population.chromosome_size).set_chromosome(child1_chromosome)
        )
        if len(new_generation) < population.size:
            new_generation.append(
                Individual(population.chromosome_size).set_chromosome(child2_chromosome)
            )

    # Reemplaza la población antigua por la nueva
    population.individuals = new_generation
    population.actual_generation += 1

print("Algoritmo genético completado")
pygame.quit()
sys.exit()
