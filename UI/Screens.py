import pygame
from .ButtonModule import *
from .ColorPalette import *
from .HealthBar import *

# Set up the display
screen_width = 720
screen_height = 720
screen_resolution = (screen_width, screen_height)
screen = pygame.display.set_mode(screen_resolution)
# Clock object to manage frame rate
clock = pygame.time.Clock()
# Learn .convert_alpha(), used for transparency in conjunction with png

class Screen:
    def __init__(self):
        self._mouse = pygame.mouse.get_pos()
        self._palette = ColorPalette()

    def handle_events(self, event, combat_manager):
        pass

    def update(self, keys, player = None, enemy= None, combat_manager = None):
        self._mouse = pygame.mouse.get_pos()
        
    def draw(self, screen, player=None, enemy=None):
        pass

class MainMenu(Screen):
    def __init__(self):
        super().__init__()
        self._quit_button = Button(screen, 'Quit', screen_width // 2 - 70, screen_height // 2, 140, 40, self._palette.get_color_by_name('grey_light'), self._palette.get_color_by_name('grey_dark'), pygame.quit,None)
        self._play_button = Button(screen, 'Play', screen_width // 2 - 70, screen_height // 2, 140, 40, self._palette.get_color_by_name('grey_light'), self._palette.get_color_by_name('grey_dark'), None,'game')

    def handle_events(self, event, combat_manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self._play_button.handle_event(self._mouse)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Press Enter to start the game
                return 'game'
        return None

    def update(self, keys, player = None, enemy= None, combat_manager = None):
        super().update(keys, player, enemy, combat_manager = None)

    def draw(self, screen, player=None, enemy=None):
        screen.fill(self._palette.get_color_by_name('soft_blue'))
        # Title
        title_font = pygame.font.Font(None, 74)
        title_text = title_font.render("Ezra Rising: the Siloing", True, self._palette.get_color_by_name('black'))
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 4 - title_text.get_height() // 2))
        # Instructions
        self._play_button.draw(self._mouse)

class PauseMenu(Screen):
    def __init__(self):
        super().__init__()
        self._quit_button = Button(screen, 'Quit', screen_width // 2 - 70, screen_height // 2, 140, 40, self._palette.get_color_by_name('grey_light'), self._palette.get_color_by_name('grey_dark'), pygame.quit)
    
    def handle_events(self, event, combat_manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._quit_button.handle_event(event,self._mouse)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Press Enter to start the game
                return 'game'
            if event.key == pygame.K_ESCAPE:  # Press Enter to start the game
                return 'quit_menu'

    def update(self, keys, player = None, enemy= None, combat_manager= None):
        super().update(keys, player, enemy, combat_manager= None)

    def draw(self, screen, player=None, enemy=None):
        screen.fill(self._palette.get_color_by_name('soft_blue'))
        title_font = pygame.font.Font(None, 74)
        title_text = title_font.render("PAUSED", True, self._palette.get_color_by_name('black'))
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 5 - title_text.get_height() // 2))
        # Instructions_Resume
        instruction_font = pygame.font.Font(None, 40)
        instruction_text = instruction_font.render("Hit Enter to Resume", True, self._palette.get_color_by_name('red'))
        screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, screen_height // 4 - instruction_text.get_height() // 2))
        # Instructions_Quit
        self._quit_button.draw(self._mouse)

class Gamescreen(Screen):
    def __init__(self):
        super().__init__()
        self._player_x, self._player_y = 100, 600
        self._enemy_x, self._enemy_y = 400, 100
        self._enemies = {}

    def handle_events(self, event, combat_manager):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Press ESC to pause
                return 'pause_menu'
        return None

    def update(self, keys, player, enemies= None, combat_manager = None):
        super().update(keys, player, enemies, combat_manager= None)
        for id, enemy in enumerate(enemies):
            var_name = f"_enemy_{id}"
            self._enemies[var_name] = enemy

        player.update_unit_position(self._player_x, self._player_y)
        for enemy in enemies:
            enemy.update_unit_position(self._enemy_x, self._enemy_y)

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self._player_y -= player._move_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self._player_y += player._move_speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self._player_x -= player._move_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self._player_x += player._move_speed


        if player._collision_rect.colliderect(enemies[0]._collision_rect):
            return 'combat'

    def draw(self, screen, player, enemies=None):
        screen.blit(pygame.image.load('Assets/Backgrounds/overworld_map.bmp'), (0,0))
        screen.blit(player._scaled_image, player._collision_rect.topleft)
        screen.blit(enemies[0]._scaled_image, enemies[0]._collision_rect.topleft)
                   
class CombatScreen(Screen):
    def __init__(self):
        super().__init__()
        # shared y var to line up enemies and hp bars
        self._hp_bar_y = 550
        self._image_bar_y = 350
        self._player_x, self._player_y = 50, self._image_bar_y
        # mouse icon control
        self._mouse_show = True
        image = pygame.image.load('Assets/Icon/sword_cursor.png')
        self._sword_cursor_image = pygame.transform.scale(image, (60,60))
        image = pygame.image.load('Assets/Icon/potion_cursor.png')
        self._potion_cursor_image = pygame.transform.scale(image, (60,60))
        #self._mouse_state = [0,True]
        self._attack_mouse = False
        self._potion_mouse = False
        image = []
        # positions for frame check
        self._enemy_positions = {}
        
    def handle_events(self, event, combat_manager):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Press ESC to pause
                return 'pause_menu'
        if event.type == pygame.MOUSEBUTTONDOWN:
                if self._attack_mouse == True:
                    combat_manager._player.unit_attacks(combat_manager._target)
                    combat_manager._turn_counter += 1
                elif self._potion_mouse == True:
                    combat_manager._player.unit_heals()
                    combat_manager._turn_counter += 1

    def update(self, keys, player = None, enemies= None, combat_manager = None):
        super().update(keys, player, enemies, combat_manager)
        player.update_unit_position(self._player_x, self._player_y)
        #combat_manager.did_game_end()

        for i, enemy in enumerate(enemies):
            if combat_manager._turn_counter % 2 != 0:
                if enemy._is_alive:
                    combat_manager.set_target(combat_manager._player)
                    enemy.unit_attacks(combat_manager._target)

            x_offset = (i * 200) 
            enemy.update_unit_position(550 - x_offset, self._image_bar_y)
            self._enemy_positions[f"enemy_{i}"] = enemy._collision_rect

        if combat_manager._turn_counter % 2 != 0:
            combat_manager._turn_counter +=1


            # move this outside the loop, store all locations in a hashmap and then check if mouse location is a key in the map. one check per update vs 2 
        self._mouse_show, self._attack_mouse, self._potion_mouse = True, False, False  # Default to show the mouse
        if player._collision_rect.collidepoint(self._mouse):
                self._mouse_show = False
                self._potion_mouse = True
                combat_manager.set_target(player)
                # print(f'Player is now the target')
        for id, rect in enumerate(self._enemy_positions.values()):
            if rect.collidepoint(self._mouse):
                if combat_manager._selected_enemies[id]._is_alive:
                    self._mouse_show = False
                    self._attack_mouse = True
                    combat_manager.set_target(combat_manager._selected_enemies[id])
                # print(f'{combat_manager._target._enemy_type} is now the target')
        pygame.mouse.set_visible(self._mouse_show)
        if combat_manager.did_game_end():
            pygame.mouse.set_visible(True)
            return combat_manager.did_game_end()

    def draw(self, screen, player=None, enemies=None):
        screen.blit(pygame.image.load('Assets/Backgrounds/combat_arena.png'), (0,0))
        
        
        player_health_bar = HealthBar(screen, player._x, self._hp_bar_y, player._curr_hp, player._max_hp)
        player_health_bar.draw(player._curr_hp)
        if player._is_alive:
            screen.blit(player._scaled_image, (player._x,self._image_bar_y))
            

            if self._potion_mouse:
                sword_cursor_scaled = pygame.transform.scale(self._sword_cursor_image, (60,60))
                #show potion in place of mouse cursor
                screen.blit(self._potion_cursor_image, (self._mouse[0]-30,self._mouse[1]-30))
                self._heal = True

        for enemy in enemies:
            enemy_health_bar = HealthBar(screen, enemy._x, self._hp_bar_y, enemy._curr_hp, enemy._max_hp)
            enemy_health_bar.draw(enemy._curr_hp)
            if enemy._is_alive:            
                screen.blit(enemy._scaled_image, (enemy._x, enemy._y))
                
            if self._attack_mouse:
                #show sword in place of mouse cursor
                screen.blit(self._sword_cursor_image, (self._mouse[0]-30,self._mouse[1]-30))
                self._attack = True                               

class GameEnd(Screen):
    def __init__(self):
        super().__init__()
        # -1 player lost, 0 default, 1 player won
        self._did_player_win = 0
        self._quit_button = Button(screen, 'Quit', 155, screen_height // 2, 140, 40, self._palette.get_color_by_name('grey_light'), self._palette.get_color_by_name('grey_dark'), pygame.quit)
        self._restart_button = Button(screen, 'Restart', 415, screen_height // 2, 140, 40, self._palette.get_color_by_name('grey_light'), self._palette.get_color_by_name('grey_dark'),  None, 'main_menu')

    def handle_events(self, event, combat_manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._quit_button.handle_event(self._mouse):
                return self._quit_button.handle_event(self._mouse)
            if self._restart_button.handle_event(self._mouse):
                combat_manager.generate_new_game()
                return self._restart_button.handle_event(self._mouse)

    def update(self, keys, player = None, enemy= None, combat_manager= None):
        super().update(keys, player, enemy, combat_manager= None)
        self._did_player_win = combat_manager._did_player_win

    def draw(self, screen, player=None, enemy=None):
        screen.fill(self._palette.get_color_by_name('black'))
        title_font = pygame.font.Font(None, 74)
        if self._did_player_win == 1:
            game_text = title_font.render("YOU WON!!!!", True, self._palette.get_color_by_name('white'))
            screen.blit(game_text, (screen_width // 2 - game_text.get_width() // 2, 300))
        elif self._did_player_win == -1:
            game_text = title_font.render("YOU LOST! :(", True, self._palette.get_color_by_name('white'))
            screen.blit(game_text, (screen_width // 2 - game_text.get_width() // 2, 300))        
        self._quit_button.draw(self._mouse)
        self._restart_button.draw(self._mouse)
                    
# Screen manager to handle transitions and screen states
class ScreenManager:
    def __init__(self):
        # Initialize the screens with their classes instead of instances
        self._screens = {
            'main_menu': MainMenu,
            'pause_menu': PauseMenu,
            'game': Gamescreen,
            'combat': CombatScreen,
            'game_ended': GameEnd,
        }
        self._current_screen = self._screens['main_menu']()

    def handle_events(self, event, combat_manager):
        new_screen = self._current_screen.handle_events(event, combat_manager)
        if new_screen:
            self._set_current_screen(new_screen)

    def update(self, keys, player=None, enemies=None, combat_manager=None):
        new_screen = self._current_screen.update(keys, player, enemies, combat_manager)
        if new_screen:
            self._set_current_screen(new_screen)

    def draw(self, screen, player, enemy=None):
        self._current_screen.draw(screen, player, enemy)

    def _set_current_screen(self, new_screen):
        # Ensure new_screen is a valid screen key and instantiate the screen class
        if new_screen in self._screens:
            self._current_screen = self._screens[new_screen]()
        else:
            raise ValueError(f"Invalid screen: {new_screen}")
