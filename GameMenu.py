import pyglet
from Quads import Quad, Quad_Right
from pyglet.sprite import Sprite
from DisplayObjects import preload_image
from ShipData import get_ship_stats, get_ship_quad_stats

resolution = ()
image_path = "res/sprites/"

all_ships = get_ship_stats()

p1_ship1_stats = all_ships[0]
p1_ship2_stats = all_ships[1]
p1_ship3_stats = all_ships[2]
p2_ship1_stats = all_ships[3]
p2_ship2_stats = all_ships[4]
p2_ship3_stats = all_ships[5]

all_quads = get_ship_quad_stats()

ship1_stat_quad_sizes = all_quads[0]
ship2_stat_quad_sizes = all_quads[1]
ship3_stat_quad_sizes = all_quads[2]


class GameMenu:
    def __init__(self, resolution1, option_list):
        global resolution
        resolution = resolution1
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
        self.nav_step = 100

    def draw(self):
        self.menu_bg.draw()
        for label in self.label_list:
            label.draw()
        self.menu_nav.draw()
        pyglet.text.Label("DUAL", font_name="Tempus Sans ITC", font_size=resy(200),
                          x=resolution[0] / 2, y=resy(850), anchor_x="center",
                          anchor_y="center",
                          color=[200, 255, 255, 255], bold=True).draw()

    def update(self, offset):
        self.nav_pos[1] -= offset
        self.menu_nav = Quad(self.nav_pos, [300, 80], [100, 10, 0, 128] * 4)


def resx(x):
    return (resolution[0] * (x)) / 1920


def resy(y):
    return (resolution[1] * (y)) / 1080


