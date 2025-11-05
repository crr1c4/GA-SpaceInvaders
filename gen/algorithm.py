# Este archivo contiene la lógica del algoritmo genetico

# FASES DEL ALGORITMO GENÉTICO.
# 1. Calcular la adaptación
# 2. Seleccionar a los padres
# 3. Crossover y mutación
# 4. Regresa al paso 1
from .population import Population
# from .individual import Individual

INDIVIDUAL_CHROMOSOME_SIZE = 50
POPULATION_SIZE = 50

population = Population(POPULATION_SIZE, INDIVIDUAL_CHROMOSOME_SIZE)

for individual in population.individuals:
    print(individual.chromosome)
