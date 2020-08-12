import glfw
import numpy as np
from OpenGL.GL import *

idx = 4
pt = [GL_POLYGON, GL_POINTS, GL_LINES, GL_LINE_STRIP, GL_LINE_LOOP, GL_TRIANGLES, GL_TRIANGLE_STRIP, GL_TRIANGLE_FAN, GL_QUADS, GL_QUAD_STRIP]

def render():
    global idx
    global pt
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(pt[idx])
    for i in np.linspace(0, 2*np.pi - np.pi/6, 12):
        glVertex2f(np.cos(i), np.sin(i))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global idx
    if key==glfw.KEY_0:
        if action==glfw.PRESS:
            idx = 0
    elif key==glfw.KEY_1:
        if action==glfw.PRESS:
            idx = 1
    elif key==glfw.KEY_2:
        if action==glfw.PRESS:
            idx = 2
    elif key==glfw.KEY_3:
        if action==glfw.PRESS:
            idx = 3        
    elif key==glfw.KEY_4:
        if action==glfw.PRESS:
            idx = 4
    elif key==glfw.KEY_5:
        if action==glfw.PRESS:
            idx = 5
    elif key==glfw.KEY_6:
        if action==glfw.PRESS:
            idx = 6
    elif key==glfw.KEY_7:
        if action==glfw.PRESS:
            idx = 7
    elif key==glfw.KEY_8:
        if action==glfw.PRESS:
            idx = 8
    elif key==glfw.KEY_9:
        if action==glfw.PRESS:
            idx = 9

def main():
    if not glfw.init():
        return

    window = glfw.create_window(480,480,"2018008395", None, None)

    if not window:
        glfw.terminate()
        return
    
    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
