# Archivo que va a almacenar toda la lógica de la nave aliada.
import pygame
import random

from .laser import Laser


# Se usa las sprite class de pygame para que sea mas facil de manejar.
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen_width: int, screen_height: int, offest: int, speed: int):
        super().__init__()
        # Dimensiones de la pantalla
        self.offset = offest
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        # pyagme usa la ruta raíz del proyecto.
        self.image = pygame.image.load("game/assets/spaceship.png")
        # Posiciona la spaceship en la parte inferior media; en ese punto se posiciona la parte inferior media de la imagen.
        self.speed = speed
        # La velocidad tambien funciona como el tamaño de la celda
        self.rect = self.image.get_rect(
            midbottom=(
                self.speed * random.randint(0, self.screen_width // self.speed)
                + self.offset,
                self.screen_height,
            )
        )
        self.laser_sound = pygame.mixer.Sound("game/assets/laser.ogg")

        # Lasers: como solo puedo disparar uno a la vez, este sera un GroupSingle
        self.laser = pygame.sprite.GroupSingle()

    # Mueve la spaceship hacia la izquierda.
    def move_left(self):
        self.rect.x -= self.speed
        # Limite izquierdo.
        if self.rect.x < 0:
            self.rect.x = 0

    # Mueve la spaceship hacia la derecha.
    def move_right(self):
        self.rect.x += self.speed

        # Limite derecho.
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width

    def shoot(self):
        if not self.laser:
            laser = Laser(self.rect.center, self.speed, self.screen_height)
            self.laser.add(laser)
            # self.laser_sound.play()

    # Actualiza el renderizado de la spaceship.
    def update(self):
        pass
        # self.get_user_input()
        # self.constrain_movement()
        # self.laser.update()

    # Resetea la posición del spaceship.
    def reset(self):
        self.rect = self.image.get_rect(
            midbottom=(
                self.speed * random.randint(0, self.screen_width // self.speed) + 25,
                self.screen_height,
            )
        )
        # Elimina el laser del spaceship
        self.laser.empty()
