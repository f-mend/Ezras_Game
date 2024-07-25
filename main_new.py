import pygame
import sys
from Backend.CombatEntities import *
from UI.Screens import *
from UI.ColorPalette import *


# Main game loop
def Main():
    running = True
    pygame.init()
    pygame.display.set_caption('Ezra Rising')
    palette = ColorPalette()
    screen_manager = ScreenManager()
    combat_manager = CombatantManager()
    combat_manager.generate_new_game()

    while running:
        keys = pygame.key.get_pressed()
        screen_manager.update(keys, combat_manager._player, combat_manager._selected_enemies, combat_manager)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            screen_manager.handle_events(event, combat_manager)
        # Clear the screenaS
       
        # Draw the current screen
        screen_manager.draw(screen, combat_manager._player, combat_manager._selected_enemies)
        # Update the display z
        pygame.display.flip()
        # Cap the frame rate
        clock.tick(60)
    pygame.quit()
    sys.exit()


Main()