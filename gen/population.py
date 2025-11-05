from .individual import Individual


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
