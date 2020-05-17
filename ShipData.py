import pyglet
from pyglet.sprite import Sprite
from DisplayObjects import preload_image

image_path = "res/sprites/"
sound_path = "res/sounds/"

# code for getting the native screen resolution and setting it into the pyglet window
display = pyglet.canvas.Display()
screen = display.get_default_screen()
screen_width = screen.width
screen_height = screen.height
resolution = (screen_width, screen.height)


# method for re-estimating the x-axis pixel point with respect to 1920 screen width
def resx(x):
    return (resolution[0] * (x)) / 1920


# method for re-estimating the y-axis pixel point with respect to 1080 screen width
def resy(y):
    return (resolution[1] * (y)) / 1080



# p1 ship stats
p1_ship1_stats = [resx(300), resx(600), resx(900), resx(35), resx(0.2), Sprite(preload_image(image_path + "p1_1.png"))]
p1_ship2_stats = [resx(340), resx(580), resx(800), resx(30), resx(0.3), Sprite(preload_image(image_path + "p1_2.png"))]
p1_ship3_stats = [resx(700), resx(1000), resx(1000), resx(10), resx(1), Sprite(preload_image(image_path + "p1_3.png"))]

# p2 ship stats
p2_ship1_stats = p1_ship1_stats[:-1].copy()
p2_ship2_stats = p1_ship2_stats[:-1].copy()
p2_ship3_stats = p1_ship3_stats[:-1].copy()
p2_ship1_stats.append(Sprite(preload_image(image_path + "p2_1.png")))
p2_ship2_stats.append(Sprite(preload_image(image_path + "p2_2.png")))
p2_ship3_stats.append(Sprite(preload_image(image_path + "p2_3.png")))

def get_ship_stats():
    all_ships = [p1_ship1_stats, p1_ship2_stats, p1_ship3_stats, p2_ship1_stats, p2_ship2_stats, p2_ship3_stats]
    return all_ships


# re evaluating the ship stat quad sizes w.r.t ship max stat and max quad size
def re(x, max):
    return (resx(500) * (x)) / resx(max)

# maximum ship stat points
ship_stat_max = [1000, 1000, 1000, 50, 1]


# method for setting every ships quad size w.r.t ship stats
def set_quad_size(stat):
    return [re(stat[i], ship_stat_max[i]) for i in range(5)]


# setting the ships quad sizes
ship1_stat_quad_sizes = set_quad_size(p1_ship1_stats)
ship2_stat_quad_sizes = set_quad_size(p1_ship2_stats)
ship3_stat_quad_sizes = set_quad_size(p1_ship3_stats)


def get_ship_quad_stats():
    all_quads = [ship1_stat_quad_sizes, ship3_stat_quad_sizes, ship3_stat_quad_sizes]
    return all_quads
