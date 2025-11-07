import numpy as np
from numpy.typing import NDArray
import random


# Valores que puede tomar del cromosoma.
LEFT = 1
RIGHT = 2
SHOOT = 3


# Representación de una población.
class Population:
    # Los parametros iniciales que se le van a pasar son el tamaño de la población y el tamaño del cromosoma de cada individuo.
    def __init__(
        self,
        size: int,
        chromosome_size: int,
        generations: int = 50,
        mutation_rate: float = 0.01,
        elite_percentage: float = 0.10,
    ):
        # Tamaño de la población.
        self.size: int = size
        self.chromosome_size: int = chromosome_size
        # Generar una población inicial (1ejecución del programa = 50 generaciones = 50 juegos con información de la población anterior)
        self.generations: int = generations
        # Asignación de los individuos de la población.
        # La primera dimensión es el número de individuo.
        # La segunda dimensión es el número de cromosoma.
        self.population: NDArray[np.uint8] = np.random.default_rng().integers(
            low=1, high=4, size=(self.size, self.chromosome_size), dtype=np.uint8
        )

        # Arreglo para guardar el fitness de los individuos.
        self.fitness: NDArray[np.float64] = np.full(self.size, np.inf, dtype=np.float64)

        # Probabilidad de mutación.
        self.mutation_rate = mutation_rate
        self.elite_percentage = elite_percentage

    def set_fitness(self, index: int, fitness_value):
        self.fitness[index] = fitness_value

    def get_chromosome(self, index: int) -> NDArray[np.uint8]:
        return self.population[index]

    def select_parents_by_elitism(self) -> NDArray[np.uint8]:
        # Obtiene la cantidad de individuos que van a formar parte de la elite.
        elite_count = max(2, int(self.size * self.elite_percentage))

        # Obtener los índices ordenados por fitness (ascendente).
        sorted_indices = np.argsort(self.fitness)

        # Seleccionar los indices de la población.
        elite_indices = sorted_indices[:elite_count]

        # Retornar los cromosomas de la élite.
        return self.population[elite_indices]

    # Se utiliza el punto sencillo, una parte del primer padre y otra del segundo padre.
    # rate es la probablidad de que haya un cruce
    def crossover(
        self, parent1: NDArray[np.uint8], parent2: NDArray[np.uint8], rate: float = 0.7
    ) -> tuple[NDArray[np.uint8], NDArray[np.uint8]]:
        if random.random() < rate:
            # Elige un punto de corte aleatorio
            cut_point = random.randint(1, self.chromosome_size - 1)

            # Mezcla de los padres.
            child1 = np.concatenate([parent1[:cut_point], parent2[cut_point:]])
            child2 = np.concatenate([parent2[:cut_point], parent1[cut_point:]])

            return child1, child2
        else:
            # Si no hay cruce, los hijos son clones
            return parent1.copy(), parent2.copy()

    # Mutación, se le pasa un cromosoma y se va recorriendo, la posibilidad de mutacion se del 1%
    def mutate(self, chromosome: NDArray[np.uint8]):
        for i in range(self.chromosome_size):
            if random.random() < self.mutation_rate:
                # Gen actual
                current_action = chromosome[i]

                if current_action == LEFT:
                    chromosome[i] = random.choice([RIGHT, SHOOT])
                elif current_action == RIGHT:
                    chromosome[i] = random.choice([LEFT, SHOOT])
                elif current_action == SHOOT:
                    chromosome[i] = random.choice([LEFT, RIGHT])

    # Evoluciona a la población.
    def evolve(self):
        elite_chromosomes = self.select_parents_by_elitism()
        elite_count = len(elite_chromosomes)
        new_population = []

        for elite_chromosome in elite_chromosomes:
            new_population.append(elite_chromosome.copy())

        # Generar el resto de la poblacion mediante cruce y mutación
        while len(new_population) < self.size:
            # Seleccionar dos padres de la élite (al azar)
            parent1 = elite_chromosomes[random.randint(0, elite_count - 1)]
            parent2 = elite_chromosomes[random.randint(0, elite_count - 1)]

            # Crossover
            child1, child2 = self.crossover(parent1, parent2)

            # Mutación
            self.mutate(child1)
            self.mutate(child2)

            # Agregar hijos a la nueva población
            new_population.append(child1)

            if len(new_population) < self.size:
                new_population.append(child2)

        # Reemplazo con la poblacion antigua.
        # el slice es por si se pasa de total de la población.
        self.population = np.array(new_population[: self.size], dtype=np.uint8)

        # Resetear fitness para la nueva generación
        self.fitness = np.full(self.size, np.inf, dtype=np.float64)
