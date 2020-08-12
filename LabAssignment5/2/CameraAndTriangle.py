import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gCamAng = 0
gComposedM = np.identity(4);

def render(M, camAng):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    
    glLoadIdentity()

    glOrtho(-1,1, -1,1, -1,1)

    gluLookAt(.1*np.sin(camAng),.1, .1*np.cos(camAng), 0,0,0, 0,1,0)
     
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0., 0.]))
    glVertex3fv(np.array([1.,0., 0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex3fv((M @ np.array([.0,.5,0.,1.]))[:-1])
    glVertex3fv((M @ np.array([.0,.0,0.,1.]))[:-1])
    glVertex3fv((M @ np.array([.5,.0,0.,1.]))[:-1])
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global gCamAng
    global gComposedM

    Q = np.array([[1.,0.,0.,-.1],
                  [0.,1.,0.,0.],
                  [0.,0.,1.,0.],
                  [0.,0.,0.,1.]])
    E = np.array([[1.,0.,0.,.1],
                  [0.,1.,0.,0.],
                  [0.,0.,1.,0.],
                  [0.,0.,0.,1.]])
    A = np.array([[np.cos(-np.pi/18),0.,np.sin(-np.pi/18),0.],
                  [0.,1.,0.,0.],
                  [-np.sin(-np.pi/18),0.,np.cos(-np.pi/18),0.],
                  [0.,0.,0.,1.]])
    D = np.array([[np.cos(np.pi/18),0.,np.sin(np.pi/18),0.],
                  [0.,1.,0.,0.],
                  [-np.sin(np.pi/18),0.,np.cos(np.pi/18),0.],
                  [0.,0.,0.,1.]])
    W = np.array([[1.,0.,0.,0.],
                  [0.,np.cos(-np.pi/18),-np.sin(-np.pi/18),0.],
                  [0.,np.sin(-np.pi/18),np.cos(-np.pi/18),0.],
                  [0.,0.,0.,1.]])
    S = np.array([[1.,0.,0.,0.],
                  [0.,np.cos(np.pi/18),-np.sin(np.pi/18),0.],
                  [0.,np.sin(np.pi/18),np.cos(np.pi/18),0.],
                  [0.,0.,0.,1.]])
    
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_1:
            gCamAng+=np.radians(-10)
        if key == glfw.KEY_3:
            gCamAng+=np.radians(10)
        if key == glfw.KEY_Q:
            gComposedM = Q @ gComposedM
        if key == glfw.KEY_E:
            gComposedM = E @ gComposedM
        if key == glfw.KEY_A:
            gComposedM = gComposedM @ A
        if key == glfw.KEY_D:
            gComposedM = gComposedM @ D
        if key == glfw.KEY_W:
            gComposedM = gComposedM @ W
        if key == glfw.KEY_S:
            gComposedM = gComposedM @ S
    
    
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
        render(gComposedM, gCamAng)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
