"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (140, 200, 230)
COLOR_HELI = (60, 60, 70)
COLOR_OBSTACLE = (70, 150, 80)
COLOR_TEXT = (20, 20, 20)
COLOR_SHIELD = (30, 180, 220)


def draw_scene(surface, helicopter, obstacles, distance=0, shield_active=False, game_over=False, font=None):
    surface.fill(COLOR_BG)
    for obstacle in obstacles:
        pygame.draw.rect(surface, COLOR_OBSTACLE, obstacle.get_top_rect())
        pygame.draw.rect(surface, COLOR_OBSTACLE, obstacle.get_bottom_rect())
    helicopter_rect = helicopter.get_rect()
    pygame.draw.rect(surface, COLOR_HELI, helicopter_rect, border_radius=4)
    if shield_active:
        pygame.draw.rect(surface, COLOR_SHIELD, helicopter_rect.inflate(10, 10), 2, border_radius=7)
    if font is not None:
        draw_text(surface, font, f"Distance: {int(distance)}", (12, 12))
        if shield_active:
            draw_text(surface, font, "SHIELD ACTIVE", (12, 40), COLOR_SHIELD)
        if game_over:
            draw_banner(surface, font, "GAME OVER")
            final_distance = font.render(f"Final distance: {int(distance)}", True, COLOR_TEXT)
            restart_hint = font.render("Press R to restart", True, COLOR_TEXT)
            center_x = surface.get_width() // 2
            center_y = surface.get_height() // 2
            surface.blit(final_distance, final_distance.get_rect(center=(center_x, center_y + 30)))
            surface.blit(restart_hint, restart_hint.get_rect(center=(center_x, center_y + 58)))


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (180, 40, 40))
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(surf, rect)
