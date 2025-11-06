from .individual import Individual
import random


# Representación de una población.
class Population:
    # Los parametros iniciales que se le van a pasar son el tamaño de la población y el tamaño del cromosoma de cada individuo.
    def __init__(
        self, size_population: int, chromosome_size: int, generations: int = 50
    ):
        self.size_population: int = size_population
        self.chromosome_size: int = chromosome_size
        # Generar una población inicial (1ejecución del programa = 50 generaciones = 50 juegos con información de la población anterior)
        self.generations: int = generations
        # Número de generacion actual.
        self.actual_generation: int = 1
        # Asignación de los individuos de la población.
        self.individuals: list[Individual] = [
            Individual(self.chromosome_size) for _ in range(self.size_population)
        ]

    def select_parents_by_tournament(self, tournament_size=3) -> list[Individual]:
        """
        Selecciona individuos para la siguiente generación usando selección por torneo.
        Funciona para minimización (menor fitness es mejor).
        """
        selected_parents = []
        for _ in range(self.size_population):
            # Elige N individuos al azar para el torneo
            participants = random.sample(self.individuals, tournament_size)

            # Elige al ganador (el de MENOR fitness/distancia)
            winner = min(participants, key=lambda ind: ind.fitness)
            selected_parents.append(winner)
        return selected_parents

    def crossover(
        self, parent1: Individual, parent2: Individual, crossover_rate=0.7
    ) -> tuple[list[int], list[int]]:
        """
        Realiza un cruce de un solo punto.
        """
        cromo1 = parent1.chromosome
        cromo2 = parent2.chromosome

        if random.random() < crossover_rate:
            # Elige un punto de corte aleatorio
            cut_point = random.randint(1, self.chromosome_size - 1)

            # Crea los hijos
            child1_chromo = cromo1[:cut_point] + cromo2[cut_point:]
            child2_chromo = cromo2[:cut_point] + cromo1[cut_point:]

            return child1_chromo, child2_chromo
        else:
            # Si no hay cruce, los hijos son clones
            return cromo1, cromo2

    def mutate(self, chromosome: list[int], mutation_rate=0.01):
        """
        Muta un cromosoma cambiando aleatoriamente un gen (acción).
        """
        for i in range(len(chromosome)):
            if random.random() < mutation_rate:
                # Cambia la acción por una de las otras dos
                new_action = random.randint(1, 3)
                while (
                    new_action == chromosome[i]
                ):  # Asegura que sea una acción diferente
                    new_action = random.randint(1, 3)
                chromosome[i] = new_action

    # --- FIN AÑADIDO ---
