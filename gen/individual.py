import random

# Valores que puede tomar allele del gen
LEFT = 1
RIGHT = 2
SHOOT = 3


# Representación de un individuo.
# Generar una población inicial (1ejecución del programa = 50 generaciones = 50 juegos con información de la población anterior)
class Individual:
    def __init__(self, chromosome_size: int, generations: int = 50):
        # Un cromosoma representa un arreglo con los acciones que va a tener que ejecutar.
        self.chromosome = []
        self.generate_random_cromosome(chromosome_size)
        self.generations = generations

    # Para generar un individuo aleatorio, se crea un cromosoma con valores (alleles) aleatorios.
    # Esto esta en la página 21 de los apuntes.
    def generate_random_cromosome(self, length: int):
        for locus in range(length):
            self.chromosome[locus] = random.randint(1, 3)
