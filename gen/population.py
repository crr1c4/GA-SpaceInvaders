from .individual import LEFT, RIGHT, SHOOT, Individual
import random


# Representación de una población.
class Population:
    # Los parametros iniciales que se le van a pasar son el tamaño de la población y el tamaño del cromosoma de cada individuo.
    def __init__(
        self, size_population: int, chromosome_size: int, generations: int = 50
    ):
        self.size: int = size_population
        self.chromosome_size: int = chromosome_size
        # Generar una población inicial (1ejecución del programa = 50 generaciones = 50 juegos con información de la población anterior)
        self.generations: int = generations
        # Número de generacion actual.
        self.actual_generation: int = 1
        # Asignación de los individuos de la población.
        self.individuals: list[Individual] = [
            Individual(self.chromosome_size) for _ in range(self.size)
        ]

    def select_parents_by_tournament(self, tournament_size=3) -> list[Individual]:
        selected_parents = []
        for _ in range(self.size):
            # Elige N individuos al azar para el torneo
            participants = random.sample(self.individuals, tournament_size)

            # Elige al ganador (el de MENOR fitness/distancia)
            winner = min(participants, key=lambda ind: ind.fitness)
            selected_parents.append(winner)
        return selected_parents

    def select_parents_by_elitism(self, elite_percentage=0.2) -> list[Individual]:
        # Ordena a todos los individuos por su fitness, de mejor a peor
        sorted_individuals = sorted(self.individuals, key=lambda ind: ind.fitness)

        # Calcula cuántos individuos forman la élite
        elite_count = int(self.size * elite_percentage)

        # Asegura que al menos haya 2 padres para poder cruzar
        elite_count = max(2, elite_count)

        # El pool de padres serán ÚNICAMENTE los mejores individuos
        parent_pool = sorted_individuals[:elite_count]

        return parent_pool

    # Se utiliza el punto sencilla, una parte del primer padre y otra del segundo padre.
    def crossover(
        self, parent1: Individual, parent2: Individual, rate=0.7
    ) -> tuple[list[int], list[int]]:
        cromo1 = parent1.chromosome
        cromo2 = parent2.chromosome

        if random.random() < rate:
            # Elige un punto de corte aleatorio
            cut_point = random.randint(1, self.chromosome_size - 1)

            # Crea los hijos
            child1_chromo = cromo1[:cut_point] + cromo2[cut_point:]
            child2_chromo = cromo2[:cut_point] + cromo1[cut_point:]

            return child1_chromo, child2_chromo
        else:
            # Si no hay cruce, los hijos son clones
            return cromo1, cromo2

    def mutate(self, chromosome: list[int], rate=0.01):
        if random.random() < rate:
            position = random.randrange(0, len(chromosome) - 1)
            action = chromosome[position]

            if action == LEFT:
                chromosome[position] = random.choice([RIGHT, SHOOT])
            elif action == RIGHT:
                chromosome[position] = random.choice([LEFT, SHOOT])
            elif action == SHOOT:
                chromosome[position] = random.choice([RIGHT, LEFT])

            print(
                f"Se presento una mutación en la posición {position}: {action} -> {chromosome[position]}"
            )

    # --- FIN AÑADIDO ---
