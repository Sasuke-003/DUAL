from pyglet.gl import *
from pyglet.sprite import Sprite


image_path = "res/sprites/"
sound_path = "res/sounds/"



def preload_image(image):
    img = pyglet.image.load(image)
    return img


class DisplayObjects:
    def __init__(self, pos_x, pos_y, image_url=None):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = 0
        self.vel_y = 0
        if image_url is not None:
            self.sprite = image_url
            self.sprite.x = self.pos_x
            self.sprite.y = self.pos_y
            self.width = self.sprite.width
            self.height = self.sprite.height

    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        self.pos_x += self.vel_x * dt
        self.pos_y += self.vel_y * dt
        self.sprite.x = self.pos_x
        self.sprite.y = self.pos_y


class DisplayPlayers:
    def __init__(self, pos_x, pos_y, fire_type="auto"):
        # PLAYER COORDINATES
        self.pos_x = pos_x
        self.pos_y = pos_y

        # PLAYER MOVEMENT INITIALIZATIONS
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.gaurding = False

        # PLAYER SHOOTING INITIALIZATIONS
        self.fire = False
        self.fire_type = fire_type
        self.fire_rate = 0
        self.laser_list = []
        self.laser_sound = pyglet.media.load(sound_path + "player_gun.wav", streaming=False)
        self.sp_laser_list = []

        # PLAYER SPRITE IMAGE INITIALIZATIONS
        self.sprite = None
        self.width = 0
        self.height = 0

        # PLAYER EXPLOSION INITIALIZATIONS
        self.exp_list = []
        self.exp_timer = []

        # PLAYER HEALTH INITIALIZATIONS
        self.hp = None
        self.dhp = None

        # PLAYER GAURD INITIALIZATIONS
        self.gaurd = None
        self.energy_shield = Sprite(preload_image(image_path + "energy_shield.png"))

        # PLAYER STATS
        self.speed = 300
        self.laser_speed = 600
        self.laser_range = 800
        self.damage_taken = 20
        self.gaurd_regen_rate = 0.3

        self.sp_damage_taken = 50

        self.lost = False

    def draw(self, game_started):
        if not self.lost:
            if self.sprite is not None:
                self.sprite.draw()
            if self.dhp is not None and game_started:
                self.dhp.draw()
            if self.hp is not None and game_started:
                self.hp.draw()
            if self.gaurd is not None and game_started:
                self.gaurd.draw()

    def update(self, dt):
        self.sprite.x = self.pos_x
        self.sprite.y = self.pos_y

    def set_stats(self, stats):
        self.speed, self.laser_speed, self.laser_range, self.damage_taken, self.gaurd_regen_rate, self.sprite = stats
        self.sprite.x = self.pos_x
        self.sprite.y = self.pos_y
        self.width = self.sprite.width
        self.height = self.sprite.height

    def draw_shield(self, x, y):
        self.energy_shield.x = x
        self.energy_shield.y = y
        self.energy_shield.draw()

class DisplayLasers:
    def __init__(self, pos_x, pos_y, image_url=None):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.initial_pos_x = pos_x
        self.initial_pos_y = pos_y
        if image_url is not None:
            self.sprite = image_url
            self.sprite.x = self.pos_x
            self.sprite.y = self.pos_y
            self.width = self.sprite.width
            self.height = self.sprite.height

    def draw(self):
        self.sprite.draw()

    def update(self):
        self.sprite.x = self.pos_x
        self.sprite.y = self.pos_y


class Lasers:
    def __init__(self, pos_x, pos_y, size, color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.initial_pos_x = pos_x
        self.initial_pos_y = pos_y
        self.size = size
        self.indices = [0, 1, 2, 3]
        self.vertex = [self.pos_x, self.pos_y, 0.0,
                       self.pos_x + self.size[0], self.pos_y, 0.0,
                       self.pos_x + self.size[0], self.pos_y - self.size[1], 0.0,
                       self.pos_x, self.pos_y - self.size[1], 0.0]
        self.color = color
        self.vertices = pyglet.graphics.vertex_list_indexed(4, self.indices, ('v3f', self.vertex), ('c4B', self.color))

    def __del__(self):
        print("destroyed")

    def draw(self):
        self.vertices.draw(GL_QUADS)

    def update(self):
        self.vertex = [self.pos_x, self.pos_y, 0.0,
                       self.pos_x + self.size[0], self.pos_y, 0.0,
                       self.pos_x + self.size[0], self.pos_y - self.size[1], 0.0,
                       self.pos_x, self.pos_y - self.size[1], 0.0]
        self.vertices = pyglet.graphics.vertex_list_indexed(4, self.indices, ('v3f', self.vertex), ('c4B', self.color))


