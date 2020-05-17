from pyglet.gl import *
from pyglet.window import FPSDisplay, key
from pyglet.sprite import Sprite
from DisplayObjects import preload_image, DisplayObjects, DisplayPlayers, DisplayLasers, Lasers
from SpriteAnimations import SpriteAnimation
from GameMenu import GameMenu, SelectionMenu, ControlsMenu, AboutMenu, draw_start_page
from GameStatus import GameStatus
import time
from LineDraw import draw_line
from Quads import Quad_Right, Quad
from math import sqrt
from ShipData import get_ship_stats, get_ship_quad_stats

# code for getting the native screen resolution and setting it into the pyglet window
display = pyglet.canvas.Display()
screen = display.get_default_screen()
screen_width = screen.width
screen_height = screen.height
resolution = (screen_width, screen.height)




fullscreen = True
image_path = "res/sprites/"
sound_path = "res/sounds/"
starting_screen_timeout = 3     # in seconds


# method for re-estimating the x-axis pixel point with respect to 1920 screen width
def resx(x):
    return (resolution[0] * (x)) / 1920


# method for re-estimating the y-axis pixel point with respect to 1080 screen width
def resy(y):
    return (resolution[1] * (y)) / 1080

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



# BG IMAGE DETAILS
space_scroll_speed = 50
space_bg_img = image_path + "space.jpg"

# PLAYER 1 DETAILS
p1_pos_x = resx(100)
p1_pos_y = resy(500)
p1_fire_rate = 0.9  # min - 0    max - 1
p1_fire_type = "auto"
p1_base = [0, resolution[0] / 2]
p1_total_life = resx(700)
p1_total_gaurd = resx(530)
p1_hp_pos = [0, resy(1000)]
p1_hp_size = [p1_total_life, resy(20)]
p1_hp_color = [0, 255, 0, 255] * 4
p1_gaurd_pos = [0, resy(970)]
p1_gaurd_size = [p1_total_gaurd, resy(20)]
p1_gaurd_color = [0, 0, 255, 255] * 4
p1_guard_consumption_rate = resx(2)
p1_dhp_pos = p1_hp_pos.copy()
p1_dhp_size = p1_hp_size.copy()
p1_dhp_color = [255, 0, 0, 255] * 4
p1_ship = ""

# PLAYER 2 DETAILS
p2_pos_x = resx(1000)
p2_pos_y = resy(500)
p2_fire_rate = 0.9  # min - 0    max - 1
p2_fire_type = "auto"
p2_base = [resolution[0] / 2, resolution[0]]
p2_total_life = resx(700)
p2_total_gaurd = resx(530)
p2_hp_pos = [resolution[0] - p2_total_life, resy(1000)]
p2_hp_size = [p2_total_life, resy(20)]
p2_hp_color = [0, 255, 0, 255] * 4
p2_gaurd_pos = [resolution[0] - p2_total_gaurd, resy(970)]
p2_gaurd_size = [p2_total_gaurd, resy(20)]
p2_gaurd_color = [0, 0, 255, 255] * 4
p2_guard_consumption_rate = resx(2)
p2_dhp_pos = p2_hp_pos.copy()
p2_dhp_size = p2_hp_size.copy()
p2_dhp_color = [255, 0, 0, 255] * 4
p2_ship = ""

# EXPLOSION DETAILS
explosion_img = image_path + "explosion.png"
explosion_time = 15  # in ms+
exp_sound = pyglet.media.load(sound_path + "exp_01.wav", streaming=False)

# song player for menu bg song
bg_player = pyglet.media.Player()
bg_player.queue(pyglet.media.load(sound_path + "loading.wav"))
bg_player.loop = True


# song player for game bg song
game_player = pyglet.media.Player()
game_player.queue(pyglet.media.load(sound_path + "battle.wav"))
game_player.loop = True


