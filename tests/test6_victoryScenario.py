import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    import pygame
    from game.game import Game
    from game.laser import Laser
    from utils import CELL_SIZE, ROWS, COLUMNS
except ImportError as e:
    print(f"Error: Faltan módulos del proyecto (Pygame, Game, Laser, etc.).")
    print(f"Detalle: {e}")
    sys.exit(1)

# --- Definición de la Prueba ---

def test_6_game_logic_victory_scenario():
    """
    Prueba 6: Verifica un escenario de victoria (Caja Negra de Lógica de Juego).
    Simula una colisión directa entre un láser y un alien.
    """
    print("\n--- Ejecutando Prueba 6: Escenario de Victoria (Caja Negra) ---")
    
    # 1. Inicialización (requerida por Pygame)
    pygame.init()
    
    # 2. Configurar el escenario
    game = Game(CELL_SIZE, ROWS, COLUMNS)
    
    # Obtenemos el alien para forzar su posición
    alien = game.alien.sprite
    
    # Creamos un láser manualmente y lo añadimos al grupo del spaceship
    laser = Laser((500, 100), 10, game.get_screen_height())
    game.spaceship.sprite.laser.add(laser)

    # Forzamos la posición de colisión exacta
    alien.rect.center = (500, 100)
    laser.rect.center = (500, 100)
    
    # 3. Ejecutar el Sistema (la "Caja Negra")
    # Este es el método que maneja la lógica de colisiones
    game.check_for_collisions()
    
    # 4. Verificar el Resultado Observable
    assert game.victory == True, "El juego no registró la victoria."
    assert game.run == False, "El juego debería detenerse (game.run = False) después de la victoria."
    assert len(game.alien) == 0, "El grupo de aliens no fue vaciado después de la colisión."

    print("- Escenario de victoria detectado correctamente.")
    print("--- Prueba 7 Superada ---")
    
    # Limpiar pygame
    pygame.quit()


# --- Ejecutor de esta prueba ---

if __name__ == "__main__":
    try:
        test_6_game_logic_victory_scenario()
        print("\nPrueba de escenario de victoria completada con éxito.")
    except AssertionError as e:
        print(f"\n X PRUEBA FALLIDA: {e}")
        sys.exit(1)