"""
GameEngine: owns the helicopter, obstacles, and active game state.

The engine detects collisions with obstacle walls and ends the game on
an unshielded hit. It tracks distance while play is active and supports
a shield that absorbs one obstacle collision before becoming inactive.
"""

import random
import pygame

from game.helicopter import Helicopter
from game.obstacle import Obstacle
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 90
GAP_HEIGHT = 150
WALL_WIDTH = 60
SCROLL_SPEED = 3


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.helicopter = Helicopter(x=100, y=HEIGHT / 2)
        self.obstacles = []
        self.frames_until_spawn = 0
        self.distance = 0
        self.shield_active = False
        self.game_over = False
        self._absorbed_obstacles = set()

    def _spawn_obstacle(self):
        margin = 60
        gap_y = random.randint(margin + GAP_HEIGHT // 2, HEIGHT - margin - GAP_HEIGHT // 2)
        self.obstacles.append(Obstacle(
            x=WIDTH, gap_y=gap_y, gap_height=GAP_HEIGHT,
            wall_width=WALL_WIDTH, screen_height=HEIGHT, speed=SCROLL_SPEED,
        ))

    def handle_input(self, keys_pressed):
        if not self.game_over:
            self.helicopter.handle_input(keys_pressed)

    def handle_keydown(self, key):
        if key == pygame.K_r and self.game_over:
            self.reset()
        elif key == pygame.K_SPACE and not self.game_over:
            self.shield_active = True

    def update(self):
        if self.game_over:
            return

        self.helicopter.update(HEIGHT)

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_obstacle()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for obstacle in self.obstacles:
            obstacle.update()
        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]
        self.distance += SCROLL_SPEED
        self._check_collisions()

    def _check_collisions(self):
        helicopter_rect = self.helicopter.get_rect()
        colliding_obstacles = {
            obstacle for obstacle in self.obstacles
            if helicopter_rect.colliderect(obstacle.get_top_rect())
            or helicopter_rect.colliderect(obstacle.get_bottom_rect())
        }
        self._absorbed_obstacles.intersection_update(colliding_obstacles)

        for obstacle in colliding_obstacles:
            if obstacle in self._absorbed_obstacles:
                continue
            if self.shield_active:
                self.shield_active = False
                self._absorbed_obstacles.add(obstacle)
            else:
                self.game_over = True
                return

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(
            surface, self.helicopter, self.obstacles, self.distance,
            self.shield_active, self.game_over, font,
        )
