# La clase Game sirve para contener toda la logica del juego.
import pygame
from .spaceship import Spaceship


class Game:
    def __init__(self, screen_width: int, screen_height: int) -> None:
        self.screen_width = screen_width
        self.screen_height = screen_height
        # Los grupos sirven para agrupar las entidades y poder renderizarlas mas facil.
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(self.screen_width, self.screen_height))
