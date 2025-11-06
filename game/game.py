# La clase Game sirve para contener toda la logica del juego.
from numpy.ma import column_stack
import pygame
import random

from .laser import Laser
from .spaceship import Spaceship
from .alien import Alien


class Game:
    def __init__(
        self,
        cell_size: int,
        rows: int,
        columns: int,
    ):
        # Variable para matriz de ranglones y columnas
        self.cell_size = cell_size
        self.rows = rows
        self.columns = columns

        # Los grupos sirven para agrupar las entidades y poder renderizarlas mas facil.
        self.spaceship = pygame.sprite.GroupSingle()
        self.spaceship.add(
            Spaceship(
                self.get_screen_width(), self.get_screen_height(), 25, self.cell_size
            )
        )
        # Grupo para los aliens.
        self.alien = pygame.sprite.GroupSingle()
        self.create_alien()
        self.alien_direction = 1
        self.alien_laser = pygame.sprite.GroupSingle()
        self.run = True
        self.explosion_sound = pygame.mixer.Sound("game/assets/explosion.ogg")

    # Se usarán 5 renglones x 11 columnas para los aliens.
    def create_alien(self):
        # Debe aparecer con la segundo renglón (ranglon 1), y la columna de en medio (10).
        x = self.get_screen_width() // 2 + self.cell_size // 2
        y = 1 * self.cell_size + self.cell_size // 2

        alien = Alien(x, y, 1)
        self.alien.add(alien)

    def move_alien(self):
        # Actualiza la ubicacion de los aliens.
        self.alien.update(self.alien_direction * self.cell_size)

        # Para detectar el borde de la pantalla y evitar que se salgan, se obtienen todos los aliens (sprites) en una lista.
        alien = self.alien.sprite

        # Limite derecho
        if (
            alien.rect.right + (alien.rect.right % self.cell_size)
            >= self.get_screen_width()
        ):
            self.alien_direction = -1
            self.move_down_alien(self.cell_size)
        # Limite izquierdo
        elif alien.rect.left - (alien.rect.left % self.cell_size) <= 0:
            self.alien_direction = 1
            self.move_down_alien(self.cell_size)

    # Mueve los aliens hacia abajo
    def move_down_alien(self, distance):
        # Checa primero si hay aliens en la pantalla.
        if self.alien:
            # Agrega la distancia.
            for alien in self.alien.sprites():
                alien.rect.y += distance

    # Realiza el disparo de un alien al azar.
    def alien_shoot_laser(self):
        # Checa primero que haya aliens en la pantalla.
        if self.alien and not self.alien_laser:
            alien = self.alien.sprite
            laser_sprite = Laser(
                alien.rect.center, -self.cell_size, self.get_screen_height()
            )
            self.alien_laser.add(laser_sprite)

    # Verifica las colisiones.
    def check_for_collisions(self):
        # Primero verifica si alguno de los lasers del spaceship colisiona con un alien.
        if self.spaceship.sprite.laser:
            laser_sprite = self.spaceship.sprite.laser_group.sprite
            # El tercer argumento le indica a pygame si debe destruir el elemento con el que hizo colisión.
            # Si colisiono con un alien, se borra el laser
            alien_hit = pygame.sprite.spritecollide(laser_sprite, self.alien, True)

            if alien_hit:
                self.explosion_sound.play()
                laser_sprite.kill()

        # Verificación por los disparos de los aliens.
        if self.alien_laser:
            for laser_sprite in self.alien_laser:
                # TODO: Como se va a implementar el algoritmo genetico, se deba checar si se tendran n cantidad de vidas o se va a reiniciar.
                # Por lo pronto se dejará lo primero.
                if pygame.sprite.spritecollide(laser_sprite, self.spaceship, False):
                    laser_sprite.kill()
                    # Checa las vidas del spaceship.
                    # self.lives -= 1

                    # if self.lives == 0:
                    self.game_over()

        # Verifica si los aliens alcanzarón la nave
        if self.alien:
            for alien in self.alien:
                if pygame.sprite.spritecollide(alien, self.spaceship, False):
                    # TODO: Hay que checar esto, para algoritmo genetico.
                    self.game_over()

    # Maneja el evento de game over.
    def game_over(self):
        self.run = False

    # Reinicia el juego
    def reset(self):
        self.run = True
        # self.lives = 1
        self.spaceship.sprite.reset()
        self.alien.empty()
        self.alien_laser.empty()
        self.create_alien()
        # self.score = 0

    # Obtiene el ancho del tablero
    def get_screen_width(self):
        return self.cell_size * self.rows

    # Obtiene la altura del tablero
    def get_screen_height(self):
        return self.cell_size * self.columns
