# Archivo que contiene la lógica de misil o laser que el spaceship va a lanzar.
import pygame


# Al tratarse de una entidad, igual se va a utilizar la clase Sprite.
class Laser(pygame.sprite.Sprite):
    def __init__(self, position, speed, screen_height):
        super().__init__()
        self.image = pygame.Surface((4, 15))  # Se guarda un rectangulo.
        self.image.fill((243, 216, 63))  # Color del laser.
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.screen_height = screen_height

    # Actualiza el movimiento del laser
    def update(self):
        self.rect.y -= self.speed

        # Si el laser sale de la pantalla, se manda a eliminar del juego.
        if self.rect.y > self.screen_height + 15 or self.rect.y < 0:
            # print("Killed")
            self.kill()
