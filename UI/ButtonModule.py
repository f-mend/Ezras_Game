import pygame

class Button:
    def __init__(self, screen, text, x, y, width, height, color_light, color_dark, action=None, transition= None):
        self._screen = screen
        self._text = text
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._color_light = color_light
        self._color_dark = color_dark
        self._action = action
        self._transition = transition

    def draw(self, mouse):
        # if mouse is hovered on button, change color
        if self._x <= mouse[0] <= self._x + self._width and self._y <= mouse[1] <= self._y + self._height:
            pygame.draw.rect(self._screen, self._color_light, [self._x, self._y, self._width, self._height])
        else:
            pygame.draw.rect(self._screen, self._color_dark, [self._x, self._y, self._width, self._height])

        # superimposing the text onto the button
        smallfont = pygame.font.SysFont('Corbel', 35)
        text_surface = smallfont.render(self._text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self._x + self._width / 2, self._y + self._height / 2))
        self._screen.blit(text_surface, text_rect)

    def handle_event(self, mouse):
        #if event.type == pygame.MOUSEBUTTONDOWN:
        if self._x <= mouse[0] <= self._x + self._width and self._y <= mouse[1] <= self._y + self._height:
            if self._action:
               return self._action()
            if self._transition:
                return self._transition
        return None