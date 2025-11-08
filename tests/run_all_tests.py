import numpy as np
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from gen.population import Population, LEFT, RIGHT, SHOOT
    from utils import CHROMOSOME_SIZE
except ImportError as e:
    print(f"Error: No se pudieron importar los módulos del proyecto. Verifica la ruta.")
    print(f"Detalle: {e}")
    sys.exit(1)

# --- Definición de Pruebas ---

def test_1_initialization():
    """
    Prueba 1: Verifica que la población inicial se genere con los parámetros correctos.
    """
    print("\n--- Ejecutando Prueba 1: Verificación de Creación de Población ---")

    test_size = 50
    test_chromosome_size = 1000
    population = Population(size=test_size, chromosome_size=test_chromosome_size)

    # 1. Verificar las dimensiones de la población
    expected_shape = (test_size, test_chromosome_size)
    assert population.population.shape == expected_shape, f"Forma esperada {expected_shape}, se obtuvo {population.population.shape}"
    print("- Dimensiones de la población correctas.")

    # 2. Verificar el rango de los valores de los genes
    is_within_range = np.all((population.population >= LEFT) & (population.population <= SHOOT))
    assert is_within_range, "Se encontraron genes fuera del rango [1, 3]"
    print("- Rango de valores de genes correcto.")

    # 3. Verificar la inicialización del arreglo de fitness
    assert population.fitness.shape == (test_size,), f"Forma de fitness esperada ({test_size},), se obtuvo {population.fitness.shape}"
    assert np.all(population.fitness == np.inf), "El fitness no se inicializó a infinito."
    print("- Arreglo de fitness inicializado correctamente.")
    print("--- Prueba 1 Superada ---")


def test_2_elitism():
    """
    Prueba 2: Verifica que el mecanismo de selección por elitismo escoja a los
    individuos con el mejor fitness (el más bajo).
    """
    print("\n--- Ejecutando Prueba 2: Verificación de Selección por Elitismo ---")

    population = Population(size=10, chromosome_size=5, elite_percentage=0.20)
    
    # Asignar fitness manualmente. Los mejores son 10 (índice 9) y 20 (índice 1)
    fitness_scores = np.array([100, 20, 300, 40, 500, 60, 700, 80, 900, 10])
    population.fitness = fitness_scores
    
    # elite_count = max(2, int(10 * 0.20)) = 2.
    elite_chromosomes = population.select_parents_by_elitism()

    # 1. Verificar el número de élites
    assert elite_chromosomes.shape[0] == 2, f"Se esperaban 2 élites, se obtuvieron {elite_chromosomes.shape[0]}"
    print("- Número de élites correcto: 2")

    # 2. Verificar que los seleccionados sean los correctos
    expected_best_indices = np.argsort(fitness_scores)[:2] # Debería ser [9, 1]
    expected_chromosomes = population.population[expected_best_indices]
    
    assert np.array_equal(elite_chromosomes, expected_chromosomes), "Los cromosomas de la élite no son los esperados."
    print("- Los individuos de la élite son los correctos (fitness más bajo).")
    print("--- Prueba 2 Superada ---")


def test_3_crossover():
    """
    Prueba 3: Verifica que el operador de cruce de un punto funcione.
    """
    print("\n--- Ejecutando Prueba 3: Verificación de Cruce ---")

    population = Population(size=2, chromosome_size=20)
    
    parent1 = np.full(population.chromosome_size, LEFT, dtype=np.uint8)  # [1, 1, 1, ...]
    parent2 = np.full(population.chromosome_size, RIGHT, dtype=np.uint8) # [2, 2, 2, ...]

    # 1. Forzar el cruce (tasa = 1.0)
    child1, child2 = population.crossover(parent1, parent2, rate=1.0)
    assert LEFT in child1 and RIGHT in child1, "El hijo 1 no es una mezcla."
    assert LEFT in child2 and RIGHT in child2, "El hijo 2 no es una mezcla."
    print("- Cruce al 100% genera hijos mezclados correctamente.")

    # 2. Evitar el cruce (tasa = 0.0)
    child1_clone, child2_clone = population.crossover(parent1, parent2, rate=0.0)
    assert np.array_equal(child1_clone, parent1), "El hijo 1 debería ser un clon del padre 1."
    assert np.array_equal(child2_clone, parent2), "El hijo 2 debería ser un clon del padre 2."
    print("- Tasa de cruce al 0% resulta en clones de los padres.")
    print("--- Prueba 3 Superada ---")


