import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

azimuth = 0
elevation = 0
distance = 5
up = 1;
gComposedM = np.identity(4);
w = np.array([0.,0.,1.])
u = np.array([1.,0.,0.])
v = np.array([0.,1.,0.])
origin = np.array([0.,0.,0.])

def render():
    global azimuth
    global elevation
    global distance
    global origin
    global up
    global w
    global u
    global v
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    gluPerspective(45, 1, 1, 100)

    w = np.array([np.cos(elevation)*(np.sin(azimuth)),np.sin(elevation),np.cos(elevation)*(np.cos(azimuth))])
    u = np.cross(np.array([0.,up, 0.]), w)
    u /= np.sqrt(np.dot(u,u))
    v = np.cross(u, w)
    v /= np.sqrt(np.dot(v,v))
    gluLookAt(distance*w[0]+origin[0],distance*w[1]+origin[1],distance*w[2]+origin[2], origin[0],origin[1],origin[2], 0,up,0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

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

    t = glfw.get_time()

    glPushMatrix()
    glColor3ub(0,255,255)
    glRotatef(20*np.sin(t), 1,0,0)
    glRotatef(360*np.cos(t/10), 0,1,0)
    glTranslate(0.,abs(np.sin(t))/2,0.)

    glPushMatrix()
    glScalef(.3,.3,.3)
    drawSphere()
    glPopMatrix()

    glColor3ub(255,255,0)
    glTranslatef(0.,.3,0.)
    glPushMatrix()
    glScalef(.8,.1,.8)
    drawCube()
    glPopMatrix()

    glRotatef(20*np.sin(-t), 1,0,0)
    glRotatef(360*np.cos(-t/7), 0,1,0)
    glTranslate(0.,abs(np.sin(t))/4,0.)
    glTranslatef(0.,.2,0.)

    glColor3ub(0,255,255)
    glPushMatrix()
    glScalef(.2,.2,.2)
    drawSphere()
    glPopMatrix()

    glColor3ub(255,255,0)
    glPushMatrix()
    glTranslatef(0.,.2,0.)
    glPushMatrix()
    glScalef(.6,.1,.6)
    drawCube()
    glPopMatrix()

    glRotatef(20*np.sin(t), 1,0,0)
    glRotatef(360*np.cos(t/15), 0,1,0)
    glTranslate(0.,abs(np.sin(t))/6,0.)
    glTranslatef(0.,.15,0.)

    glColor3ub(0,255,255)
    glPushMatrix()
    glScalef(.15,.15,.15)
    drawSphere()    
    glPopMatrix()

    glColor3ub(255,255,0)
    glPushMatrix()
    glTranslatef(0.,.15,0.)
    glPushMatrix()
    glScalef(.4,.1,.4)
    drawCube()
    
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    
def drawCube():
    glBegin(GL_QUADS)
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f( 0.5, 0.5, 0.5) 
                             
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f( 0.5,-0.5,-0.5) 
                             
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
                             
    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5,-0.5)
 
    glVertex3f(-0.5, 0.5, 0.5) 
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5) 
    glVertex3f(-0.5,-0.5, 0.5) 
                             
    glVertex3f( 0.5, 0.5,-0.5) 
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    glEnd()

def drawSphere(numLats=12, numLongs=12):
    for i in range(0, numLats + 1):
        lat0 = np.pi * (-0.5 + float(float(i - 1) / float(numLats)))
        z0 = np.sin(lat0)
        zr0 = np.cos(lat0) 
 
        lat1 = np.pi * (-0.5 + float(float(i) / float(numLats)))
        z1 = np.sin(lat1)
        zr1 = np.cos(lat1) 
 
        # Use Quad strips to draw the sphere
        glBegin(GL_QUAD_STRIP) 
 
        for j in range(0, numLongs + 1):
            lng = 2 * np.pi * float(float(j - 1) / float(numLongs))
            x = np.cos(lng)
            y = np.sin(lng)
            glVertex3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr1, y * zr1, z1)
            
        glEnd()
        
oldpos = (0,0)
newpos = (0,0)
enableOrbit = False
enablePanning = False
face = up

def cursor_callback(window, xpos, ypos):
    global azimuth
    global elevation
    global oldpos
    global newpos
    global enableOrbit
    global origin
    global up
    global w
    global u
    global v
    if enableOrbit:
        oldpos = newpos
        newpos = glfw.get_cursor_pos(window)
        elevation -= (oldpos[1] - newpos[1])/100
        if np.cos(elevation)<0:
            up = -1
        else:
            up = 1
        azimuth += face*(oldpos[0] - newpos[0])/100
        
    if enablePanning:
        oldpos = newpos
        newpos = glfw.get_cursor_pos(window)
        origin += ((oldpos[0] - newpos[0])*u+(oldpos[1] - newpos[1])*v)/500
        
def button_callback(window, button, action, mod):
    global azimuth
    global elevation
    global oldpos
    global newpos
    global enableOrbit
    global enablePanning
    global face
    global up
    if button==glfw.MOUSE_BUTTON_LEFT:
        if action==glfw.PRESS:
            oldpos = glfw.get_cursor_pos(window)
            newpos = glfw.get_cursor_pos(window)
            enableOrbit = True
        elif action==glfw.RELEASE:
            enableOrbit = False
            face = up
            while azimuth > 2*np.pi:
                azimuth -= 2*np.pi
            while azimuth < 0:
                azimuth += 2*np.pi
            while elevation > 2*np.pi:
                elevation -= 2*np.pi
            while elevation < 0:
                elevation += 2*np.pi
    if button==glfw.MOUSE_BUTTON_RIGHT:
        if action==glfw.PRESS:
            oldpos = glfw.get_cursor_pos(window)
            newpos = glfw.get_cursor_pos(window)
            enablePanning = True
        elif action==glfw.RELEASE:
            enablePanning = False
        
def scroll_callback(window, xoffset, yoffset):
    global distance
    distance *= 10**(float(yoffset)/10)
    
def main():
    if not glfw.init():
        return
    window = glfw.create_window(1000,1000,"2018008395", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)
    glfw.terminate()
if __name__ == "__main__":
    main()
