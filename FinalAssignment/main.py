import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gComposedM = np.identity(4);
objectA = np.array([0., 0, 0., 1.]) #main object (packman)
A_size = 0.3
objectB = np.array([5., 0, 5., 1.]) #coin1 : just keep distance with packman and coin2
objectC = np.array([-5, 0, 5., 1.]) #coin2 : follow packman but keep distance
lookmode = True # if True : quarter view, else : first person view
up = 1 #upvector

def render():
    global lookmode
    global up
    global objectA
    global objectB
    global objectC
    global A_size
    global gComposedM
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    gluPerspective(45, 1, .001, 100)
   
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    camera = 0;
    target = 0;
    if lookmode:
        temp_A = gComposedM @ objectA
        target = temp_A
        camera = temp_A + 3*up
    else:
        camera = gComposedM @ (objectA + np.array([0.,A_size,A_size,0.]))
        target = gComposedM @ (objectA + np.array([0.,A_size,A_size*2,0.]))

    gluLookAt(camera[0],camera[1],camera[2], target[0],target[1],target[2], 0,up,0)
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([-10.,0., 0.]))
    glVertex3fv(np.array([10.,0., 0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,-10.]))
    glVertex3fv(np.array([0.,0.,10.]))
    #draw grid
    glColor3ub(64, 64, 64)
    for i in np.linspace(-10, 10, 201):
        glVertex3fv(np.array([-10.,0., i]))
        glVertex3fv(np.array([10.,0., i]))
        glVertex3fv(np.array([i,0., -10.]))
        glVertex3fv(np.array([i,0., 10.]))
    glEnd()
    glEnable(GL_LIGHTING)   
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_NORMALIZE)  
    glEnable(GL_RESCALE_NORMAL)
    # light position
    glPushMatrix()
    t = glfw.get_time()
    
    lightPos0 = (np.sin(t)*5.,5.,np.cos(t)*5.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos0) 
    lightPos1 = (np.sin(t)*-5.,5.,np.cos(t)*-5.,1.)    
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos1)
    glPopMatrix()
    # light intensity for each color channel
    lightColor0 = (1.,0.,0.,1.)
    lightColor1 = (0.,1.,0.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor0)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor1)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)
    # material reflectance for each color channel
    objectColor = (1.,1.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    managingCollision()
    glPushMatrix()
    glMultMatrixf(gComposedM.T)
    drawPackMan()
    glPopMatrix()

    objectColor = (1.,0.,0.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    
    glPushMatrix()
    glTranslatef(objectB[0], objectB[1], objectB[2])
    drawCoin()
    glPopMatrix()

    objectColor = (0.,0.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    
    glPushMatrix()
    glTranslatef(objectC[0], objectC[1], objectC[2])
    drawCoin()
    glPopMatrix()
    glDisable(GL_LIGHTING)

def button_callback(window, button, action, mod):
    global lookmode
    if button==glfw.MOUSE_BUTTON_LEFT:
        if action==glfw.PRESS:
            lookmode = not lookmode
            
moldpos = (0,0)
mnewpos = (0,0)

def cursor_callback(window, xpos, ypos):
    global up
    global gComposedM
    global moldpos
    global mnewpos

    moldpos = mnewpos
    mnewpos = glfw.get_cursor_pos(window)
    rad = (mnewpos[0] - moldpos[0])/100*up

    gComposedM = gComposedM @ np.array([[np.cos(rad),0.,-np.sin(rad),0.],
                                        [0.,1.,0.,0.],
                                        [np.sin(rad),0.,np.cos(rad),0.],
                                        [0.,0.,0.,1.]])

def key_callback(window, key, scancode, action, mods):
    global gComposedM, A_size, up
    
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_UP:
            gComposedM = gComposedM @ np.array([[1.,0.,0.,0.],
                                                [0.,1.,0.,0.],
                                                [0.,0.,1.,.05],
                                                [0.,0.,0.,1.]])
        if key == glfw.KEY_DOWN:
            gComposedM = gComposedM @ np.array([[1.,0.,0.,0.],
                                                [0.,1.,0.,0.],
                                                [0.,0.,1.,-.05],
                                                [0.,0.,0.,1.]])
        if key == glfw.KEY_LEFT:
            gComposedM = gComposedM @ np.array([[1.,0.,0.,.05],
                                                [0.,1.,0.,0.],
                                                [0.,0.,1.,0.],
                                                [0.,0.,0.,1.]])
        if key == glfw.KEY_RIGHT:
            gComposedM = gComposedM @ np.array([[1.,0.,0.,-.05],
                                                [0.,1.,0.,0.],
                                                [0.,0.,1.,0.],
                                                [0.,0.,0.,1.]])
        if key == glfw.KEY_G:
            gComposedM = gComposedM @ np.array([[1.1,0.,0.,0.],
                                                [0.,1.1,0.,0.],
                                                [0.,0.,1.1,0.],
                                                [0.,0.,0.,1.]])
            A_size *= 1.1
        if key == glfw.KEY_H:
            gComposedM = gComposedM @ np.array([[0.9,0.,0.,0.],
                                                [0.,0.9,0.,0.],
                                                [0.,0.,0.9,0.],
                                                [0.,0.,0.,1.]])
            A_size *= 0.9
        if key == glfw.KEY_S:
            gComposedM = gComposedM @ np.array([[1.,0.,0.,0.],
                                                [0.,1.,1.,0.],
                                                [0.,0.,1.,0.],
                                                [0.,0.,0.,1.]])
        if key == glfw.KEY_A:
            gComposedM = gComposedM @ np.array([[1.,0.,0.,0.],
                                                [0.,1.,-1.,0.],
                                                [0.,0.,1.,0.],
                                                [0.,0.,0.,1.]])
        if key == glfw.KEY_R:
            gComposedM = gComposedM @ np.array([[1.,0.,0.,0.],
                                                [0.,-1.,0.,0.],
                                                [0.,0.,1.,0.],
                                                [0.,0.,0.,1.]])
            up *= -1

def drawCube():
    glBegin(GL_TRIANGLES)
    glNormal3f(0,0,1) # v0, v2, v1, v0, v3, v2 normal
    glVertex3f( -1 ,  1 ,  1 ) # v0 position
    glVertex3f(  1 ,  -1 ,  1 ) # v2 position
    glVertex3f(  1 ,  1 ,  1 ) # v1 position
    glVertex3f( -1 ,  1 ,  1 ) # v0 position
    glVertex3f( -1 ,  -1 ,  1 ) # v3 position
    glVertex3f(  1 ,  -1 ,  1 ) # v2 position
    glNormal3f(0,0,-1)
    glVertex3f( -1 ,  1 , -1 ) # v4
    glVertex3f(  1 ,  1 , -1 ) # v5
    glVertex3f(  1 ,  -1 , -1 ) # v6
    glVertex3f( -1 ,  1 , -1 ) # v4
    glVertex3f(  1 ,  -1 , -1 ) # v6
    glVertex3f( -1 ,  -1 , -1 ) # v7
    glNormal3f(0,1,0)
    glVertex3f( -1 ,  1 ,  1 ) # v0
    glVertex3f(  1 ,  1 ,  1 ) # v1
    glVertex3f(  1 ,  1 , -1 ) # v5
    glVertex3f( -1 ,  1 ,  1 ) # v0
    glVertex3f(  1 ,  1 , -1 ) # v5
    glVertex3f( -1 ,  1 , -1 ) # v4
    glNormal3f(0,-1,0)
    glVertex3f( -1 ,  -1 ,  1 ) # v3
    glVertex3f(  1 ,  -1 , -1 ) # v6
    glVertex3f(  1 ,  -1 ,  1 ) # v2
    glVertex3f( -1 ,  -1 ,  1 ) # v3
    glVertex3f( -1 ,  -1 , -1 ) # v7
    glVertex3f(  1 ,  -1 , -1 ) # v6
    glNormal3f(1,0,0)
    glVertex3f(  1 ,  1 ,  1 ) # v1
    glVertex3f(  1 ,  -1 ,  1 ) # v2
    glVertex3f(  1 ,  -1 , -1 ) # v6
    glVertex3f(  1 ,  1 ,  1 ) # v1
    glVertex3f(  1 ,  -1 , -1 ) # v6
    glVertex3f(  1 ,  1 , -1 ) # v5
    glNormal3f(-1,0,0)
    glVertex3f( -1 ,  1 ,  1 ) # v0
    glVertex3f( -1 ,  -1 , -1 ) # v7
    glVertex3f( -1 ,  -1 ,  1 ) # v3
    glVertex3f( -1 ,  1 ,  1 ) # v0
    glVertex3f( -1 ,  1 , -1 ) # v4
    glVertex3f( -1 ,  -1 , -1 ) # v7
    glEnd()

def drawPackMan():
    t = glfw.get_time()

    glPushMatrix()
    glTranslatef(0, np.absolute(np.sin(t))*0.3+0.3, 0)
    glPushMatrix()
    glRotatef(np.absolute(np.sin(t))*30, 1, 0, 0)
    glScalef(.3, .15, .3)
    drawCube()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, .3, 0)
    glRotatef(-np.absolute(np.sin(t))*30, 1, 0, 0)
    glScalef(.3, .15, .3)
    drawCube()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, .7, 0)
    glScalef(.05, .1, .05)
    glRotatef(np.degrees(2*t), 0, 1, 0)
    glRotatef(45, 0, 1, 0)
    glRotatef(45, 0, 0, 1)
    glRotatef(45, 1, 0, 0)
    
    drawCube()
    glPopMatrix()
    glPopMatrix()
def drawCoin():
    t = glfw.get_time()

    glPushMatrix()
    glTranslatef(0, np.absolute(np.cos(t))*0.3+0.3, 0)
    glPushMatrix()
    glRotatef(np.degrees(t), 0,1,0)
    glPushMatrix()
    glScalef(.02, .2, .2)
    glRotatef(np.degrees(t), 1,0,0)
    drawCube()
    glPopMatrix()

    glPushMatrix()
    glScalef(.01, .2, .2)
    glRotatef(np.degrees(t)+45, 1,0,0)
    drawCube()
    glPopMatrix()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0,.7, 0)
    glScalef(.02, .2, .02)
    drawCube()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0,.6, 0)
    glRotatef(30, 1,0,0)
    glTranslatef(0, 0, .05)
    glScalef(.01, .1, .01)
    drawCube()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0,.6, 0)
    glRotatef(-30, 1,0,0)
    glTranslatef(0, 0, -.05)
    glScalef(.01, .1, .01)
    drawCube()
    glPopMatrix()

    glPopMatrix()

