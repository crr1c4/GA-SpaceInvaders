import numpy as np
import os

from gen.population import Population

CHROMOSOME_SIZE = 1000
POPULATION_SIZE = 50
GENERATIONS = 50

# Colores
GREY = (29, 29, 27)
LIGHT_GREY = (40, 40, 36)
YELLOW = (243, 216, 63)
GREEN = (0, 200, 0)  # Verde para victorias
RED = (200, 0, 0)  # Rojo para derrotas
ALIEN_BLUE = (123, 124, 182)  # Color del alien

# Paleta de colores para la UI
COLOR_PALETTE = {
    "background": GREY,
    "text": YELLOW,
    "grid": LIGHT_GREY,
    "win": GREEN,
    "loss": RED,
    "alien": ALIEN_BLUE,
}

# Cuadricula del GRID
ROWS, COLUMNS = 20, 15
CELL_SIZE = 50
GRID_WIDTH = ROWS * CELL_SIZE
GRID_HEIGHT = COLUMNS * CELL_SIZE

# Espacio para la información del algoritmo genetico.
UI_WIDTH = 500

# Dimensiones y configuracion de la ventana de la ventana.
SCREEN_WIDTH = ROWS * CELL_SIZE + UI_WIDTH
SCREEN_HEIGHT = COLUMNS * CELL_SIZE

LOG_X_START = GRID_WIDTH + 30
LOG_Y_START = 50
LOG_LINE_HEIGHT = 45

GRAPH_X_START = GRID_WIDTH + 30
GRAPH_Y_START = SCREEN_HEIGHT - 180  # Deja espacio en la parte inferior para la gráfica
GRAPH_WIDTH = UI_WIDTH - 60
GRAPH_HEIGHT = 150
BAR_WIDTH = 8  # Ancho de cada barra de generación
BAR_SPACING = 2  # Espacio entre barras
# Calcula el número máximo de barras que caben en la gráfica
MAX_BARS = int(GRAPH_WIDTH / (BAR_WIDTH + BAR_SPACING))


def save_population(population: Population, filepath: str = "data.npz"):
    try:
        np.savez_compressed(
            filepath,
            population=population.population,
            fitness=population.fitness,
            size=population.size,
            chromosome_size=population.chromosome_size,
            generations=population.generations,
            mutation_rate=population.mutation_rate,
            elite_percentage=population.elite_percentage,
        )

        print(f"✅ Población guardada en: {filepath}")
    except Exception as e:
        print(f"❌ Error al guardar población: {e}")


def load_population(filepath: str = "data.npz"):
    from gen.population import Population

    if not os.path.exists(filepath):
        return None

    try:
        # Cargar archivo
        data = np.load(filepath)

        # Crear nueva instancia de Population con los parámetros guardados
        population = Population(
            size=int(data["size"]),
            chromosome_size=int(data["chromosome_size"]),
            generations=int(data["generations"]),
            # mutation_rate=float(data["mutation_rate"]),
            # elite_percentage=float(data["elite_percentage"]),
        )

        # Cargar los datos en la instancia
        population.population = data["population"]
        population.fitness = data["fitness"]
        print("✅ Población cargada")
        return population

    except Exception as e:
        print(f"❌ Error al cargar población: {e}")
        return None
