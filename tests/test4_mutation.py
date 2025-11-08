import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gen.population import Population, LEFT

def test_mutation():
    """
    Verifica que el operador de mutación funcione correctamente basado en la
    tasa de mutación.
    """
    print("--- Ejecutando Prueba 4: Verificación de Mutación ---")
    
    population = Population(size=1, chromosome_size=1000)
    
    # --- Caso 1: Forzar mutación en todos los genes (tasa = 1.0) ---
    population.mutation_rate = 1.0
    chromosome_to_mutate = np.full(population.chromosome_size, LEFT, dtype=np.uint8)

    population.mutate(chromosome_to_mutate)
    
    # Verificación: Ningún gen debería ser 'LEFT' (1) después de la mutación forzada.
    assert np.all(chromosome_to_mutate != LEFT), "Error: Con una tasa de 1.0, todos los genes deberían haber mutado."
    print("- Mutación al 100% cambió todos los genes correctamente.")

    # --- Caso 2: Evitar la mutación (tasa = 0.0) ---
    population.mutation_rate = 0.0
    original_chromosome = np.full(population.chromosome_size, LEFT, dtype=np.uint8)
    chromosome_to_preserve = original_chromosome.copy()

    population.mutate(chromosome_to_preserve)
    
    # Verificación: El cromosoma no debería haber cambiado.
    assert np.array_equal(original_chromosome, chromosome_to_preserve), "Error: Con una tasa de 0.0, ningún gen debería haber mutado."
    print("- Tasa de mutación al 0% no alteró el cromosoma.")
    print("--- Prueba 4 superada con éxito ---\n")

if __name__ == "__main__":
    test_mutation()