def managingCollision():
    global objectA, objectB, objectC, gComposedM, A_size
    temp_A = gComposedM @ objectA;

    while True:
        disAB = objectB - temp_A
        if np.sqrt(np.dot(disAB, disAB)) >= A_size+1:
            break;
        move = disAB * np.array([1.,0.,1.,0.])
        move /= np.sqrt(np.dot(move, move))*30
        objectB += move
        break
    while True:
        disAC = objectC - temp_A

        move = disAC * np.array([1.,0.,1.,0.])
        move /= np.sqrt(np.dot(move, move))
        if np.sqrt(np.dot(disAC, disAC)) <= A_size+0.7:
            objectC += move/30
        elif np.sqrt(np.dot(disAC, disAC)) > A_size+1:
            objectC -= move/50
        break
    
    while True:
        disBC = objectB - objectC
        if np.dot(disBC, disBC) >= 0.3:
            break;
        move = disBC * np.array([1.,0.,1.,0.])
        move /= np.sqrt(np.dot(move, move))*10;
        objectB += move
    
def main():
    if not glfw.init():
        return
    window = glfw.create_window(1000,1000,"2018008395", None, None)
    if not window:
        glfw.terminate()
        return
    
    np.random.seed(0)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)
    glfw.terminate()
if __name__ == "__main__":
    main()
