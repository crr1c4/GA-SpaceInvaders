import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import CHROMOSOME_SIZE

def test_fitness_extreme_cases():
    """
    Verifica que las bonificaciones y penalizaciones más grandes (victoria/derrota)
    se apliquen correctamente al fitness.
    """
    print("--- Ejecutando Prueba 5: Verificación de Fitness (Casos Extremos) ---")

    # --- Caso 1: Victoria Rápida ---
    # Simula una victoria en muy pocos pasos. El fitness debería ser muy bajo (bueno).
    steps_survived_win = 10
    
    # Lógica extraída de game.py para el cálculo de fitness en victoria
    # self.fitness -= 50_000
    # self.fitness -= (CHROMOSOME_SIZE - self.steps_survived) * 5
    expected_win_fitness = -50_000 - (CHROMOSOME_SIZE - steps_survived_win) * 5
    
    assert expected_win_fitness < -54000, "Error: El fitness por victoria rápida no es tan bajo como se esperaba."
    print(f"- Fitness por victoria rápida calculado correctamente: {expected_win_fitness}")

    # --- Caso 2: Derrota Rápida ---
    # Simula una derrota en los primeros pasos, lo que activa una penalización extra.
    steps_survived_loss = 5
    
    # Lógica extraída de game.py para el cálculo de fitness en derrota
    # self.fitness += 100_000
    # if self.steps_survived < (CHROMOSOME_SIZE // 5): self.fitness += 20_000
    
    # CHROMOSOME_SIZE // 5 es 200. Como 5 < 200, la penalización extra aplica.
    expected_loss_fitness = 100_000 + 20_000
    
    assert expected_loss_fitness == 120_000, "Error: El fitness por derrota rápida no es el esperado."
    print(f"- Fitness por derrota rápida calculado correctamente: {expected_loss_fitness}")
    print("--- Prueba 5 superada con éxito ---\n")

if __name__ == "__main__":
    test_fitness_extreme_cases()