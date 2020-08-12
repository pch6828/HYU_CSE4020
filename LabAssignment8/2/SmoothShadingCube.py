import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo
import ctypes

gCamAng = 0.
gCamHeight = 1.
objectColor = (1.,0.,0.,1.)
lightColor = (1.,1.,1.,1.)

def createVertexAndIndexArrayIndexed():
    varr = np.array([
            (-0.5773502691896258,0.5773502691896258,0.5773502691896258),
            ( -1 ,  1 ,  1 ), # v0
            (0.8163965809277261,0.4082482904638631,0.4082482904638631),
            (  1 ,  1 ,  1 ), # v1
            (0.4082482904638631,-0.4082482904638631,0.8163965809277261),
            (  1 , -1 ,  1 ), # v2
            (-0.4082482904638631,-0.8163965809277261,0.4082482904638631),
            ( -1 , -1 ,  1 ), # v3
            (-0.4082482904638631,0.4082482904638631,-0.8163965809277261),
            ( -1 ,  1 , -1 ), # v4
            (0.4082482904638631,0.8163965809277261,-0.4082482904638631),
            (  1 ,  1 , -1 ), # v5
            (0.5773502691896258,-0.5773502691896258,-0.5773502691896258),
            (  1 , -1 , -1 ), # v6
            (-0.8163965809277261,-0.4082482904638631,-0.4082482904638631),
            ( -1 , -1 , -1 ), # v7
            ], 'float32')
    iarr = np.array([
            (0,2,1),
            (0,3,2),
            (4,5,6),
            (4,6,7),
            (0,1,5),
            (0,5,4),
            (3,6,2),
            (3,7,6),
            (1,2,6),
            (1,6,5),
            (0,7,3),
            (0,4,7),
            ])
    return varr, iarr

def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)
    
def render():
    global gCamAng, gCamHeight
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1,10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)

    drawFrame()

    glEnable(GL_LIGHTING)   # try to uncomment: no lighting
    glEnable(GL_LIGHT0)

    glEnable(GL_NORMALIZE)  # try to uncomment: lighting will be incorrect if you scale the object
    glEnable(GL_RESCALE_NORMAL)

    # light position
    glPushMatrix()

    lightPos = (3.,4.,5.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos) 

    lightPos = (3.,4.,5.,1.)    # try to change 4th element to 0. or 1.
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glPopMatrix()

    # light intensity for each color channel
    lightColor = (1.,1.,1.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

    # material reflectance for each color channel
    objectColor = (1.,0.,0.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glColor3ub(0, 0, 255) # glColor*() is ignored if lighting is enabled
 
    drawCube_glDrawElements()

    glDisable(GL_LIGHTING)

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight
    global lightColor
    global objectColor
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1

gVertexArrayIndexed = None
gIndexArray = None

def main():
    global gVertexArrayIndexed, gIndexArray

    if not glfw.init():
        return
    window = glfw.create_window(480,480,'2018008395', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)

    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
