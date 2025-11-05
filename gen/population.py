from .individual import Individual


# Representación de una población.
class Population:
    # Los parametros iniciales que se le van a pasar son el tamaño de la población y el tamaño del cromosoma de cada individuo.
    def __init__(self, size_population: int, chromosome_size: int):
        self.size_population = size_population
        self.chromosome_size = chromosome_size
        self.individuals = []

        # Asignación de los individuos de la población.
        for index in range(self.size_population):
            self.individuals[index] = Individual(self.chromosome_size)
