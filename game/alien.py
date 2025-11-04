# Archivo que contiene la lógica de los alies.
import pygame


class Alien(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, type: int):
        super().__init__()
        # El tipo carga el tipo de alien
        self.type = type
        # Carga el alien aleatorio.
        self.image = pygame.image.load(f"game/assets/alien_{type}.png")
        # Las coordendas iniciales seran segun la esquina superior izquierda.
        self.rect = self.image.get_rect(topleft=(x, y))

    # Actualiza el movimiento del alien
    # Si se quiere modificar la velocidad, se puede multiplicar direction
    def update(self, direction):
        self.rect.x += direction
