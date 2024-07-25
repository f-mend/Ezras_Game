import pygame
from UI.ColorPalette import *

# Define Colors
palette = ColorPalette()

class HealthBar:
    def __init__(self, screen, x, y, curr_hp, max_hp):
        self._screen = screen
        self._x = x
        self._y = y
        self._curr_hp = curr_hp
        self._max_hp = max_hp
    
    def draw(self, hp):
        # Update with new health
        self._curr_hp = hp
        # Calculate health ratio
        ratio = self._curr_hp / self._max_hp
        # Draw health text
        health_font = pygame.font.Font(None, 40)
        instruction_text = health_font.render(f"{self._curr_hp}/{self._max_hp}", True, palette.get_color_by_name('black'))
        self._screen.blit(instruction_text, (self._x+45, self._y - 30))
        # Draw health bar background
        pygame.draw.rect(self._screen, palette.get_color_by_name('red'), (self._x, self._y, 150, 20))
        # Draw health bar foreground
        pygame.draw.rect(self._screen, palette.get_color_by_name('green'), (self._x, self._y, 150 * ratio, 20))