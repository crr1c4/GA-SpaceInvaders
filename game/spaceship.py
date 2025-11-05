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
                self.speed * random.randint(0, self.screen_width // self.speed) + 25,
                self.screen_height,
            )
        )
        self.laser_sound = pygame.mixer.Sound("game/assets/laser.ogg")

        # Lasers: como solo puedo disparar uno a la vez, este sera un GroupSingle
        self.laser_group = pygame.sprite.GroupSingle()

    # TODO: Se va a cambiar esto por los metodos del algoritmo genetico.
    # def move_left
    # def move_right
    # def get_user_input(self):
    #     keys = pygame.key.get_pressed()

    #     if keys[pygame.K_RIGHT]:
    #         self.rect.x += self.speed

    #     if keys[pygame.K_LEFT]:
    #         self.rect.x -= self.speed

    #     # Checa que no exista ya un misil en la pantalla.
    #     if keys[pygame.K_SPACE] and not self.laser_group:
    #         laser = Laser(self.rect.center, 5, self.screen_height)
    #         self.laser_group.add(laser)
    #         self.laser_sound.play()

    # Mueve la spaceship hacia la izquierda.
    def move_left(self):
        self.rect.x -= self.speed
        # Limite izquierdo.
        if self.rect.left < 0:
            self.rect.left = self.offset

    # Mueve la spaceship hacia la derecha.
    def move_right(self):
        self.rect.x -= self.speed

        # Limite derecho.
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width

    def shoot(self):
        laser = Laser(self.rect.center, self.speed, self.screen_height)
        self.laser_group.add(laser)
        self.laser_sound.play()

    # Checa que la spaceschip no se salga de los limites de la pantalla.
    def constrain_movement(self):
        # Limite derecho.
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width

        # Limite izquierdo.
        if self.rect.left < 0:
            self.rect.left = self.offset

    # Actualiza el renderizado de la spaceship.
    def update(self):
        # self.get_user_input()
        self.constrain_movement()
        self.laser_group.update()

    # Resetea la posición del spaceship.
    def reset(self):
        self.rect = self.image.get_rect(
            midbottom=((self.screen_width + self.offset) / 2, self.screen_height)
        )
        # Elimina el laser del spaceship
        self.laser_group.empty()
