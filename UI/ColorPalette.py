class ColorPalette:
    def __init__(self):
        self.colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'green' : (0, 255, 0),
            'blue': (0, 0, 255),
            'soft_blue': (173, 216, 230),
            'grey_light': (170, 170, 170),
            'grey_dark': (100, 100, 100)
        }

    def get_color_by_name(self, name):
        return self.colors.get(name, None)

    def get_all_colors(self):
        return self.colors