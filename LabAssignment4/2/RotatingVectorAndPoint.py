import glfw
import numpy as np
from OpenGL.GL import *

def render(M):
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
    
    # draw point p
    glBegin(GL_POINTS)
    T = np.array([[1.,0.,.5],
                  [0.,1.,0.],
                  [0.,0.,1.]])
    glVertex2fv((M @ T @ np.array([.5,0.,1.]))[:-1])
    glEnd()

    #draw vector v
    glBegin(GL_LINES)
    glVertex2fv((M @ np.array([0.,0.,1.]))[:-1])
    glVertex2fv((M @ np.array([.5,0.,1.]))[:-1])
    glEnd()
    
def main():
    global gComposedM
    if not glfw.init():
        return

    window = glfw.create_window(480,480,"2018008395", None, None)

    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        th = glfw.get_time()
        R = np.array([[np.cos(th), -np.sin(th),0.],
                      [np.sin(th), np.cos(th),0.],
                      [0.,         0.,        1.]])
        render(R)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
