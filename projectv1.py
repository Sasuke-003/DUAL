from pyglet.gl import *
from pyglet.window import FPSDisplay, key
from pyglet.sprite import Sprite
from DisplayObjects import *
from SpriteAnimations import SpriteAnimation
from Quads import Quad
from TextLabels import GameMenu

# resolution = (1200, 800)
image_path = "res/sprites/"
sound_path = "res/sounds/"


# GAME DETAILS
game_running = False
game_over = False
winner = None
game_options = False
game_credits = False
game_paused = False
game_menu_text = ["start", "controls", "credits", "exit"]
game_menu_nav_step = 100

# BG IMAGE DETAILS
space_scroll_speed = 50
space_bg_img = image_path + "space.jpg"

# PLAYER 1 DETAILS
p1_sprite = Sprite(preload_image(image_path + "player1.png"))
p1_pos_x = 100
p1_pos_y = 500
p1_speed = 300
p1_laser_img = image_path + "player1_laser.png"
p1_laser_speed = 600
p1_laser_range = 800
p1_fire_rate = 0.9  # min - 0    max - 1
p1_fire_type = "auto"
p1_base = [0, resolution[0] / 2]
p1_total_life = 550
p1_total_gaurd = 530
p1_damage_taken = 20
p1_hp_pos = [0, 790]
p1_hp_size = [p1_total_life, 20]
p1_hp_color = [0, 255, 0, 255] * 4
p1_hp_score = p1_total_life / p1_damage_taken
p1_gaurd_pos = [0, 760]
p1_gaurd_size = [p1_total_gaurd, 20]
p1_gaurd_color = [0, 0, 255, 255] * 4
p1_guard_consumption_rate = 2
p1_gaurd_regen_rate = 0.3
p1_dhp_pos = p1_hp_pos.copy()
p1_dhp_size = p1_hp_size.copy()
p1_dhp_color = [255, 0, 0, 255]*4

# PLAYER 2 DETAILS
p2_sprite = Sprite(preload_image(image_path + "player2.png"))
p2_pos_x = 1000
p2_pos_y = 500
p2_speed = 300
p2_laser_img = image_path + "player2_laser.png"
p2_laser_speed = 600
p2_laser_range = 800
p2_fire_rate = 0.9  # min - 0    max - 1
p2_fire_type = "auto"
p2_base = [resolution[0] / 2, resolution[0]]
p2_total_life = 550
p2_total_gaurd = 530
p2_damage_taken = 20
p2_hp_pos = [resolution[0] - p2_total_life, 790]
p2_hp_size = [p2_total_life, 20]
p2_hp_color = [0, 255, 0, 255] * 4
p2_hp_score = p2_total_life / p2_damage_taken
p2_gaurd_pos = [resolution[0] - p2_total_gaurd, 760]
p2_gaurd_size = [p2_total_gaurd, 20]
p2_gaurd_color = [0, 0, 255, 255] * 4
p2_guard_consumption_rate = 2
p2_gaurd_regen_rate = 0.3
p2_dhp_pos = p2_hp_pos.copy()
p2_dhp_size = p2_hp_size.copy()
p2_dhp_color = [255, 0, 0, 255]*4

# EXPLOSION DETAILS
explosion_img = image_path + "explosion.png"
explosion_time = 15  # in ms
exp_sound = pyglet.media.load(sound_path + "exp_01.wav", streaming=False)