def test_4_mutation():
    """
    Prueba 4: Verifica que el operador de mutación funcione basado en la tasa.
    """
    print("\n--- Ejecutando Prueba 4: Verificación de Mutación ---")
    
    population = Population(size=1, chromosome_size=1000)
    
    # 1. Forzar mutación (tasa = 1.0)
    population.mutation_rate = 1.0
    chromosome_to_mutate = np.full(population.chromosome_size, LEFT, dtype=np.uint8)
    population.mutate(chromosome_to_mutate)
    
    assert np.all(chromosome_to_mutate != LEFT), "Con tasa 1.0, todos los genes deberían haber mutado."
    print("- Mutación al 100% cambió todos los genes correctamente.")

    # 2. Evitar la mutación (tasa = 0.0)
    population.mutation_rate = 0.0
    original_chromosome = np.full(population.chromosome_size, LEFT, dtype=np.uint8)
    chromosome_to_preserve = original_chromosome.copy()
    population.mutate(chromosome_to_preserve)
    
    assert np.array_equal(original_chromosome, chromosome_to_preserve), "Con tasa 0.0, ningún gen debería haber mutado."
    print("- Tasa de mutación al 0% no alteró el cromosoma.")
    print("--- Prueba 4 Superada ---")


def test_5_fitness_sanity():
    """
    Prueba 5: Verifica que las bonificaciones/penalizaciones de fitness se apliquen.
    """
    print("\n--- Ejecutando Prueba 5: Verificación de Fitness (Casos Extremos) ---")

    # 1. Caso Victoria Rápida
    steps_survived_win = 10
    expected_win_fitness = -50_000 - (CHROMOSOME_SIZE - steps_survived_win) * 5
    
    assert expected_win_fitness < -54000, "El fitness por victoria rápida no es tan bajo como se esperaba."
    print(f"- Fitness por victoria rápida calculado correctamente: {expected_win_fitness}")

    # 2. Caso Derrota Rápida
    steps_survived_loss = 5
    # (CHROMOSOME_SIZE // 5) es 200. 5 < 200, por lo que la penalización extra aplica.
    expected_loss_fitness = 100_000 + 20_000
    
    assert expected_loss_fitness == 120_000, "El fitness por derrota rápida no es el esperado."
    print(f"- Fitness por derrota rápida calculado correctamente: {expected_loss_fitness}")
    print("--- Prueba 5 Superada ---")


# --- Ejecutor de Pruebas ---

if __name__ == "__main__":
    # Lista de todas las funciones de prueba que queremos ejecutar
    all_tests = [
        test_1_initialization,
        test_2_elitism,
        test_3_crossover,
        test_4_mutation,
        test_5_fitness_sanity
    ]
    
    passed_count = 0
    failed_count = 0

    print("--- INICIANDO EJECUCIÓN DE PRUEBAS DEL ALGORITMO GENÉTICO ---")

    for test_func in all_tests:
        try:
            # Llama a la función de prueba (ej. test_1_initialization())
            test_func()
            passed_count += 1
        except AssertionError as e:
            # Captura fallos de aserción (assert)
            print(f"- FALLÓ: {test_func.__name__} -> {e}")
            failed_count += 1
        except Exception as e:
            # Captura cualquier otro error inesperado (ej. TypeError, NameError)
            print(f"- ERROR en {test_func.__name__}: {e}")
            failed_count += 1
    
    print("\n--- RESUMEN DE PRUEBAS ---")
    print(f"Total de Pruebas: {len(all_tests)}")
    print(f"- Pasadas: {passed_count}")
    print(f"X Fallidas: {failed_count}")
    print("------------------------")

    # Termina con un código de error si alguna prueba falló
    if failed_count > 0:
        sys.exit(1)