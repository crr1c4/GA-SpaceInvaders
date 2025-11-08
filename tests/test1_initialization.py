import numpy as np
import sys
import os

# Agregamos la ruta raíz del proyecto para que Python pueda encontrar los módulos
# Asume que este script está en una carpeta 'tests/'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gen.population import Population, LEFT, RIGHT, SHOOT

def test_population_initialization():
    """
    Verifica que la población inicial se genere con los parámetros correctos.
    """
    print("--- Ejecutando Prueba 1: Verificación de Creación de Población ---")

    # Parámetros de prueba
    test_size = 50
    test_chromosome_size = 1000

    # 1. Crear una instancia de la población
    population = Population(size=test_size, chromosome_size=test_chromosome_size)

    # 2. Verificar las dimensiones de la población
    # La forma (shape) del arreglo debe ser (tamaño_poblacion, tamaño_cromosoma)
    expected_shape = (test_size, test_chromosome_size)
    assert population.population.shape == expected_shape, f"Error: La forma esperada era {expected_shape}, pero se obtuvo {population.population.shape}"
    print(f"- Dimensiones de la población correctas: {population.population.shape}")

    # 3. Verificar el rango de los valores de los genes
    # Cada gen debe ser 1 (LEFT), 2 (RIGHT), o 3 (SHOOT)
    is_within_range = np.all((population.population >= LEFT) & (population.population <= SHOOT))
    assert is_within_range, "Error: Se encontraron genes fuera del rango [1, 3]"
    print("- Rango de valores de genes correcto.")

    # 4. Verificar la inicialización del arreglo de fitness
    assert population.fitness.shape == (test_size,), f"Error: La forma del arreglo de fitness debería ser ({test_size},), pero fue {population.fitness.shape}"
    assert np.all(population.fitness == np.inf), "Error: El fitness no se inicializó a infinito."
    print("- Arreglo de fitness inicializado correctamente.")
    print("--- Prueba 1 superada con éxito ---\n")

# Ejecutar la prueba
if __name__ == "__main__":
    test_population_initialization()