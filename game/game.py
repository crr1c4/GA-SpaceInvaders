# La clase Game sirve para contener toda la logica del juego.
import pygame
import random

from .laser import Laser
from .spaceship import Spaceship
from .alien import Alien


class Game:
    def __init__(self, screen_width: int, screen_height: int) -> None:
        self.screen_width = screen_width
        self.screen_height = screen_height
        # Los grupos sirven para agrupar las entidades y poder renderizarlas mas facil.
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(self.screen_width, self.screen_height))
        # Grupo para los aliens.
        self.aliens_group = pygame.sprite.Group()
        self.create_aliens()
        self.aliens_direction = 1
        self.alien_lasers_group = pygame.sprite.Group()

    # Se usarán 5 renglones x 11 columnas para los aliens.
    def create_aliens(self):
        for row in range(5):
            for column in range(11):
                # Tamaño de la celda es 55
                # Los numeros que se suman al principio son para mostrar los aliens con un offset.
                x = 75 + column * 55
                y = 110 + row * 55

                # Los tipos se eligen segun la columna
                if row == 0:
                    alien_type = 3
                elif row in (1, 2):
                    alien_type = 2
                else:
                    alien_type = 1
                alien = Alien(x, y, alien_type)
                self.aliens_group.add(alien)

    def move_aliens(self):
        # Actualiza la ubicacion de los aliens.
        self.aliens_group.update(self.aliens_direction)

        # Para detectar el borde de la pantalla y evitar que se salgan, se obtienen todos los aliens (sprites) en una lista.
        alien_sprites = self.aliens_group.sprites()

        # Se iteran por cada uno y se checa si ya paso el limite de la pantalla.
        for alien in alien_sprites:
            # Limite derecho
            if alien.rect.right >= self.screen_width:
                self.aliens_direction = -1
                self.move_down_alien(2)
            # Limite izquierdo
            elif alien.rect.left <= 0:
                self.aliens_direction = 1
                self.move_down_alien(2)

    # Mueve los aliens hacia abajo
    def move_down_alien(self, distance):
        # Checa primero si hay aliens en la pantalla.
        if self.aliens_group:
            # Agrega la distancia.
            for alien in self.aliens_group.sprites():
                alien.rect.y += distance

    # Realiza el disparo de un alien al azar.
    def alien_shoot_laser(self):
        # Checa primero que haya aliens en la pantalla.
        if self.aliens_group.sprites():
            # Elige uno al azar.
            random_alien = random.choice(self.aliens_group.sprites())
            # Se crea el laser basado en los parametros del alien elegido.
            laser_sprite = Laser(random_alien.rect.center, -6, self.screen_height)
            self.alien_lasers_group.add(laser_sprite)

    # Verifica las colisiones.
    def check_for_collisions(self):
        # Primero verifica si alguno de los lasers del spaceship colisiona con un alien.
        if self.spaceship_group.sprite.laser_group:
            laser_sprite = self.spaceship_group.sprite.laser_group.sprite
            # El tercer argumento le indica a pygame si debe destruir el elemento con el que hizo colisión.
            # Si colisiono con un alien, se borra el laser
            if pygame.sprite.spritecollide(laser_sprite, self.aliens_group, True):
                laser_sprite.kill()

        # Verificación por los disparos de los aliens.
        if self.alien_lasers_group:
            for laser_sprite in self.alien_lasers_group:
                # TODO: Como se va a implementar el algoritmo genetico, se deba checar si se tendran n cantidad de vidas o se va a reiniciar.
                # Por lo pronto se dejará lo primero.
                if pygame.sprite.spritecollide(
                    laser_sprite, self.spaceship_group, False
                ):
                    laser_sprite.kill()
                    print("Spaceship hit")

        # Verifica si los aliens alcanzarón la nave
        if self.aliens_group:
            for alien in self.aliens_group:
                if pygame.sprite.spritecollide(alien, self.spaceship_group, False):
                    print("Spaceship hit")
