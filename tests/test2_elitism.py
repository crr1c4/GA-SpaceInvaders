import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gen.population import Population

def test_elitism_selection():
    """
    Verifica que el mecanismo de selección por elitismo escoja a los
    individuos con el mejor fitness (el más bajo).
    """
    print("--- Ejecutando Prueba 2: Verificación de Selección por Elitismo ---")

    # 1. Crear una población de prueba
    population = Population(size=10, chromosome_size=5, elite_percentage=0.20)
    
    # 2. Asignar fitness manualmente. Los mejores son 10 (índice 9) y 20 (índice 1)
    fitness_scores = np.array([100, 20, 300, 40, 500, 60, 700, 80, 900, 10])
    population.fitness = fitness_scores
    
    # elite_count = max(2, int(10 * 0.20)) = 2. Debe seleccionar 2 individuos.
    
    # 3. Ejecutar la selección por elitismo
    elite_chromosomes = population.select_parents_by_elitism()

    # 4. Verificar los resultados
    # El número de élites debe ser 2
    assert elite_chromosomes.shape[0] == 2, f"Error: Se esperaban 2 élites, pero se obtuvieron {elite_chromosomes.shape[0]}"
    print("- Número de élites correcto: 2")

    # Obtener los índices de los 2 mejores fitness (los más bajos)
    # np.argsort devuelve los índices que ordenarían el arreglo
    expected_best_indices = np.argsort(fitness_scores)[:2] # Debería ser [9, 1]

    # Obtener los cromosomas que corresponden a esos índices
    expected_chromosomes = population.population[expected_best_indices]
    
    # Verificar que los cromosomas seleccionados son los esperados
    assert np.array_equal(elite_chromosomes, expected_chromosomes), "Error: Los cromosomas de la élite no son los esperados."
    print("- Los individuos de la élite son los correctos (fitness más bajo).")
    print("--- Prueba 2 superada con éxito ---\n")

if __name__ == "__main__":
    test_elitism_selection()