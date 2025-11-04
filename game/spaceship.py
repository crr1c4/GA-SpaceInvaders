# Archivo que va a almacenar toda la lógica de la nave aliada.
import pygame


# Se usa las sprite class de pygame para que sea mas facil de manejar.
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        # Dimensiones de la pantalla
        self.screen_width = screen_width
        self.screen_height = screen_height
        # pyagme usa la ruta raíz del proyecto.
        self.image = pygame.image.load("game/assets/spaceship.png")
        # Posiciona la spaceship en la parte inferior media; en ese punto se posiciona la parte inferior media de la imagen.
        self.rect = self.image.get_rect(
            midbottom=(self.screen_width / 2, self.screen_height)
        )
        self.speed = 6

    # TODO: Se va a cambiar esto por los metodos del algoritmo genetico.
    def get_user_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

    # Checa que la spaceschip no se salga de los limites de la pantalla.
    def constrain_movement(self):
        # Limite derecho.
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width

        # Limite izquierdo.
        if self.rect.left < 0:
            self.rect.left = 0

    # Actualiza el renderizado de la spaceship.
    def update(self):
        self.get_user_input()
        self.constrain_movement()
