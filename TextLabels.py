import pyglet
from Quads import Quad


class GameMenu:
    def __init__(self, resolution, option_list):
        self.label_list = []
        self.resolution = resolution
        self.nav_pos = [(resolution[0] / 2) - 150, 430]
        for i in range(len(option_list)):
            self.label_list.append(pyglet.text.Label(option_list[i], font_name="Tempus Sans ITC", font_size=60,
                                                     x=resolution[0] / 2, y=400 - (i * 100), anchor_x="center",
                                                     anchor_y="center",
                                                     color=[255, 255, 255, 255], bold=True))
        self.menu_bg = Quad([0, resolution[1]], resolution, [10, 10, 10, 128] * 4)
        self.menu_nav = Quad(self.nav_pos, [300, 75], [100, 10, 0, 128] * 4)
        self.nav_ofs = 0

    def draw(self):
        self.menu_bg.draw()
        for label in self.label_list:
            label.draw()
        self.menu_nav.draw()

    def update(self, offset):
        self.nav_pos[1] -= offset
        self.menu_nav = Quad(self.nav_pos, [300, 80], [100, 10, 0, 128] * 4)
