import pygame
from utils import (
    LOG_X_START,
    LOG_Y_START,
    LOG_LINE_HEIGHT,
    GRAPH_X_START,
    GRAPH_Y_START,
    GRAPH_WIDTH,
    GRAPH_HEIGHT,
    BAR_WIDTH,
    BAR_SPACING,
    MAX_BARS,
    COLOR_PALETTE,
)


# Este módulo contiene las clases para dibujar toda la UI (Log y Gráfica).
class LogDisplay:
    def __init__(self, font):
        self.font = font
        self.x = LOG_X_START
        self.y = LOG_Y_START
        self.line_height = LOG_LINE_HEIGHT
        self.color = COLOR_PALETTE["text"]

    def draw(self, screen, gen_text, ind_text, fitness_text, elite_text, mutation_text):
        y_pos = self.y

        # Título
        title_surface = self.font.render("--- LOG DEL AG ---", True, self.color)
        screen.blit(title_surface, (self.x, y_pos))
        y_pos += self.line_height * 1.5

        # Generación e Individuo
        gen_surface = self.font.render(gen_text, True, self.color)
        screen.blit(gen_surface, (self.x, y_pos))
        y_pos += self.line_height

        ind_surface = self.font.render(ind_text, True, self.color)
        screen.blit(ind_surface, (self.x, y_pos))
        y_pos += self.line_height * 1.5

        # Fitness
        fit_title_surface = self.font.render(
            "MEJOR FITNESS (GEN PREVIA):", True, self.color
        )
        screen.blit(fit_title_surface, (self.x, y_pos))
        y_pos += self.line_height

        fit_val_surface = self.font.render(fitness_text, True, self.color)
        screen.blit(fit_val_surface, (self.x + 20, y_pos))
        y_pos += self.line_height * 1.5

        # Parámetros
        param_title_surface = self.font.render("PARAMETROS:", True, self.color)
        screen.blit(param_title_surface, (self.x, y_pos))
        y_pos += self.line_height

        elite_surface = self.font.render(elite_text, True, self.color)
        screen.blit(elite_surface, (self.x + 20, y_pos))
        y_pos += self.line_height

        mut_surface = self.font.render(mutation_text, True, self.color)
        screen.blit(mut_surface, (self.x + 20, y_pos))


class ResultsGraph:
    def __init__(self, font):
        self.font = font
        self.results = []  # Almacena {'wins': int, 'losses': int}
        self.x = GRAPH_X_START
        self.y = GRAPH_Y_START
        self.width = GRAPH_WIDTH
        self.height = GRAPH_HEIGHT
        self.bar_width = BAR_WIDTH
        self.bar_spacing = BAR_SPACING
        self.max_bars = MAX_BARS

        self.color_win = COLOR_PALETTE["win"]
        self.color_loss = COLOR_PALETTE["loss"]
        self.color_border = COLOR_PALETTE["grid"]
        self.color_text = COLOR_PALETTE["text"]

    def add_generation_result(self, wins, losses):
        self.results.append({"wins": wins, "losses": losses})
        # Si la lista es muy larga, elimina el resultado más antiguo
        if len(self.results) > self.max_bars:
            self.results.pop(0)

    def draw(self, screen):
        # Dibujar el recuadro
        pygame.draw.rect(
            screen, self.color_border, (self.x, self.y, self.width, self.height), 2
        )

        # Título
        title_surface = self.font.render("VICTORIAS / DERROTAS", True, self.color_text)
        screen.blit(
            title_surface,
            (
                self.x + (self.width // 2) - (title_surface.get_width() // 2),
                self.y - 35,
            ),
        )

        # Dibujar las barras
        x_offset = 0
        for res in self.results:
            total = res["wins"] + res["losses"]
            if total == 0:
                continue

            win_height = int((res["wins"] / total) * self.height)
            loss_height = self.height - win_height

            # Barra de Derrotas (roja, arriba)
            pygame.draw.rect(
                screen,
                self.color_loss,
                (self.x + x_offset, self.y, self.bar_width, loss_height),
            )
            # Barra de Victorias (verde, abajo)
            pygame.draw.rect(
                screen,
                self.color_win,
                (self.x + x_offset, self.y + loss_height, self.bar_width, win_height),
            )

            x_offset += self.bar_width + self.bar_spacing


class UIManager:
    def __init__(self, font):
        self.log_display = LogDisplay(font)
        self.results_graph = ResultsGraph(font)

        # Información estática que no cambia
        self.best_fitness_log = "N/A"
        self.last_wins = 0
        self.last_losses = 0

    def update_generation_stats(self, best_fitness, wins, losses):
        # Se llama una vez por generación para actualizar los stats.
        self.best_fitness_log = f"{best_fitness:.2f}"
        self.results_graph.add_generation_result(wins, losses)

    def draw(self, screen, population, gen_num, ind_num):
        # Se llama en cada frame del bucle principal.

        # Prepara los strings de texto dinámico
        gen_text = f"GENERACION: {gen_num} / {population.generations}"
        ind_text = f"INDIVIDUO: {ind_num} / {population.size}"

        # Prepara los strings de parámetros (podrían cambiar si se ajusta en vivo)
        elite_text = f"Elitismo: {population.elite_percentage * 100:.0f}%"
        mutation_text = f"Mutacion: {population.mutation_rate * 100:.1f}%"

        # Dibuja los componentes
        self.log_display.draw(
            screen, gen_text, ind_text, self.best_fitness_log, elite_text, mutation_text
        )
        self.results_graph.draw(screen)
