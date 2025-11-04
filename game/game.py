# La clase Game sirve para contener toda la logica del juego.
import pygame
import random

from .laser import Laser
from .spaceship import Spaceship
from .alien import Alien


class Game:
    def __init__(self, screen_width: int, screen_height: int, offset: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset
        # Los grupos sirven para agrupar las entidades y poder renderizarlas mas facil.
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(
            Spaceship(self.screen_width, self.screen_height, self.offset)
        )
        # Grupo para los aliens.
        self.aliens_group = pygame.sprite.Group()
        self.create_aliens()
        self.aliens_direction = 1
        self.alien_lasers_group = pygame.sprite.Group()
        # El algoritmo genetico reiniciara el juego, por lo que no es necesario tener mas de una vida.
        self.lives = 1
        self.run = True
        self.score = 0
        self.highscore = 0
        # Musica de fondo
        # pygame.mixer.music.load("game/assets/music.ogg")
        # pygame.mixer.music.play(-1)  # -1 indica el loop
        self.explosion_sound = pygame.mixer.Sound("game/assets/explosion.ogg")

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
                alien = Alien(x + self.offset // 2, y, alien_type)
                self.aliens_group.add(alien)

    def move_aliens(self):
        # Actualiza la ubicacion de los aliens.
        self.aliens_group.update(self.aliens_direction)

        # Para detectar el borde de la pantalla y evitar que se salgan, se obtienen todos los aliens (sprites) en una lista.
        alien_sprites = self.aliens_group.sprites()

        # Se iteran por cada uno y se checa si ya paso el limite de la pantalla.
        for alien in alien_sprites:
            # Limite derecho
            if alien.rect.right >= self.screen_width + self.offset / 2:
                self.aliens_direction = -1
                self.move_down_alien(2)
            # Limite izquierdo
            elif alien.rect.left <= self.offset / 2:
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
            aliens_hit = pygame.sprite.spritecollide(
                laser_sprite, self.aliens_group, True
            )

            if aliens_hit:
                self.explosion_sound.play()
                for alien in aliens_hit:
                    self.score += alien.type * 100
                    self.check_for_highscore()
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
                    # Checa las vidas del spaceship.
                    self.lives -= 1

                    if self.lives == 0:
                        self.game_over()

        # Verifica si los aliens alcanzarón la nave
        if self.aliens_group:
            for alien in self.aliens_group:
                if pygame.sprite.spritecollide(alien, self.spaceship_group, False):
                    # TODO: Hay que checar esto, para algoritmo genetico.
                    self.game_over()

    # Maneja el evento de game over.
    def game_over(self):
        self.run = False
        print("Game Over")

    # Reinicia el juego
    def reset(self):
        self.run = True
        self.lives = 1
        self.spaceship_group.sprite.reset()
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.create_aliens()
        self.score = 0

    # Checa la puntuación mas alta.
    def check_for_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score

            # Por si se quiere guardar la highscore de manera persistente.
            # with open("highscore.txt", "w") as file:
            #     file.write(str(self.highscore))
