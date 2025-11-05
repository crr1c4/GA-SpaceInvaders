import random

# Valores que puede tomar allele del gen
LEFT = 1
RIGHT = 2
SHOOT = 3


# Representación de un individuo, osea una solución unica para el juego.
class Individual:
    def __init__(self, chromosome_size: int):
        # Un cromosoma representa un arreglo con los acciones que va a tener que ejecutar.
        self.chromosome_size: int = chromosome_size
        # Para generar un individuo aleatorio, se crea un cromosoma con valores (alleles) aleatorios.
        # Esto esta en la página 21 de los apuntes.
        self.chromosome: list[int] = [
            random.randint(1, 3) for _ in range(self.chromosome_size)
        ]
        # fitness es la adaptación del juego. Se va a cambiar dependiendo de la puntuacion o de lo cerca que llegan los misiles del defenser al invasor.
        # PREGUNTARLE A LA MAESTRA SI SE PUEDE DEJAR COMO LA PUNTUACION.
        self.fitness: int = -1