class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):

        # WINDOW INITIALIZATIONS
        super().__init__(*args, **kwargs)
        self.frame_rate = 1 / 60.0
        self.fps_display = FPSDisplay(self)
        self.fps_display.label.font_size = 50
        self.nav_ofs = 0

        # MAKING THE PRIMITIVE DRAWINGS TRANSPARENT
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.menu = GameMenu(resolution, game_menu_text)

        # SPACE BG INITIALIZATIONS
        self.space_list = []
        self.space_img = preload_image(space_bg_img)
        for i in range(2):
            self.space_list.append(DisplayObjects(0, i * 1200, Sprite(self.space_img)))
        for space in self.space_list:
            space.vel_y = -space_scroll_speed

        # PLAYER INITIALIZATIONS
        self.player1 = DisplayPlayers(p1_pos_x, p1_pos_y, p1_sprite, p1_speed, p1_laser_img, p1_fire_type)

        self.player2 = DisplayPlayers(p2_pos_x, p2_pos_y, p2_sprite, p2_speed, p2_laser_img, p2_fire_type)

        self.player1.laser_sound.play()

        self.p1_hp = Quad(p1_hp_pos, p1_hp_size, p1_hp_color, 'p1')
        self.p2_hp = Quad(p2_hp_pos, p2_hp_size, p2_hp_color, 'p2')

        self.p1_gaurd = Quad(p1_gaurd_pos, p1_gaurd_size, p1_gaurd_color, 'p1')
        self.p2_gaurd = Quad(p2_gaurd_pos, p2_gaurd_size, p2_gaurd_color, 'p2')

        self.p1_dhp = Quad(p1_dhp_pos, p1_dhp_size, p1_dhp_color, 'p1')
        self.p2_dhp = Quad(p2_dhp_pos, p2_dhp_size, p2_dhp_color, 'p2')

    def on_resize(self, width, height):
        width = max(1, width)
        height = max(1, height)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)

    def on_key_press(self, symbol, modifiers):
        global game_running, game_options, game_credits, game_paused
        if symbol == key.ESCAPE:
            if game_options:
                game_options = False
            if game_credits:
                game_credits = False

            # FOR PAUSING THE GAME
            if game_running and not game_paused:
                game_paused = True
                game_running = False
                self.menu = GameMenu(resolution, ["resume", "controls", "credits", "exit"])

        if symbol == key.ENTER:

            # FOR STARTING THE GAME
            if not game_running and not game_over and self.nav_ofs == 0:
                game_running = True
                game_paused = False

            # FOR ENTERING THE CONTROLS MENU
            elif not game_running and not game_over and self.nav_ofs == 100:
                game_options = True

            # FOR ENTERING THE CREDITS MENU
            elif not game_running and not game_over and self.nav_ofs == 200:
                game_credits = True

            # FOR EXITING THE GAME
            elif not game_running and not game_over and self.nav_ofs == 300:
                pyglet.app.exit()

            # FOR RELOADING THE GAME AFTER GAME OVER
            if not game_running and game_over:
                self.reload()

        # PLAYER 1 KEY PRESS EVENTS
        if symbol == key.D:
            self.player1.right = True
        if symbol == key.A:
            self.player1.left = True
        if symbol == key.W:
            self.player1.up = True

            # FOR NAVIGATING UP IN GAME MENU
            if not game_running and not game_over and not game_options and not game_credits:
                if self.nav_ofs > 0:
                    self.menu.update(-game_menu_nav_step)
                    self.nav_ofs -= game_menu_nav_step
                elif self.nav_ofs == 0:
                    self.nav_ofs = (len(game_menu_text)-1) * game_menu_nav_step
                    self.menu.update(((len(game_menu_text)-1) * game_menu_nav_step))


        if symbol == key.S:
            self.player1.down = True

            # FOR NAVIGATING DOWN IN GAME MENU
            if not game_running and not game_over and not game_options and not game_credits:
                if self.nav_ofs < (len(game_menu_text)-1)*game_menu_nav_step:
                    self.menu.update(game_menu_nav_step)
                    self.nav_ofs += game_menu_nav_step
                elif self.nav_ofs == (len(game_menu_text)-1) * game_menu_nav_step:
                    self.nav_ofs = 0
                    self.menu.update(-((len(game_menu_text)-1) * game_menu_nav_step))

        if symbol == key.F and game_running:

            # TOGGLE FIRE (MANUAL/AUTO)
            if self.player1.fire_type == "auto":
                self.player1.fire_type = "manual"
            else:
                self.player1.fire_type = "auto"

        if symbol == key.SPACE and game_running:
            if self.player1.fire_type == "auto":
                self.player1.fire = True
            else:
                self.player1.laser_list.append(
                    DisplayLasers(self.player1.pos_x + 90, self.player1.pos_y + 30, Sprite(self.player1.fire_img)))
                self.player1.laser_sound.play()

        if symbol == key.LSHIFT and game_running:
            self.player1.gaurd = True

        # PLAYER 2 KEY PRESS EVENTS
        if symbol == key.RIGHT:
            self.player2.right = True
        if symbol == key.LEFT:
            self.player2.left = True
        if symbol == key.UP:
            self.player2.up = True
        if symbol == key.DOWN:
            self.player2.down = True
        if symbol == key.NUM_0 and game_running:
            if self.player2.fire_type == "auto":
                self.player2.fire_type = "manual"
            else:
                self.player2.fire_type = "auto"
        if symbol == key.P and game_running:
            if self.player2.fire_type == "auto":
                self.player2.fire = True
            else:
                self.player2.laser_list.append(
                    DisplayLasers(self.player2.pos_x - 15, self.player2.pos_y + 30, Sprite(self.player2.fire_img)))
                self.player2.laser_sound.play()

        if symbol == key.RALT and game_running:
            self.player2.gaurd = True

    def on_key_release(self, symbol, modifiers):

        # PLAYER 1 KEY RELEASE EVENTS
        if symbol == key.D:
            self.player1.right = False
        if symbol == key.A:
            self.player1.left = False
        if symbol == key.W:
            self.player1.up = False
        if symbol == key.S:
            self.player1.down = False
        if symbol == key.SPACE:
            if self.player1.fire_type == "auto":
                self.player1.fire = False
        if symbol == key.LSHIFT and game_running:
            self.player1.gaurd = False

        # PLAYER 1 KEY RELEASE EVENTS
        if symbol == key.RIGHT:
            self.player2.right = False
        if symbol == key.LEFT:
            self.player2.left = False
        if symbol == key.UP:
            self.player2.up = False
        if symbol == key.DOWN:
            self.player2.down = False
        if symbol == key.P:
            if self.player2.fire_type == "auto":
                self.player2.fire = False
        if symbol == key.RALT and game_running:
            self.player2.gaurd = False

    def on_draw(self):
        self.clear()

        # SPACE BG DRAWING
        for space in self.space_list:
            space.draw()

        # PLAYER DRAWINGS
        if not self.player1.lost:
            self.player1.draw()
        if not self.player2.lost:
            self.player2.draw()

        # GAME MENU DRAWINGS
        if game_options:
            Quad([0, resolution[1]], resolution, [100, 10, 10, 128] * 4).draw()
        elif game_credits:
            Quad([0, resolution[1]], resolution, [10, 10, 100, 128] * 4).draw()
        elif not game_running and not game_over:
            self.menu.draw()
            pyglet.text.Label("DUAL", font_name="Tempus Sans ITC", font_size=150,
                              x=resolution[0] / 2, y=700, anchor_x="center",
                              anchor_y="center",
                              color=[200, 255, 255, 255], bold=True).draw()

        if game_running:
            # PLAYER LASER DRAWINGS
            for lsr in self.player1.laser_list:
                lsr.draw()
            for lsr in self.player2.laser_list:
                lsr.draw()

            # PLAYER HP DRAWINGS
            self.p1_dhp.draw()
            self.p2_dhp.draw()
            self.p1_hp.draw()
            self.p2_hp.draw()

            # PLAYER GAURD DRAWINGS
            self.p1_gaurd.draw()
            self.p2_gaurd.draw()

        # PLAYER EXPLOSION DRAWINGS
        for explosion in self.player1.exp_list:
            explosion.draw()
        for explosion in self.player2.exp_list:
            explosion.draw()

        # GAME OVER MENU DRAWINGS
        if game_over:
            self.menu.menu_bg.draw()
            pyglet.text.Label(winner+" WINS", font_name="Tempus Sans ITC", font_size=80,
                              x=resolution[0] / 2, y=(resolution[1] / 2)+200, anchor_x="center",
                              anchor_y="center",
                              color=[255, 255, 255, 255], bold=True).draw()
            pyglet.text.Label("PRESS ENTER TO RELOAD", font_name="Tempus Sans ITC", font_size=60,
                              x=resolution[0] / 2, y=resolution[1] / 2, anchor_x="center",
                              anchor_y="center",
                              color=[255, 255, 255, 255], bold=True).draw()

        # FPS LABEL DRAWING
        self.fps_display.draw()

    def update(self, dt):

        self.update_space(dt)
        if game_running and not game_paused:
            self.update_player(self.player1, p1_base, dt)
            self.update_player(self.player2, p2_base, dt)

            self.player_auto_fire(dt)
            self.update_player_laser(dt)

            self.update_explosion(self.player1)
            self.update_explosion(self.player2)

            self.p1_hp.update(p1_hp_pos, p1_hp_size)
            self.p2_hp.update(p2_hp_pos, p2_hp_size)

            self.update_gaurd()
            self.update_dhp()

    def update_space(self, dt):

        # FOR SCROLLING SPACE BG
        for space in self.space_list:
            space.update(dt)
            if space.pos_y <= -1300:
                self.space_list.remove(space)
                self.space_list.append(DisplayObjects(0, 1100, Sprite(self.space_img)))
            space.vel_y = -space_scroll_speed

    def update_player(self, player, player_base, dt):

        # PLAYER MOVEMENTS INSIDE PLAYER BASE
        if player.right and player.pos_x < player_base[1] - player.width:
            player.pos_x += player.speed * dt
        if player.left and player.pos_x > player_base[0]:
            player.pos_x -= player.speed * dt
        if player.up and player.pos_y < resolution[1] - player.height - 100:
            player.pos_y += player.speed * dt
        if player.down and player.pos_y > 0:
            player.pos_y -= player.speed * dt

        # UPDATING PLAYER MOVEMENTS
        player.update(dt)

    def player_auto_fire(self, dt):
        if self.player1.fire and self.player1.fire_type == "auto":
            self.player1.fire_rate -= dt
            if self.player1.fire_rate <= 0:
                self.player1.laser_list.append(
                    DisplayLasers(self.player1.pos_x + 90, self.player1.pos_y + 30, Sprite(self.player1.fire_img)))
                self.player1.laser_sound.play()
                self.player1.fire_rate += 1 - p1_fire_rate
        if self.player2.fire and self.player2.fire_type == "auto":
            self.player2.fire_rate -= dt
            if self.player2.fire_rate <= 0:
                self.player2.laser_list.append(
                    DisplayLasers(self.player2.pos_x - 15, self.player2.pos_y + 30, Sprite(self.player2.fire_img)))
                self.player2.laser_sound.play()
                self.player2.fire_rate += 1 - p2_fire_rate

    def update_player_laser(self, dt):
        global p2_hp_score, p1_hp_score
        sp = 15
        # UPDATING LASER POSITIONS OF PLAYER 1
        for lsr in self.player1.laser_list:
            lsr.update()
            lsr.pos_x += p1_laser_speed * dt
            if lsr.pos_x > lsr.initial_pos_x + p1_laser_range:
                self.player1.laser_list.remove(lsr)
            elif self.player2.pos_x + self.player2.width > lsr.pos_x + lsr.width > self.player2.pos_x + sp:
                if self.player2.pos_y < lsr.pos_y + lsr.height and lsr.pos_y < self.player2.pos_y + self.player2.height:
                    if not self.player2.gaurd or (self.player2.gaurd and p2_gaurd_pos[0] >= resolution[0]):
                        self.player1.laser_list.remove(lsr)
                        p2_hp_pos[0] += p2_damage_taken
                        p2_hp_score -= 1
                        self.check_game_status()
                        self.player1.exp_list.append(
                            SpriteAnimation(explosion_img, [4, 5], [480, 384], 0.1, [lsr.pos_x + lsr.width - 48,
                                                                                     lsr.pos_y - 48]).get_sprite()
                        )
                        self.player1.exp_timer.append(explosion_time)
                        exp_sound.play()

        # UPDATING LASER POSITIONS OF PLAYER 2
        for lsr in self.player2.laser_list:
            lsr.update()
            lsr.pos_x -= p2_laser_speed * dt
            if lsr.pos_x < lsr.initial_pos_x - p2_laser_range:
                self.player2.laser_list.remove(lsr)
            elif self.player1.pos_x < lsr.pos_x < self.player1.pos_x + self.player1.width - sp:
                if self.player1.pos_y < lsr.pos_y < self.player1.pos_y + self.player1.height:
                    if not self.player1.gaurd or (self.player1.gaurd and p1_gaurd_size[0] <= 0):
                        self.player2.laser_list.remove(lsr)
                        p1_hp_size[0] -= p1_damage_taken
                        p1_hp_score -= 1
                        self.check_game_status()
                        self.player2.exp_list.append(
                            SpriteAnimation(explosion_img, [4, 5], [480, 384], 0.1, [lsr.pos_x + lsr.width - 48,
                                                                                     lsr.pos_y - 48]).get_sprite()
                        )
                        self.player2.exp_timer.append(explosion_time)
                        exp_sound.play()

    def update_explosion(self, player):
        exploded = False
        for i in range(len(player.exp_timer)):
            player.exp_timer[i] -= 1
            if player.exp_timer[i] <= 0:
                exploded = True
        if exploded:
            player.exp_list.pop(0)
            player.exp_timer.pop(0)

    def update_gaurd(self):
        global p1_gaurd_size, p2_gaurd_size
        self.p1_gaurd.update(p1_gaurd_pos, p1_gaurd_size)
        self.p2_gaurd.update(p2_gaurd_pos, p2_gaurd_size)
        if self.player1.gaurd and p1_gaurd_size[0] > 0:
            p1_gaurd_size[0] -= p1_guard_consumption_rate
        elif p1_gaurd_size[0] < p1_total_gaurd:
            p1_gaurd_size[0] += p1_gaurd_regen_rate
        if self.player2.gaurd and p2_gaurd_pos[0] < resolution[0]:
            p2_gaurd_pos[0] += p2_guard_consumption_rate
        elif p2_gaurd_pos[0] > resolution[0] - p2_total_gaurd:
            p2_gaurd_pos[0] -= p2_gaurd_regen_rate

    def check_game_status(self):
        global game_running, game_over, winner, explosion_time
        if p1_hp_score <= 0:
            game_running = False
            game_over = True
            winner = "PLAYER 2"
            self.player1.lost = True
            explosion_time = 25
        if p2_hp_score <= 0:
            game_running = False
            game_over = True
            winner = "PLAYER 1"
            self.player2.lost = True
            explosion_time = 25

    def reload(self):
        global game_running, game_over, winner, p1_hp_pos, p1_total_life, p1_hp_size, p1_hp_score, p2_hp_pos, \
            p2_hp_size, p2_total_life, p2_hp_score, explosion_time, p1_gaurd_size, p2_gaurd_pos, p1_dhp_pos, p1_dhp_size, p2_dhp_pos, p2_dhp_size

        # GAME DETAILS
        game_running = False
        game_over = False
        winner = None

        # PLAYER 1 DETAILS
        p1_total_life = 550
        p1_hp_pos = [0, 800]
        p1_hp_size = [p1_total_life, 20]
        p1_hp_score = p1_total_life / p1_damage_taken
        p1_gaurd_size = [p1_total_gaurd, 20]
        p1_dhp_pos = p1_hp_pos.copy()
        p1_dhp_size = p1_hp_size.copy()

        # PLAYER 2 DETAILS
        p2_total_life = 550
        p2_hp_pos = [resolution[0] - p2_total_life, 800]
        p2_hp_size = [p2_total_life, 20]
        p2_hp_score = p2_total_life / p2_damage_taken
        p2_gaurd_pos = [resolution[0] - p2_total_gaurd, 770]
        p2_dhp_pos = p2_hp_pos.copy()
        p2_dhp_size = p2_hp_size.copy()

        # OTHER DETAILS
        explosion_time = 15  # in ms

        # PLAYER INITIALIZATIONS
        self.player1 = DisplayPlayers(p1_pos_x, p1_pos_y, p1_sprite, p1_speed, p1_laser_img, p1_fire_type)

        self.player2 = DisplayPlayers(p2_pos_x, p2_pos_y, p2_sprite, p2_speed, p2_laser_img, p2_fire_type)

        # self.player1.laser_sound.play()

        self.p1_hp = Quad(p1_hp_pos, p1_hp_size, p1_hp_color, 'p1')
        self.p2_hp = Quad(p2_hp_pos, p2_hp_size, p2_hp_color, 'p2')

        self.p1_dhp = Quad(p1_dhp_pos, p1_dhp_size, p1_dhp_color, 'p1')
        self.p2_dhp = Quad(p2_dhp_pos, p2_dhp_size, p2_dhp_color, 'p2')

        self.p1_gaurd = Quad(p1_gaurd_pos, p1_gaurd_size, p1_gaurd_color, 'p1')
        self.p2_gaurd = Quad(p2_gaurd_pos, p2_gaurd_size, p2_gaurd_color, 'p2')

        self.menu = GameMenu(resolution, game_menu_text)

    def update_dhp(self):
        global p1_dhp_size, p2_dhp_pos
        self.p1_dhp.update(p1_dhp_pos, p1_dhp_size)
        self.p2_dhp.update(p2_dhp_pos, p2_dhp_size)

        if p1_hp_size[0] < p1_dhp_size[0]:
            p1_dhp_size[0] -= 1.5
        if p2_hp_pos[0] > p2_dhp_pos[0]:
            p2_dhp_pos[0] += 1.5


if __name__ == "__main__":
    window = MyWindow(resolution[0], resolution[1], "DUAL", resizable=False)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
