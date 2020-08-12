import glfw
import numpy as np
from OpenGL.GL import *

changes = []

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()

    glColor3ub(255, 255, 255)

    global changes
    
    for c in changes:
        if c == 1:
            glTranslatef(-.1, 0., 0)
        elif c == 2:
            glTranslatef(.1, 0., 0)
        elif c == 3:
            glRotatef(10, 0, 0, 1)
        elif c == 4:
            glRotatef(-10, 0, 0, 1)

    drawTriangle()

def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0.,.5])) 
    glVertex2fv(np.array([0.,0.,]))
    glVertex2fv(np.array([.5,0.,]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global changes
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            changes = []
        elif key==glfw.KEY_Q:
            changes.insert(0,1)
        elif key==glfw.KEY_E:
            changes.insert(0,2)
        elif key==glfw.KEY_A:
            changes.insert(0,3)
        elif key==glfw.KEY_D:
            changes.insert(0,4)

def main():
    if not glfw.init():
        return

    window = glfw.create_window(480,480,"2018008395", None, None)

    if not window:
        glfw.terminate()
        return
    
    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
