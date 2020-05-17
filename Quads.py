from pyglet.gl import *


class Quad:
    def __init__(self, starting_position, size=[10, 10], color=[255, 255, 255, 255]*4, incline=None):
        self.p1_incl = 0
        self.p2_incl = 0
        if incline == 'p1':
            self.p1_incl = 20
            self.p2_incl = 0
        elif incline == 'p2':
            self.p1_incl = 0
            self.p2_incl = 20
        self.size = size
        self.starting_position = starting_position
        self.indices = [0, 1, 2, 3]
        self.vertex = [self.starting_position[0], self.starting_position[1], 0.0,
                       self.starting_position[0] + self.size[0], self.starting_position[1], 0.0,
                       self.starting_position[0] + self.size[0] - self.p1_incl, self.starting_position[1] - self.size[1], 0.0,
                       self.starting_position[0] + self.p2_incl, self.starting_position[1] - self.size[1], 0.0]
        self.color = color
        self.vertices = pyglet.graphics.vertex_list_indexed(4, self.indices, ('v3f', self.vertex), ('c4B', self.color))

    def draw(self):
        self.vertices.draw(GL_QUADS)

    def update(self, starting_position, size=[10, 10]):
        self.starting_position = starting_position
        self.size = size
        self.vertex = [self.starting_position[0], self.starting_position[1], 0.0,
                       self.starting_position[0] + self.size[0], self.starting_position[1], 0.0,
                       self.starting_position[0] + self.size[0] - self.p1_incl, self.starting_position[1] - self.size[1], 0.0,
                       self.starting_position[0] + self.p2_incl, self.starting_position[1] - self.size[1], 0.0]
        self.vertices = pyglet.graphics.vertex_list_indexed(4, self.indices, ('v3f', self.vertex), ('c4B', self.color))


class Quad_Right:
    def __init__(self, starting_position, size=[10, 10], color=[255, 255, 255, 255]*4):
        self.size = size
        self.starting_position = starting_position
        self.indices = [0, 1, 2, 3]
        self.vertex = [self.starting_position[0], self.starting_position[1], 0.0,
                       self.starting_position[0], self.starting_position[1]+size[1], 0.0,
                       self.starting_position[0] - self.size[0], self.starting_position[1] + self.size[1], 0.0,
                       self.starting_position[0] - self.size[0], self.starting_position[1], 0.0]
        self.color = color
        self.vertices = pyglet.graphics.vertex_list_indexed(4, self.indices, ('v3f', self.vertex), ('c4B', self.color))

    def draw(self):
        self.vertices.draw(GL_QUADS)

    def update(self, starting_position, size=[10, 10]):
        self.starting_position = starting_position
        self.size = size
        self.vertex = [self.starting_position[0], self.starting_position[1], 0.0,
                       self.starting_position[0], self.starting_position[1] + size[1], 0.0,
                       self.starting_position[0] - self.size[0], self.starting_position[1] + self.size[1], 0.0,
                       self.starting_position[0] - self.size[0], self.starting_position[1], 0.0]
        self.vertices = pyglet.graphics.vertex_list_indexed(4, self.indices, ('v3f', self.vertex), ('c4B', self.color))
