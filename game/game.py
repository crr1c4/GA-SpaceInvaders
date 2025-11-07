# La clase Game sirve para contener toda la logica del juego.
import pygame
import random

from gen.population import SHOOT
from utils import ALIEN_BLUE, CHROMOSOME_SIZE
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
        self.alien_direction = random.choice([-1, 1])
        self.alien_laser = pygame.sprite.GroupSingle()
        self.run = True
        self.explosion_sound = pygame.mixer.Sound("game/assets/explosion.ogg")
        self.fitness: int = 0

        # Variables de diagnóstico y métricas.
        self.alignment_count = 0  # Veces alineado verticalmente
        self.shots_fired = 0  # Total de disparos
        self.danger_encounters = 0  # Veces en zona de peligro
        self.steps_survived = 0  # Pasos antes de morir/ganar

        # Banderas de resultado.
        self.victory = False
        self.defeat = False

    # Se usarán 5 renglones x 11 columnas para los aliens.
    def create_alien(self):
        # Debe aparecer con la segundo renglón (ranglon 1), y la columna de en medio (10).
        x = random.randint(0, self.columns - 1) * self.cell_size + self.cell_size // 2
        y = self.cell_size + self.cell_size // 2

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
            # TODO: CAMB
            if self.alien.sprite:
                self.alien.sprite.rect.y += distance

                if self.alien.sprite.rect.y + self.cell_size > self.get_screen_height():
                    self.game_over()

    # Realiza el disparo de un alien al azar.
    def alien_shoot_laser(self):
        # Checa primero que haya aliens en la pantalla.
        if self.alien and not self.alien_laser:
            alien = self.alien.sprite
            laser_sprite = Laser(
                alien.rect.center,
                -self.cell_size,
                self.get_screen_height(),
                ALIEN_BLUE,
            )
            self.alien_laser.add(laser_sprite)

    # Verifica las colisiones.
    def check_for_collisions(self):
        # Primero verifica si alguno de los lasers del spaceship colisiona con un alien.
        if self.spaceship.sprite.laser:
            laser_sprite = self.spaceship.sprite.laser.sprite
            # El tercer argumento le indica a pygame si debe destruir el elemento con el que hizo colisión.
            # Si colisiono con un alien, se borra el laser
            alien_hit = pygame.sprite.spritecollide(laser_sprite, self.alien, True)

            if alien_hit:
                # Se reduce el fitness si gana.
                self.fitness -= 50_000
                # Checa cuantos pasos dio para el derrotar al alien
                # CHROMOSOME_SIZE esta aqui por si se cambia desde main jsjsjs.
                self.fitness -= (CHROMOSOME_SIZE - self.steps_survived) * 5
                self.victory = True
                self.explosion_sound.play()
                laser_sprite.kill()
                # Termina el juego, solo hay un alien.
                self.game_over()

        # Verificación por los disparos de los aliens.
        if self.alien_laser:
            if self.alien_laser:
                # Por lo pronto se dejará lo primero.
                if pygame.sprite.spritecollide(
                    self.alien_laser.sprite, self.spaceship, False
                ):
                    self.alien_laser.sprite.kill()
                    # Castigo por derrota.
                    self.fitness += 100_000
                    # Castigo por morir rapido < 20%.
                    if self.steps_survived < (CHROMOSOME_SIZE // 5):
                        self.fitness += 20_000
                    self.defeat = True
                    self.game_over()

        # Verifica si los aliens alcanzarón la nave
        if self.alien:
            for alien in self.alien:
                if pygame.sprite.spritecollide(alien, self.spaceship, False):
                    # Castigo por permitir que el alien aterrice.
                    self.fitness += 100_000
                    self.defeat = True
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
        self.fitness = 0
        self.alien_direction = random.choice([-1, 1])

        self.alignment_count = 0
        self.shots_fired = 0
        self.danger_encounters = 0
        self.steps_survived = 0
        self.victory = False
        self.defeat = False

    # Obtiene el ancho del tablero
    def get_screen_width(self):
        return self.cell_size * self.rows

    # Obtiene la altura del tablero
    def get_screen_height(self):
        return self.cell_size * self.columns

    # 🧮 Función de adaptación: verifica los criterios para evaluar el fitness de una iteración del juego.
    # Se le pasa como parametro la acción para evaluar la acción.
    # El objetivo es minimizar, el fitness bajo es un "buen" jugador.
    def calculate_fitness_step(self, action: int):
        # Criterio 1. Distancia horizontal del laser al alien.
        if self.spaceship.sprite.laser and self.alien.sprite:
            # Obtencion de las entidades
            laser = self.spaceship.sprite.laser.sprite
            alien = self.alien.sprite

            # Obtención de la distancia vertical
            vertical_distance = abs(laser.rect.centery - alien.rect.centery)

            # Checa si estan en el mismo renglon, si es asi, saca la distancia entre columnas.
            # Mientras menos distancia significa que mas cerca estuvo de darle.
            if vertical_distance < (self.cell_size // 2):
                horizontal_distance = abs(laser.rect.centerx - alien.rect.centerx)
                self.fitness += horizontal_distance

                self.alignment_count += 1

                # Bonificación por si estuvo cerca de darle.
                if horizontal_distance < self.cell_size:
                    self.fitness -= 10

        # Criterio 2. Penalización por peligro (distancia del laser del alien a la nave).
        if self.alien_laser.sprite and self.spaceship.sprite:
            alien_laser = self.alien_laser.sprite
            spaceship = self.spaceship.sprite

            distance_to_danger = abs(alien_laser.rect.centerx - spaceship.rect.centerx)

            # Si la distancia entre la nave y el laser del alien es menor a dos casillas,
            # se tiene que penalizar...
            if distance_to_danger < self.cell_size * 2:
                self.fitness += (self.cell_size * 2 - distance_to_danger) * 3
                self.danger_encounters += 1

        # Penalizacion por disparo ineficiente. Esto lo agregamos para que se vayan
        # casitigando los intentos de disparo mientras existe un laser en el espacio.
        # Por que quita la posibilidad de moverse.
        if action == SHOOT:
            # Castiga el spam de disparos
            if self.spaceship.sprite.laser:
                self.fitness += 5

            # Penalización por disparar lejos del alien.
            elif self.alien.sprite:
                alien = self.alien.sprite
                spaceship = self.spaceship.sprite

                horizontal_distance = abs(spaceship.rect.centerx - alien.rect.centerx)

                # Casillas de tolerancia: 5
                if horizontal_distance > self.cell_size * 5:
                    self.fitness += 20

        self.steps_survived += 1
