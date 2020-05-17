from pyglet.gl import *


class SpriteAnimation:
    def __init__(self, image_path, sprite_row_columns, img_size, animation_speed=0.1, display_location=[0, 0],
                 set_region=None):
        self.original_img = pyglet.image.load(image_path)
        self.sprite_rows = sprite_row_columns[0]
        self.sprite_columns = sprite_row_columns[1]
        self.img_size = img_size
        self.animation_speed = animation_speed
        self.display_location = display_location
        self.time = 0
        if set_region is not None:
            self.original_img = self.original_img.get_region(set_region[0], 0,
                                                             img_size[0]-set_region[0], img_size[1])
            self.sprite_columns = set_region[1]
            img_size[0] = img_size[0]-set_region[0]

    def get_sprite(self):
        img_grid = pyglet.image.ImageGrid(self.original_img,
                                          self.sprite_rows,                # sprite rows
                                          self.sprite_columns,
                                          item_width=self.img_size[0] / self.sprite_columns,
                                          item_height=self.img_size[1] / self.sprite_rows)
        sprite_textures = pyglet.image.TextureGrid(img_grid)
        sprite_animation = pyglet.image.Animation.from_image_sequence(sprite_textures[0:], self.animation_speed,
                                                                      loop=True)
        final_sprite = pyglet.sprite.Sprite(sprite_animation, x=self.display_location[0], y=self.display_location[1])

        return final_sprite