class SelectionMenu:
    def __init__(self, resolution1, option_list):
        global resolution
        resolution = resolution1
        self.p1_label_list = []
        self.p2_label_list = []
        self.resolution = resolution
        self.p1_nav_pos = [resx(100), resy(850)]
        self.p2_nav_pos = [resx(1520), resy(850)]
        for i in range(len(option_list)):
            self.p1_label_list.append(pyglet.text.Label(option_list[i], font_name="Tempus Sans ITC", font_size=resx(60),
                                                        x=self.p1_nav_pos[0] + resx(150),
                                                        y=self.p1_nav_pos[1] - (i * 100) - 35, anchor_x="center",
                                                        anchor_y="center",
                                                        color=[255, 255, 255, 255], bold=True))
        for i in range(len(option_list)):
            self.p2_label_list.append(pyglet.text.Label(option_list[i], font_name="Tempus Sans ITC", font_size=resx(60),
                                                        x=self.p2_nav_pos[0] + resx(150),
                                                        y=self.p2_nav_pos[1] - (i * 100) - 35, anchor_x="center",
                                                        anchor_y="center",
                                                        color=[255, 255, 255, 255], bold=True))
        self.menu_bg = Quad([0, resolution[1]], resolution, [10, 10, 10, 128] * 4)
        self.p1_menu_nav = Quad(self.p1_nav_pos, [300, 85], [100, 10, 0, 128] * 4)
        self.p2_menu_nav = Quad(self.p2_nav_pos, [300, 85], [100, 10, 0, 128] * 4)
        self.p1_nav_ofs = 0
        self.p2_nav_ofs = 0
        self.nav_step = 100

    def draw(self):
        self.menu_bg.draw()
        for label in self.p1_label_list:
            label.draw()
        for label in self.p2_label_list:
            label.draw()
        self.p1_menu_nav.draw()
        self.p2_menu_nav.draw()
        self.draw_text()

        if self.p1_nav_ofs == 0:
            self.draw_ship1(200, 150)
            self.p1_draw_ship1_stats()
        elif self.p1_nav_ofs == 100:
            self.draw_ship2(200, 150)
            self.p1_draw_ship2_stats()
        elif self.p1_nav_ofs == 200:
            self.draw_ship3(200, 150)
            self.p1_draw_ship3_stats()

        if self.p2_nav_ofs == 0:
            self.draw_ship1(1656, 150)
            self.p2_draw_ship1_stats()
        elif self.p2_nav_ofs == 100:
            self.draw_ship2(1656, 150)
            self.p2_draw_ship2_stats()
        elif self.p2_nav_ofs == 200:
            self.draw_ship3(1656, 150)
            self.p2_draw_ship3_stats()

        pyglet.text.Label("Esc", font_name="Tempus Sans ITC", font_size=resx(15),
                          x=0, y=resolution[1], anchor_y='top',
                          color=[255, 255, 255, 75], bold=True).draw()

    def update_p1(self, offset):
        self.p1_nav_pos[1] -= offset
        self.p1_menu_nav = Quad(self.p1_nav_pos, [300, 80], [100, 10, 0, 128] * 4)

    def update_p2(self, offset):
        self.p2_nav_pos[1] -= offset
        self.p2_menu_nav = Quad(self.p2_nav_pos, [300, 80], [100, 10, 0, 128] * 4)

    def draw_text(self):
        dis_y = resy(450)
        dis_x = resx(350)
        f_size = resx(25)
        t_gap = resy(40)
        p_gap = resx(1220)

        pyglet.text.Label("PLAYER 1", font_name="Tempus Sans ITC", font_size=resx(100),
                          x=resx(300), y=resy(1000), anchor_x="center",
                          anchor_y="center",
                          color=[255, 255, 255, 255], bold=True).draw()
        pyglet.text.Label("PLAYER 2", font_name="Tempus Sans ITC", font_size=resx(100),
                          x=resx(1620), y=resy(1000), anchor_x="center",
                          anchor_y="center",
                          color=[255, 255, 255, 255], bold=True).draw()

        for i in range(2):
            xanchor = 'right' if i == 0 else 'left'
            pyglet.text.Label("SHIP SPEED", font_name="Tempus Sans ITC", font_size=f_size,
                              x=dis_x + (i * p_gap), y=dis_y, anchor_x=xanchor,
                              color=[255, 255, 255, 255], bold=True).draw()
            pyglet.text.Label("LASER SPEED", font_name="Tempus Sans ITC", font_size=f_size,
                              x=dis_x + (i * p_gap), y=dis_y - (t_gap), anchor_x=xanchor,
                              color=[255, 255, 255, 255], bold=True).draw()
            pyglet.text.Label("LASER RANGE", font_name="Tempus Sans ITC", font_size=f_size,
                              x=dis_x + (i * p_gap), y=dis_y - (t_gap * 2), anchor_x=xanchor,
                              color=[255, 255, 255, 255], bold=True).draw()
            pyglet.text.Label("DAMAGE TAKEN", font_name="Tempus Sans ITC", font_size=f_size,
                              x=dis_x + (i * p_gap), y=dis_y - (t_gap * 3), anchor_x=xanchor,
                              color=[255, 255, 255, 255], bold=True).draw()
            pyglet.text.Label("GAURD REGEN RATE", font_name="Tempus Sans ITC", font_size=f_size,
                              x=dis_x + (i * p_gap), y=dis_y - (t_gap * 4), anchor_x=xanchor,
                              color=[255, 255, 255, 255], bold=True).draw()

    def draw_ship1(self, x, y):
        Sprite(preload_image(image_path + "ship1.png"), x=resx(x), y=resy(y)).draw()

    def draw_ship2(self, x, y):
        Sprite(preload_image(image_path + "ship2.png"), x=resx(x), y=resy(y)).draw()

    def draw_ship3(self, x, y):
        Sprite(preload_image(image_path + "ship3.png"), x=resx(x), y=resy(y)).draw()

    def p1_draw_ship1_stats(self):
        dis_y = resy(470)
        dis_x = resx(400)
        for i in range(5):
            Quad([dis_x, dis_y - (i * 40)], [ship1_stat_quad_sizes[i], 20], [255, 0, 0, 255] * 4).draw()

    def p1_draw_ship2_stats(self):
        dis_y = resy(470)
        dis_x = resx(400)
        for i in range(5):
            Quad([dis_x, dis_y - (i * 40)], [ship2_stat_quad_sizes[i], 20], [255, 0, 0, 255] * 4).draw()

    def p1_draw_ship3_stats(self):
        dis_y = resy(470)
        dis_x = resx(400)
        for i in range(5):
            Quad([dis_x, dis_y - (i * 40)], [ship3_stat_quad_sizes[i], 20], [255, 0, 0, 255] * 4).draw()

    def p2_draw_ship1_stats(self):
        dis_y = resy(450)
        dis_x = resx(1520)
        for i in range(5):
            Quad_Right([dis_x, dis_y - (i * 40)], [ship1_stat_quad_sizes[i], 20], [255, 0, 0, 255] * 4).draw()

    def p2_draw_ship2_stats(self):
        dis_y = resy(450)
        dis_x = resx(1520)
        for i in range(5):
            Quad_Right([dis_x, dis_y - (i * 40)], [ship2_stat_quad_sizes[i], 20], [255, 0, 0, 255] * 4).draw()

    def p2_draw_ship3_stats(self):
        dis_y = resy(450)
        dis_x = resx(1520)
        for i in range(5):
            Quad_Right([dis_x, dis_y - (i * 40)], [ship3_stat_quad_sizes[i], 20], [255, 0, 0, 255] * 4).draw()


