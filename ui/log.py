# def draw_ui(current_gen, current_ind, best_fitness):
#     """Dibuja el panel de información del AG a la derecha del grid."""

#     # Posición inicial del texto en el panel UI
#     x_pos = GRID_WIDTH + 30
#     y_pos = 50
#     line_height = 45  # Espacio entre líneas

#     # --- Título ---
#     title_surface = font.render("--- LOG DEL AG ---", True, YELLOW)
#     screen.blit(title_surface, (x_pos, y_pos))
#     y_pos += line_height * 1.5  # Deja un espacio extra

#     # --- Información de Generación ---
#     gen_text = f"GENERACION: {current_gen} / {GENERATIONS}"
#     gen_surface = font.render(gen_text, True, YELLOW)
#     screen.blit(gen_surface, (x_pos, y_pos))
#     y_pos += line_height

#     # --- Información de Individuo ---
#     ind_text = f"INDIVIDUO: {current_ind} / {POPULATION_SIZE}"
#     ind_surface = font.render(ind_text, True, YELLOW)
#     screen.blit(ind_surface, (x_pos, y_pos))
#     y_pos += line_height * 1.5

#     # --- Información de Fitness ---
#     fit_text = f"MEJOR FITNESS (GEN PREVIA):"
#     fit_surface = font.render(fit_text, True, YELLOW)
#     screen.blit(fit_surface, (x_pos, y_pos))
#     y_pos += line_height

#     fit_val_text = f"{best_fitness}"
#     fit_val_surface = font.render(fit_val_text, True, YELLOW)
#     screen.blit(fit_val_surface, (x_pos + 20, y_pos))  # Indentado
#     y_pos += line_height * 1.5

#     # --- Información de Parámetros ---
#     param_text = "PARAMETROS:"
#     param_surface = font.render(param_text, True, YELLOW)
#     screen.blit(param_surface, (x_pos, y_pos))
#     y_pos += line_height

#     # Lee el valor por defecto de la tasa de mutación
#     try:
#         mut_rate = population.mutate.__defaults__[0]
#         mut_text = f"Tasa Mutacion: {(mut_rate * 100):.1f}%"
#     except (AttributeError, TypeError, IndexError):
#         mut_text = "Tasa Mutacion: N/A"

#     mut_surface = font.render(mut_text, True, YELLOW)
#     screen.blit(mut_surface, (x_pos + 20, y_pos))
#     y_pos += line_height

#     # --- CAMBIO A TORNEO ---
#     # Lee el valor por defecto del tamaño del torneo
#     try:
#         # Asume que la función se llama 'select_parents_by_tournament'
#         tournament_size = population.select_parents_by_tournament.__defaults__[0]
#         torneo_text = f"Seleccion: Torneo (k={tournament_size})"
#     except (AttributeError, TypeError, IndexError):
#         # Fallback por si la función no existe o no tiene defaults
#         torneo_text = "Seleccion: Torneo"

#     torneo_surface = font.render(torneo_text, True, YELLOW)
#     screen.blit(torneo_surface, (x_pos + 20, y_pos))
#     # --- FIN CAMBIO ---


# # --- FIN FUNCIÓN UI ---
