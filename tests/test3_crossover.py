import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gen.population import Population, LEFT, RIGHT

def test_crossover():
    """
    Verifica que el operador de cruce de un punto funcione como se espera.
    """
    print("--- Ejecutando Prueba 3: Verificación de Cruce ---")

    population = Population(size=2, chromosome_size=20)
    
    # 1. Crear dos padres muy diferentes para que el cruce sea evidente
    parent1 = np.full(population.chromosome_size, LEFT, dtype=np.uint8)  # [1, 1, 1, ...]
    parent2 = np.full(population.chromosome_size, RIGHT, dtype=np.uint8) # [2, 2, 2, ...]

    # --- Caso 1: Forzar el cruce (tasa = 1.0) ---
    child1, child2 = population.crossover(parent1, parent2, rate=1.0)

    # Verificación: Ambos hijos deben contener tanto 1s como 2s
    assert LEFT in child1 and RIGHT in child1, "Error: El hijo 1 no es una mezcla."
    assert LEFT in child2 and RIGHT in child2, "Error: El hijo 2 no es una mezcla."

    # Verificación más robusta: la cantidad total de genes no debe cambiar.
    # El total de '1's entre los dos hijos debe ser igual al tamaño del cromosoma.
    total_lefts = np.count_nonzero(child1 == LEFT) + np.count_nonzero(child2 == LEFT)
    assert total_lefts == population.chromosome_size, "Error: Se perdieron o ganaron genes 'LEFT' durante el cruce."
    print("- Cruce al 100% genera hijos mezclados correctamente.")

    # --- Caso 2: Evitar el cruce (tasa = 0.0) ---
    child1_clone, child2_clone = population.crossover(parent1, parent2, rate=0.0)
    
    # Verificación: Los hijos deben ser clones exactos de los padres
    assert np.array_equal(child1_clone, parent1), "Error: El hijo 1 debería ser un clon del padre 1."
    assert np.array_equal(child2_clone, parent2), "Error: El hijo 2 debería ser un clon del padre 2."
    print("- Tasa de cruce al 0% resulta en clones de los padres.")
    print("--- Prueba 3 superada con éxito ---\n")

if __name__ == "__main__":
    test_crossover()