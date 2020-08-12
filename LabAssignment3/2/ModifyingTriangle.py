import glfw
import numpy as np
from OpenGL.GL import *

gComposedM = np.identity(3)

def render(T):
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
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )
    glEnd()
    
def key_callback(window, key, scancode, action, mods):
    W = np.array([[.9, 0., 0.],
                  [0., 1., 0.],
                  [0., 0., 1.]])
    E = np.array([[1.1, 0., 0.],
                  [0., 1., 0.],
                  [0., 0., 1.]])
    S = np.array([[np.cos(np.pi/18), -np.sin(np.pi/18),0.],
                  [np.sin(np.pi/18), np.cos(np.pi/18),0.],
                  [0.,         0.,        1.]])
    D = np.array([[np.cos(-np.pi/18), -np.sin(-np.pi/18),0.],
                  [np.sin(-np.pi/18), np.cos(-np.pi/18),0.],
                  [0.,         0.,        1.]])
    X = np.array([[1., -.1, 0.],
                  [0., 1., 0.],
                  [0., 0., 1.]])
    C = np.array([[1., .1, 0.],
                  [0., 1., 0.],
                  [0., 0., 1.]])
    R = np.array([[1., 0., 0.],
                  [0., -1., 0.],
                  [0., 0., 1.]])
    global gComposedM
    if key==glfw.KEY_1:
        if action==glfw.PRESS or action==glfw.REPEAT:
            gComposedM = np.identity(3)
    elif key==glfw.KEY_W:
        if action==glfw.PRESS or action==glfw.REPEAT:
            gComposedM = W@gComposedM
    elif key==glfw.KEY_E:
        if action==glfw.PRESS or action==glfw.REPEAT:
            gComposedM = E@gComposedM
    elif key==glfw.KEY_S:
        if action==glfw.PRESS or action==glfw.REPEAT:
            gComposedM = S@gComposedM
    elif key==glfw.KEY_D:
        if action==glfw.PRESS or action==glfw.REPEAT:
            gComposedM = D@gComposedM
    elif key==glfw.KEY_X:
        if action==glfw.PRESS or action==glfw.REPEAT:
            gComposedM = X@gComposedM
    elif key==glfw.KEY_C:
        if action==glfw.PRESS or action==glfw.REPEAT:
            gComposedM = C@gComposedM
    elif key==glfw.KEY_R:
        if action==glfw.PRESS or action==glfw.REPEAT:
            gComposedM = R@gComposedM

def main():
    global gComposedM
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
        render(gComposedM)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