class ControlsMenu:
    def __init__(self):
        self.controls_text_file = open('ReadMe.txt', 'r')

    def draw(self):
        Quad([0, resolution[1]], resolution, [10, 10, 10, 128] * 4).draw()
        pyglet.text.Label("CONTROLS", font_name="Tempus Sans ITC", font_size=resx(100),
                          x=resolution[0] / 2, y=resolution[1] - resy(100), anchor_x='center', anchor_y='center',
                          color=[255, 255, 255, 255], bold=True).draw()
        yxs = 0
        xxs = resx(100)
        for text in self.controls_text_file:
            if text.strip() == 'PLAYER 2 CONTROLS':
                xxs = (resolution[0] / 2) + resx(100)
                yxs = 0
            pyglet.text.Label(text, font_name="Tempus Sans ITC", font_size=resx(26),
                              x=xxs, y=resolution[1] - resy(300 + yxs),
                              color=[255, 255, 255, 255], bold=True).draw()
            yxs += resy(35)
        pyglet.text.Label("Esc", font_name="Tempus Sans ITC", font_size=resx(20),
                          x=0, y=resolution[1], anchor_y='top',
                          color=[255, 255, 255, 75], bold=True).draw()
        self.controls_text_file.seek(0)


class AboutMenu:
    def __init__(self):
        self.about_text_file = open('about.txt')

    def draw(self):
        Quad([0, resolution[1]], resolution, [10, 10, 10, 128] * 4).draw()
        pyglet.text.Label("ABOUT", font_name="Tempus Sans ITC", font_size=resx(100),
                          x=resolution[0] / 2, y=resolution[1] - resy(100), anchor_x='center', anchor_y='center',
                          color=[255, 255, 255, 255], bold=True).draw()
        yxs = 0
        for text in self.about_text_file:
            pyglet.text.Label(text, font_name="Tempus Sans ITC", font_size=resx(27),
                              x=resx(100), y=resolution[1] - resy(300 + yxs),
                              color=[255, 255, 255, 255], bold=True).draw()
            yxs += resy(40)

        pyglet.text.Label("Esc", font_name="Tempus Sans ITC", font_size=resx(20),
                          x=0, y=resolution[1], anchor_y='top',
                          color=[255, 255, 255, 75], bold=True).draw()
        self.about_text_file.seek(0)


def draw_start_page(timer, max_timeout):
    pyglet.text.Label("SRINIVAS INSTITUTE OF TECHNOLOGY", font_name="Tempus Sans ITC", font_size=resx(50),
                      x=resolution[0] / 2, y=resolution[1] - resy(100), anchor_x='center', anchor_y='center',
                      color=[0, 255, 0, 255], bold=True).draw()
    pyglet.text.Label("Mangalore", font_name="Tempus Sans ITC", font_size=resx(20),
                      x=resolution[0] / 2, y=resolution[1] - resy(200), anchor_x='center', anchor_y='center',
                      color=[0, 255, 0, 255], bold=True).draw()
    pyglet.text.Label("COMPUTER GRAPHICS AND VISUALIZATION", font_name="Tempus Sans ITC", font_size=resx(20),
                      x=resolution[0] / 2, y=resolution[1] - resy(300), anchor_x='center', anchor_y='center',
                      color=[0, 255, 0, 255], bold=True).draw()
    pyglet.text.Label("MINI PROJECT ON", font_name="Tempus Sans ITC", font_size=resx(20),
                      x=resolution[0] / 2, y=resolution[1] - resy(400), anchor_x='center', anchor_y='center',
                      color=[0, 255, 0, 255], bold=True).draw()
    pyglet.text.Label("DUAL", font_name="Tempus Sans ITC", font_size=resy(100),
                      x=resolution[0] / 2, y=resolution[1] - resy(550), anchor_x="center",
                      anchor_y="center",
                      color=[200, 255, 255, 255], bold=True).draw()
    pyglet.text.Label("AN ARCADE SPACE SHOOTER GAME", font_name="Tempus Sans ITC", font_size=resy(20),
                      x=resolution[0] / 2, y=resolution[1] - resy(670), anchor_x="center",
                      anchor_y="center",
                      color=[200, 255, 255, 255], bold=True, multiline=True, width=500).draw()
    pyglet.text.Label("\t\t\t\t\t\tTEAM MEMBERS\n\n\tADITHYA KRISHNA\t\t\t\t\tMOHAMMAD HAFEEZ", font_name="Tempus Sans ITC", font_size=resy(20),
                      x=resolution[0] / 2, y=resolution[1] - resy(900), anchor_x="center",
                      anchor_y="center",
                      color=[0, 255, 0, 255], bold=True, multiline=True, width=800).draw()
    pyglet.text.Label(str(max_timeout - int(timer)+1), font_name="Tempus Sans ITC", font_size=resy(30),
                      x=resolution[0] / 2, y=resolution[1] - resy(1000), anchor_x="center",
                      anchor_y="center",
                      color=[255, 0, 0, 127], bold=True).draw()