from pyglet.gl import *

def draw_line(x1, x2, y1, y2):
    i=0
    x=0
    y=0
    dx = x2-x1
    dy = y2-y1
    if (dx < 0):
        dx = -dx
    if (dy < 0):
        dy = -dy
    incx = 1
    if (x2 < x1):
        # global incx
        incx = -1
    incy = 1
    if (y2 < y1):
        # global incy
        incy = -1
    x = x1
    y = y1
    if (dx > dy):
        draw_pixel(x, y)
        e = 2 * dy-dx
        inc1 = 2*(dy-dx)
        inc2 = 2*dy
        for i in range(int(dx)):
            if (e >= 0):
                y += incy
                e += inc1
            else:
                e += inc2
            x += incx
            draw_pixel(x, y)
    else:
        draw_pixel(x, y)
        e = 2*dx-dy
        inc1 = 2*(dx-dy)
        inc2 = 2*dx
        for i in range(int(dy)):
            if (e >= 0):
                x += incx
                e += inc1
            else:
                e += inc2
            y += incy
            draw_pixel(x, y)

def draw_pixel(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