class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):

        # WINDOW INITIALIZATIONS
        super().__init__(*args, **kwargs)
        self.frame_rate = 1 / 60.0
        self.fps_display = FPSDisplay(self)
        self.fps_display.label.font_size = 50

        # MAKING THE PRIMITIVE DRAWINGS TRANSPARENT
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # GAME MENU INITIALIZATIONS
        self.status = GameStatus()
        self.menu = GameMenu(resolution, self.status.game_menu_text)
        self.smenu = SelectionMenu(resolution, self.status.game_selection_text)
        self.cmenu = ControlsMenu()
        self.amenu = AboutMenu()
        self.start_time = time.time()

        # INITIALLY PLAYING THE MENU BG SONG
        bg_player.play()

        # SPACE BG INITIALIZATIONS
        self.space_list = []
        self.space_img = preload_image(space_bg_img)
        for i in range(2):
            self.space_list.append(DisplayObjects(0, i * 1080, Sprite(self.space_img)))
        for space in self.space_list:
            space.vel_y = -space_scroll_speed

        # PLAYER INITIALIZATIONS
        # CREATING PLAYER OBJECTS
        self.player1 = DisplayPlayers(p1_pos_x, p1_pos_y, p1_fire_type)
        self.player2 = DisplayPlayers(p2_pos_x, p2_pos_y, p2_fire_type)

        # PLAYER HP QUAD CREATION
        self.player1.hp = Quad(p1_hp_pos, p1_hp_size, p1_hp_color, 'p1')
        self.player2.hp = Quad(p2_hp_pos, p2_hp_size, p2_hp_color, 'p2')

        # PLAYER GAURD QUAD CREATION
        self.player1.gaurd = Quad(p1_gaurd_pos, p1_gaurd_size, p1_gaurd_color, 'p1')
        self.player2.gaurd = Quad(p2_gaurd_pos, p2_gaurd_size, p2_gaurd_color, 'p2')

        # PLAYER DAMAGE HP QUAD CREATION
        self.player1.dhp = Quad(p1_dhp_pos, p1_dhp_size, p1_dhp_color, 'p1')
        self.player2.dhp = Quad(p2_dhp_pos, p2_dhp_size, p2_dhp_color, 'p2')


    def on_resize(self, width, height):
        # CODE FOR SETTING THE ORIGIN TO THE BOTTOM LEFT CORNER
        width = max(1, width)
        height = max(1, height)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            # GETTING BACK FROM OPTIONS AND CREDITS MENU TO MAIN MENU
            if self.status.game_menu:
                if self.status.game_controls:
                    self.status.game_controls = False
                if self.status.game_about:
                    self.status.game_about = False

            # GETTING BACK FROM SELECTION MENU TO MAIN MENU AND SETTING THE REQUIRED VARIABLES TO DEFAULT
            if self.status.game_selection:
                self.status.game_selection = False
                self.status.game_menu = True
                self.status.player1_selected = False
                self.status.player2_selected = False
                self.smenu.update_p1(-self.smenu.p1_nav_ofs)
                self.smenu.p1_nav_ofs = 0
                self.smenu.update_p2(-self.smenu.p2_nav_ofs)
                self.smenu.p2_nav_ofs = 0

            # FOR PAUSING THE GAME
            if self.status.game_running and not self.status.game_paused:
                self.status.game_paused = True
                self.status.game_running = False
                self.status.game_menu = True
                self.menu = GameMenu(resolution, self.status.pause_menu_text)
                # PAUSING THE GAME MUSIC AND PLAYING THE MENU MUSIC
                game_player.pause()
                bg_player.play()

        if symbol == key.ENTER and time.time() - self.start_time > starting_screen_timeout+1:
            # IN GAME MAIN MENU
            if self.status.game_menu:

                # FOR ENTERING INTO THE SELECTION MENU
                if not self.status.game_started and self.menu.nav_ofs == 0:
                    self.status.game_selection = True
                    self.status.game_menu = False

                # FOR RESUMING THE GAME WHILE PAUSED
                elif self.status.game_paused and self.menu.nav_ofs == 0:
                    self.status.game_running = True
                    self.status.game_paused = False
                    self.status.game_menu = False
                    # PAUSING THE MENU MUSIC AND PLAYING THE GAME MUSIC
                    bg_player.pause()
                    game_player.play()

                # FOR ENTERING THE CONTROLS MENU
                elif (not self.status.game_started or self.status.game_paused) and self.menu.nav_ofs == 100:
                    self.status.game_controls = True

                # FOR ENTERING THE CREDITS MENU
                elif (not self.status.game_started or self.status.game_paused) and self.menu.nav_ofs == 200:
                    self.status.game_about = True

                # FOR EXITING THE GAME AND ENTERING MAIN MENU
                elif self.status.game_paused and self.menu.nav_ofs == 300:
                    self.reload()

                # FOR EXITING THE GAME
                elif not self.status.game_started and self.menu.nav_ofs == 300:
                    pyglet.app.exit()

            # FOR RELOADING THE GAME AFTER GAME OVER
            if self.status.game_over:
                self.reload()

        # PLAYER 1 KEY PRESS EVENTS
        if symbol == key.D:
            self.player1.right = True
        if symbol == key.A:
            self.player1.left = True
        if symbol == key.W:
            self.player1.up = True

            # IN GAME MAIN MENU
            if self.status.game_menu:
                # FOR NAVIGATING UP IN GAME MENU
                if not self.status.game_running and not self.status.game_over and not self.status.game_controls and not self.status.game_about:
                    if self.menu.nav_ofs > 0:
                        self.menu.update(-self.menu.nav_step)
                        self.menu.nav_ofs -= self.menu.nav_step
                    elif self.menu.nav_ofs == 0:
                        self.menu.nav_ofs = (len(self.status.game_menu_text) - 1) * self.menu.nav_step
                        self.menu.update(((len(self.status.game_menu_text) - 1) * self.menu.nav_step))

            # IN GAME SELECTION MENU
            if self.status.game_selection:
                # FOR NAVIGATING UP IN SELECTION MENU
                if self.smenu.p1_nav_ofs > 0:
                    self.smenu.update_p1(-self.smenu.nav_step)
                    self.smenu.p1_nav_ofs -= self.smenu.nav_step
                elif self.smenu.p1_nav_ofs == 0:
                    self.smenu.p1_nav_ofs = (len(self.status.game_selection_text) - 1) * self.smenu.nav_step
                    self.smenu.update_p1(((len(self.status.game_selection_text) - 1) * self.smenu.nav_step))

        if symbol == key.S:
            self.player1.down = True

            # IN GAME MAIN MENU
            if self.status.game_menu:
                # FOR NAVIGATING DOWN IN GAME MENU
                if not self.status.game_running and not self.status.game_over and not self.status.game_controls and not self.status.game_about:
                    if self.menu.nav_ofs < (len(self.status.game_menu_text) - 1) * self.menu.nav_step:
                        self.menu.update(self.menu.nav_step)
                        self.menu.nav_ofs += self.menu.nav_step
                    elif self.menu.nav_ofs == (len(self.status.game_menu_text) - 1) * self.menu.nav_step:
                        self.menu.nav_ofs = 0
                        self.menu.update(-((len(self.status.game_menu_text) - 1) * self.menu.nav_step))

            # IN GAME SELECTION MENU
            if self.status.game_selection:
                # FOR NAVIGATING DOWN IN SELECTION MENU
                if self.smenu.p1_nav_ofs < (len(self.status.game_selection_text) - 1) * self.smenu.nav_step:
                    self.smenu.update_p1(self.menu.nav_step)
                    self.smenu.p1_nav_ofs += self.menu.nav_step
                elif self.smenu.p1_nav_ofs == (len(self.status.game_selection_text) - 1) * self.smenu.nav_step:
                    self.smenu.p1_nav_ofs = 0
                    self.smenu.update_p1(-((len(self.status.game_selection_text) - 1) * self.smenu.nav_step))

        if symbol == key.F and self.status.game_running:

            # TOGGLE FIRE (MANUAL/AUTO)
            if self.player1.fire_type == "auto":
                self.player1.fire_type = "manual"
            else:
                self.player1.fire_type = "auto"

        if symbol == key.SPACE:
            global p1_hp_score, p1_ship

            # FOR FIRING THE LASERS WHILE GAME RUNNING
            if self.status.game_running:
                if self.player1.fire_type == "auto":
                    self.player1.fire = True
                else:
                    self.player1.laser_list.append(
                        Lasers(self.player1.pos_x + 96, self.player1.pos_y + 34, [20, 5], p1_dhp_color))
                    self.player1.laser_sound.play()

            # IN GAME SELECTION MENU
            if self.status.game_selection:

                # FOR SELECTING THE SHIP OF PLAYER 1 AND SETTING THE SELECTED SHIP STATS TO THE PLAYER OBJECT
                if self.smenu.p1_nav_ofs == 0:
                    self.player1.set_stats(p1_ship1_stats)
                    p1_ship = self.status.game_selection_text[0]
                elif self.smenu.p1_nav_ofs == 100:
                    self.player1.set_stats(p1_ship2_stats)
                    p1_ship = self.status.game_selection_text[1]
                elif self.smenu.p1_nav_ofs == 200:
                    self.player1.set_stats(p1_ship3_stats)
                    p1_ship = self.status.game_selection_text[2]

                # CALCULATING THE PLAYER 1 SHIP HP SCORE BASED ON SELECTED SHIP STAT
                p1_hp_score = p1_total_life / self.player1.damage_taken

                # CHECKING FOR PLAYER 2 SHIP SELECTION // IF TRUE START THE GAME
                self.status.player1_selected = True
                if self.status.player2_selected:
                    self.status.game_started = True
                    self.status.game_running = True
                    self.status.game_selection = False
                    # FOR PAUSING THE MENU MUSIC AND PLAYING THE GAME MUSIC
                    bg_player.pause()
                    game_player.play()


        # PLAYER SPECIAL FIRE
        if symbol == key.G and self.status.game_running:
            self.player1.sp_fire = True
            if len(self.player1.sp_laser_list) < 3:
                self.player1.sp_laser_list.append(Lasers(self.player1.pos_x + 96, self.player1.pos_y + 34, [50, 50], [255, 0, 0, 255]*4))

        # PLAYER 1 GAURDING
        if symbol == key.LSHIFT and self.status.game_running:
            self.player1.gaurding = True

        # PLAYER 2 KEY PRESS EVENTS
        if symbol == key.RIGHT:
            self.player2.right = True
        if symbol == key.LEFT:
            self.player2.left = True
        if symbol == key.UP:
            self.player2.up = True

            # IN GAME SELECTION MENU
            if self.status.game_selection:
                # FOR NAVIGATING UP IN SELECTION MENU
                if self.smenu.p2_nav_ofs > 0:
                    self.smenu.update_p2(-self.smenu.nav_step)
                    self.smenu.p2_nav_ofs -= self.smenu.nav_step
                elif self.smenu.p2_nav_ofs == 0:
                    self.smenu.p2_nav_ofs = (len(self.status.game_selection_text) - 1) * self.smenu.nav_step
                    self.smenu.update_p2(((len(self.status.game_selection_text) - 1) * self.smenu.nav_step))

        if symbol == key.DOWN:
            self.player2.down = True

            # IN GAME SELECTION  MENU
            if self.status.game_selection:
                # FOR NAVIGATING DOWN IN SELECTION MENU
                if self.smenu.p2_nav_ofs < (len(self.status.game_selection_text) - 1) * self.smenu.nav_step:
                    self.smenu.update_p2(self.menu.nav_step)
                    self.smenu.p2_nav_ofs += self.menu.nav_step
                elif self.smenu.p2_nav_ofs == (len(self.status.game_selection_text) - 1) * self.smenu.nav_step:
                    self.smenu.p2_nav_ofs = 0
                    self.smenu.update_p2(-((len(self.status.game_selection_text) - 1) * self.smenu.nav_step))

        if symbol == key.NUM_0 and self.status.game_running:

            # TOGGLE FIRE (MANUAL/AUTO)
            if self.player2.fire_type == "auto":
                self.player2.fire_type = "manual"
            else:
                self.player2.fire_type = "auto"

        if symbol == key.P:
            global p2_hp_score, p2_ship

            # FOR FIRING THE LASERS WHILE GAME RUNNING
            if self.status.game_running:
                if self.player2.fire_type == "auto":
                    self.player2.fire = True
                else:
                    self.player2.laser_list.append(
                        Lasers(self.player2.pos_x - 17, self.player2.pos_y + 34, [20, 5], p2_hp_color))
                    self.player2.laser_sound.play()

            # IN GAME SELECTION MENU
            if self.status.game_selection:

                # FOR SELECTING THE SHIP OF PLAYER 2 AND SETTING THE SELECTED SHIP STATS TO THE PLAYER OBJECT
                if self.smenu.p2_nav_ofs == 0:
                    self.player2.set_stats(p2_ship1_stats)
                    p2_ship = self.status.game_selection_text[0]
                elif self.smenu.p2_nav_ofs == 100:
                    self.player2.set_stats(p2_ship2_stats)
                    p2_ship = self.status.game_selection_text[1]
                elif self.smenu.p2_nav_ofs == 200:
                    self.player2.set_stats(p2_ship3_stats)
                    p2_ship = self.status.game_selection_text[2]

                # CALCULATING THE PLAYER 2 SHIP HP SCORE BASED ON SELECTED SHIP STAT
                p2_hp_score = p2_total_life / self.player2.damage_taken
                self.status.player2_selected = True
                if self.status.player1_selected:
                    self.status.game_started = True
                    self.status.game_running = True
                    self.status.game_selection = False
                    # FOR PAUSING THE MENU MUSIC AND PLAYING THE GAME MUSIC
                    bg_player.pause()
                    game_player.play()

        # PLAYER 1 GAURDING
        if symbol == key.RALT and self.status.game_running:
            self.player2.gaurding = True

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
        if symbol == key.SPACE and self.status.game_running:
            if self.player1.fire_type == "auto":
                self.player1.fire = False
        if symbol == key.LSHIFT and self.status.game_running:
            self.player1.gaurding = False
        if symbol == key.G and self.status.game_running:
            self.player1.sp_fire = False

        # PLAYER 1=2 KEY RELEASE EVENTS
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
        if symbol == key.RALT and self.status.game_running:
            self.player2.gaurding = False

    def on_draw(self):
        self.clear()
        # SPACE BG DRAWING
        for space in self.space_list:
            space.draw()

        if time.time() - self.start_time < starting_screen_timeout+1:
            draw_start_page(time.time() - self.start_time, starting_screen_timeout)

        # GAME MENU DRAWINGS
        elif self.status.game_controls:
            self.cmenu.draw()
        elif self.status.game_about:
            self.amenu.draw()
        elif not self.status.game_running and not self.status.game_over and not self.status.game_selection:
            self.menu.draw()

        # SELECTION MENU DRAWINGS
        if self.status.game_selection:
            self.smenu.draw()
            if self.status.player1_selected:
                pyglet.text.Label("PLAYER 1 SELECTED " + p1_ship, font_name="Tempus Sans ITC", font_size=30,
                                  x=300, y=100, anchor_x="center",
                                  anchor_y="center",
                                  color=[200, 255, 255, 255], bold=True).draw()
            if self.status.player2_selected:
                pyglet.text.Label("PLAYER 2 SELECTED " + p2_ship, font_name="Tempus Sans ITC", font_size=30,
                                  x=1620, y=100, anchor_x="center",
                                  anchor_y="center",
                                  color=[200, 255, 255, 255], bold=True).draw()

        # DRAWINGS WHILE GAME IS RUNNING
        if self.status.game_running:
            # PLAYER LASER DRAWINGS
            for lsr in self.player1.laser_list:
                lsr.draw()
            for lsr in self.player2.laser_list:
                lsr.draw()

            # PLAYER DRAWINGS
            self.player1.draw(self.status.game_started)
            self.player2.draw(self.status.game_started)

            # PLAYER ENERGY SHIELD DRAWINGS
            if self.player1.gaurding and p1_gaurd_size[0] > 2:
                self.player1.draw_shield(self.player1.sprite.x - 40, self.player1.sprite.y - 40)
            if self.player2.gaurding and p2_gaurd_pos[0] + 1 < resolution[0]:
                self.player2.draw_shield(self.player2.sprite.x - 20, self.player2.sprite.y - 40)

            xy = draw_line(self.player1.sprite.x + self.player1.width, self.player2.sprite.x,
                      self.player1.sprite.y + (self.player1.height / 2),
                      self.player2.sprite.y + (self.player2.height / 2))

            for splsr in self.player1.sp_laser_list:
                splsr.draw()

            # PLAYER EXPLOSION DRAWINGS
            for explosion in self.player1.exp_list:
                explosion.draw()
            for explosion in self.player2.exp_list:
                explosion.draw()


        # GAME OVER MENU DRAWINGS
        if self.status.game_over:
            self.menu.menu_bg.draw()
            pyglet.text.Label("GAME OVER", font_name="Tempus Sans ITC", font_size=resx(200),
                              x=resolution[0] / 2, y=resy(resolution[1] / 2) + resy(400), anchor_x="center",
                              anchor_y="center",
                              color=[255, 255, 255, 255], bold=True).draw()
            pyglet.text.Label(winner + " WINS", font_name="Tempus Sans ITC", font_size=resx(100),
                              x=resolution[0] / 2, y=(resolution[1] / 2), anchor_x="center",
                              anchor_y="center",
                              color=[255, 255, 255, 255], bold=True).draw()
            pyglet.text.Label("PRESS ENTER TO RELOAD", font_name="Tempus Sans ITC", font_size=resx(30),
                              x=resolution[0] / 2, y=(resolution[1] / 2) - resy(500), anchor_x="center",
                              anchor_y="center",
                              color=[255, 255, 255, 255], bold=True).draw()

        # FPS LABEL DRAWING
        self.fps_display.draw()



    def update(self, dt):

        # UPDATE SPACE BG
        self.update_space(dt)

        # UPADTE DRAWINGS WHILE GAME  IS RUNNING
        if self.status.game_running and not self.status.game_paused:
            self.update_player(self.player1, p1_base, dt)
            self.update_player(self.player2, p2_base, dt)

            self.player_auto_fire(dt)
            self.update_player_laser(dt)

            self.update_explosion(self.player1)
            self.update_explosion(self.player2)

            self.update_special_laser()

    def update_space(self, dt):

        # FOR SCROLLING SPACE BG
        for space in self.space_list:
            space.update(dt)
            # CHECKING IF THE IMAGE HAS REACHED ITS END BY SCROLLING // IF TRUE THEN REMOVE THE IMAGE FROM THE LIST AND ADD NEW IMAGE ON TOP OF PREVIOUS
            if space.pos_y <= -1080:
                self.space_list.remove(space)
                self.space_list.append(DisplayObjects(0, 1080, Sprite(self.space_img)))
            space.vel_y = -space_scroll_speed

    def update_player(self, player, player_base, dt):

        # PLAYER MOVEMENTS INSIDE PLAYER BASE
        if player.right and player.pos_x < player_base[1] - player.width:
            player.pos_x += player.speed * dt
        if player.left and player.pos_x > player_base[0]:
            player.pos_x -= player.speed * dt
        if player.up and player.pos_y < resolution[1] - player.height - 150:
            player.pos_y += player.speed * dt
        if player.down and player.pos_y > 0:
            player.pos_y -= player.speed * dt

        # PLAYER HP CHECKING AND UPDATING
        self.player1.hp.update(p1_hp_pos, p1_hp_size)
        self.player2.hp.update(p2_hp_pos, p2_hp_size)

        # PLAYER GAURD UPDATING
        self.update_gaurd()

        # PLAYER DAMAGE HP UPDATING
        self.update_dhp()

        # UPDATING PLAYER MOVEMENTS
        player.update(dt)

    def player_auto_fire(self, dt):
        # ADDING LASERS TO THE LASER LIST IIF THE FIRE TYPE IS AUTO
        if self.player1.fire and self.player1.fire_type == "auto":
            self.player1.fire_rate -= dt
            if self.player1.fire_rate <= 0:
                self.player1.laser_list.append(
                    Lasers(self.player1.pos_x + 96, self.player1.pos_y + 34, [20, 5], p1_dhp_color))
                self.player1.laser_sound.play()
                self.player1.fire_rate += 1 - p1_fire_rate
        if self.player2.fire and self.player2.fire_type == "auto":
            self.player2.fire_rate -= dt
            if self.player2.fire_rate <= 0:
                self.player2.laser_list.append(
                    Lasers(self.player2.pos_x - 17, self.player2.pos_y + 34, [20, 5], p2_hp_color))
                self.player2.laser_sound.play()
                self.player2.fire_rate += 1 - p2_fire_rate

    def update_player_laser(self, dt):
        global p2_hp_score, p1_hp_score
        sp = 15
        # UPDATING LASER POSITIONS OF PLAYER 1
        for lsr in self.player1.laser_list:
            lsr.update()
            lsr.pos_x += self.player1.laser_speed * dt
            if lsr.pos_x > lsr.initial_pos_x + self.player1.laser_range:
                self.player1.laser_list.remove(lsr)
            elif self.player2.pos_x + self.player2.width > lsr.pos_x + lsr.size[0] > self.player2.pos_x + sp:
                if self.player2.pos_y < lsr.pos_y + lsr.size[
                    1] and lsr.pos_y < self.player2.pos_y + self.player2.height:
                    if not self.player2.gaurding or (self.player2.gaurding and p2_gaurd_pos[0] >= resolution[0]):
                        self.player1.laser_list.remove(lsr)
                        p2_hp_pos[0] += self.player2.damage_taken
                        self.check_game_status()
                        self.player1.exp_list.append(
                            SpriteAnimation(explosion_img, [4, 5], [480, 384], 0.1, [lsr.pos_x + lsr.size[0] - 48,
                                                                                     lsr.pos_y - 48]).get_sprite()
                        )
                        self.player1.exp_timer.append(explosion_time)
                        exp_sound.play()

        # UPDATING LASER POSITIONS OF PLAYER 2
        for lsr in self.player2.laser_list:
            lsr.update()
            lsr.pos_x -= self.player2.laser_speed * dt
            if lsr.pos_x < lsr.initial_pos_x - self.player2.laser_range:
                self.player2.laser_list.remove(lsr)
            elif self.player1.pos_x < lsr.pos_x < self.player1.pos_x + self.player1.width - sp:
                if self.player1.pos_y < lsr.pos_y < self.player1.pos_y + self.player1.height:
                    if not self.player1.gaurding or (self.player1.gaurding and p1_gaurd_size[0] <= 0):
                        self.player2.laser_list.remove(lsr)
                        p1_hp_size[0] -= self.player1.damage_taken
                        self.check_game_status()
                        self.player2.exp_list.append(
                            SpriteAnimation(explosion_img, [4, 5], [480, 384], 0.1, [lsr.pos_x + lsr.size[0] - 48,
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
        # UPADTING GAURD
        self.player1.gaurd.update(p1_gaurd_pos, p1_gaurd_size)
        self.player2.gaurd.update(p2_gaurd_pos, p2_gaurd_size)
        # CHECKING IF PLAYER IS GUARDING // IF TRUE DEPLETE THE GAURD QUAD // ELSE REPLENISH THE GAURD QUAD
        if self.player1.gaurding and p1_gaurd_size[0] > 0:
            p1_gaurd_size[0] -= p1_guard_consumption_rate
        elif p1_gaurd_size[0] < p1_total_gaurd:
            p1_gaurd_size[0] += self.player1.gaurd_regen_rate
        if self.player2.gaurding and p2_gaurd_pos[0] < resolution[0]:
            p2_gaurd_pos[0] += p2_guard_consumption_rate
        elif p2_gaurd_pos[0] > resolution[0] - p2_total_gaurd:
            p2_gaurd_pos[0] -= self.player2.gaurd_regen_rate

    def check_game_status(self):
        global winner, explosion_time
        # CHECKING IF ANY PLAYER HAS WON THE GAME

        if p1_hp_size[0] <= 0:
            self.status.game_running = False
            self.status.game_over = True
            winner = "PLAYER 2"
            self.player1.lost = True
            explosion_time = 25
        if p2_hp_pos[0] >= resolution[0]:
            self.status.game_running = False
            self.status.game_over = True
            winner = "PLAYER 1"
            self.player2.lost = True
            explosion_time = 25

    def reload(self):
        global winner, p1_hp_pos, p1_total_life, p1_hp_size, p1_hp_score, p2_hp_pos, \
            p2_hp_size, p2_total_life, p2_hp_score, explosion_time, p1_gaurd_size, p2_gaurd_pos, p1_dhp_pos, p1_dhp_size, p2_dhp_pos, p2_dhp_size

        # GAME DETAILS
        winner = None

        # PLAYER 1 DETAILS
        p1_total_life = resx(550)
        p1_hp_pos = [0, resy(1000)]
        p1_hp_size = [p1_total_life, resy(20)]
        p1_hp_score = 0
        p1_gaurd_size = [p1_total_gaurd, resy(20)]
        p1_dhp_pos = p1_hp_pos.copy()
        p1_dhp_size = p1_hp_size.copy()

        # PLAYER 2 DETAILS
        p2_total_life = resx(550)
        p2_hp_pos = [resolution[0] - p2_total_life, resy(1000)]
        p2_hp_size = [p2_total_life, resy(20)]
        p2_hp_score = 0
        p2_gaurd_pos = [resolution[0] - p2_total_gaurd, resy(970)]
        p2_dhp_pos = p2_hp_pos.copy()
        p2_dhp_size = p2_hp_size.copy()

        # OTHER DETAILS
        explosion_time = 15  # in ms

        self.status = GameStatus()
        self.menu = GameMenu(resolution, self.status.game_menu_text)
        self.smenu = SelectionMenu(resolution, self.status.game_selection_text)

        # PLAYER INITIALIZATIONS
        self.player1 = DisplayPlayers(p1_pos_x, p1_pos_y, p1_fire_type)

        self.player2 = DisplayPlayers(p2_pos_x, p2_pos_y, p2_fire_type)

        # self.player1.laser_sound.play()
        self.player1.hp = Quad(p1_hp_pos, p1_hp_size, p1_hp_color, 'p1')
        self.player2.hp = Quad(p2_hp_pos, p2_hp_size, p2_hp_color, 'p2')

        self.player1.dhp = Quad(p1_dhp_pos, p1_dhp_size, p1_dhp_color, 'p1')
        self.player2.dhp = Quad(p2_dhp_pos, p2_dhp_size, p2_dhp_color, 'p2')

        self.player1.gaurd = Quad(p1_gaurd_pos, p1_gaurd_size, p1_gaurd_color, 'p1')
        self.player2.gaurd = Quad(p2_gaurd_pos, p2_gaurd_size, p2_gaurd_color, 'p2')

        self.menu = GameMenu(resolution, self.status.game_menu_text)

    def update_dhp(self):
        global p1_dhp_size, p2_dhp_pos
        self.player1.dhp.update(p1_dhp_pos, p1_dhp_size)
        self.player2.dhp.update(p2_dhp_pos, p2_dhp_size)

        if p1_hp_size[0] < p1_dhp_size[0]:
            p1_dhp_size[0] -= 1.5
        if p2_hp_pos[0] > p2_dhp_pos[0]:
            p2_dhp_pos[0] += 1.5

    def track_enemy(self, obj, dest_pos, speed=5):
        x = dest_pos[0] - obj.pos_x
        y = dest_pos[1] - obj.pos_y
        hyp = sqrt((x * x) + (y * y))
        if hyp != 0:
            x /= hyp
            y /= hyp
            obj.pos_x += x*speed
            obj.pos_y += y*speed
            obj.update()

    def update_special_laser(self):
        global p2_hp_score, p1_hp_score
        for splsr in self.player1.sp_laser_list:
            self.track_enemy(splsr, [self.player2.sprite.x, self.player2.sprite.y])
            if self.player2.pos_x + self.player2.width > splsr.pos_x + splsr.size[0] > self.player2.pos_x:
                if self.player2.pos_y < splsr.pos_y + splsr.size[
                1] and splsr.pos_y < self.player2.pos_y + self.player2.height:
                    if not self.player2.gaurding or (self.player2.gaurding and p2_gaurd_pos[0] >= resolution[0]):
                        self.player1.sp_laser_list.remove(splsr)
                        p2_hp_pos[0] += self.player2.sp_damage_taken
                        self.check_game_status()
                        self.player1.exp_list.append(
                            SpriteAnimation(explosion_img, [4, 5], [480, 384], 0.1, [splsr.pos_x + splsr.size[0] - 48,
                                                                                     splsr.pos_y - 48]).get_sprite()
                        )
                        self.player1.exp_timer.append(explosion_time)
                        exp_sound.play()
                    else:
                        self.player1.sp_laser_list.remove(splsr)




if __name__ == "__main__":
    window = MyWindow(resolution[0], resolution[1], "DUAL", resizable=False, fullscreen=fullscreen)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()







