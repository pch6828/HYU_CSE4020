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

fcnt = 0
now_frame = 0

def render():
    global azimuth
    global elevation
    global distance
    global origin
    global up
    global w
    global u
    global v
    global wiremode
    global smooth
    global moving
    global now_frame
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    gluPerspective(45, 1, 1, 100)
   
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    w = np.array([np.cos(elevation)*(np.sin(azimuth)),np.sin(elevation),np.cos(elevation)*(np.cos(azimuth))])
    u = np.cross(np.array([0.,up, 0.]), w)
    u /= np.sqrt(np.dot(u,u))
    v = np.cross(u, w)
    v /= np.sqrt(np.dot(v,v))
    gluLookAt(distance*w[0]+origin[0],distance*w[1]+origin[1],distance*w[2]+origin[2], origin[0],origin[1],origin[2], 0,up,0)

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
    lightPos0 = (5.,5.,5.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos0) 
    lightPos1 = (-5.,5.,-5.,1.)    
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
    glColor3ub(0,255,255)

    glColor3ub(0, 255, 255)
    drawHierarchy()

    if moving and fcnt != 0:
        now_frame += 1
        now_frame %= fcnt
    glDisable(GL_LIGHTING)
    
oldpos = (0,0)
newpos = (0,0)
enableOrbit = False
enablePanning = False
face = up
moving = False
resize = 1

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

channel_list = []
joint_list = []
motion_list = []

def drop_callback(window, paths):
    global moving, channel_list, joint_list, motion_list, fcnt, now_frame, resize
    moving = False
    channel_list = []
    joint_list = []
    motion_list = []
    fcnt = 0
    now_frame = 0
    resize = 1
    hinput = False
    minput = False
    jcnt = 0
    jname_list = []
    fps = 0
    pushcnt = 0
    popcnt = 0

    file = open(paths[0])
    while True:
        line = file.readline()
        if not line:
            break
        line = line.strip()

        if line == 'HIERARCHY':
            hinput = True
            minput = False
            continue
        elif line == 'MOTION':
            minput = True
            hinput = False
            continue

        parsedline = line.split()

        if hinput:
            if parsedline[0] == 'ROOT' or parsedline[0] == 'JOINT':
                jname_list.append(parsedline[1])
                jcnt += 1
            elif parsedline[0] == '{':
                channel_list.append('push')
            elif parsedline[0] == '}':
                channel_list.append('pop')
            elif parsedline[0] == 'OFFSET':
                t = np.array(list(map(float, parsedline[1:])))
                if np.dot(t, t) > 1:
                    resize = 100
                joint_list.append(t)
            elif parsedline[0] == 'CHANNELS':
                channel_list.append(parsedline[2:])
        elif minput:
            if parsedline[0] == 'Frames:':
                fcnt = int(parsedline[1])
            elif parsedline[0] == 'Frame' and parsedline[1] == 'Time:':
                fps = 1.0/float(parsedline[2])
            else:
                motion_list.append(list(map(float, parsedline)))
    print("File Name: " + paths[0])
    print("# of Frames: "+str(fcnt))
    print("FPS: "+str(fps))
    print("# of Joints: "+str(jcnt))
    print("Joint Name:")
    for n in jname_list:
        print(n, end=' ')
    print('')

def key_callback(window, key, scancode, action, mods):
    global moving
    if action == glfw.PRESS:
        if key == glfw.KEY_SPACE:
            moving = True

def drawHierarchy():
    global moving, channel_list, joint_list, motion_list, now_frame, resize

    joint_stack = []
    jcnt = 0
    mcnt = 0
    for ch in channel_list:
        if ch == 'push':
            glPushMatrix()
            glTranslatef(joint_list[jcnt][0]/resize, joint_list[jcnt][1]/resize, joint_list[jcnt][2]/resize)
            if len(joint_stack)!=0:
                #glBegin(GL_LINES)
                #glVertex3fv(-joint_list[jcnt]/resize)
                #glVertex3fv(np.array([0.,0.,0.])/resize)
                #glEnd()
                drawCubeBetweenJoints(-joint_list[jcnt]/resize, np.array([0.,0.,0.])/resize)
                joint_stack.append(joint_stack[-1]+joint_list[jcnt])
            else:
                joint_stack.append(joint_list[jcnt])
            jcnt += 1
        elif ch == 'pop':
            glPopMatrix()
            joint_stack = joint_stack[:-1]
        else:
            if moving:
                for mo in ch:
                    mo = mo.upper()
                    if mo == 'XPOSITION':
                        glTranslatef(motion_list[now_frame][mcnt]/resize, 0, 0)
                    elif mo == 'YPOSITION':
                        glTranslatef(0, motion_list[now_frame][mcnt]/resize, 0)
                    elif mo == 'ZPOSITION':
                        glTranslatef(0, 0, motion_list[now_frame][mcnt]/resize)
                    elif mo == 'XROTATION':
                        glRotatef(motion_list[now_frame][mcnt], 1, 0, 0)
                    elif mo == 'YROTATION':
                        glRotatef(motion_list[now_frame][mcnt], 0, 1, 0)
                    elif mo == 'ZROTATION':
                        glRotatef(motion_list[now_frame][mcnt], 0, 0, 1)
                    mcnt+=1

def drawCubeBetweenJoints(p1, p2):
    v = p1-p2
    nv = v/np.sqrt(np.dot(v, v))
    n = np.array([0.,1.,0.])

    c = np.cross(nv, n)
    cn = np.sqrt(np.dot(c, c))
    theta = np.rad2deg(np.arcsin(cn))
    if np.dot(nv, n) < 0:
        theta = 180 - theta
    
    if cn != 0:
        c /= cn
    glPushMatrix()
    glRotatef(-theta, c[0], c[1], c[2])
    glScalef(.05, np.sqrt(np.dot(v, v)), .05)
    glBegin(GL_TRIANGLES)

    glNormal3f(0,0,1) # v0, v2, v1, v0, v3, v2 normal
    glVertex3f( -1 ,  1 ,  1 ) # v0 position
    glVertex3f(  1 ,  0 ,  1 ) # v2 position
    glVertex3f(  1 ,  1 ,  1 ) # v1 position

    glVertex3f( -1 ,  1 ,  1 ) # v0 position
    glVertex3f( -1 ,  0 ,  1 ) # v3 position
    glVertex3f(  1 ,  0 ,  1 ) # v2 position

    glNormal3f(0,0,-1)
    glVertex3f( -1 ,  1 , -1 ) # v4
    glVertex3f(  1 ,  1 , -1 ) # v5
    glVertex3f(  1 ,  0 , -1 ) # v6

    glVertex3f( -1 ,  1 , -1 ) # v4
    glVertex3f(  1 ,  0 , -1 ) # v6
    glVertex3f( -1 ,  0 , -1 ) # v7

    glNormal3f(0,1,0)
    glVertex3f( -1 ,  1 ,  1 ) # v0
    glVertex3f(  1 ,  1 ,  1 ) # v1
    glVertex3f(  1 ,  1 , -1 ) # v5

    glVertex3f( -1 ,  1 ,  1 ) # v0
    glVertex3f(  1 ,  1 , -1 ) # v5
    glVertex3f( -1 ,  1 , -1 ) # v4

    glNormal3f(0,-1,0)
    glVertex3f( -1 ,  0 ,  1 ) # v3
    glVertex3f(  1 ,  0 , -1 ) # v6
    glVertex3f(  1 ,  0 ,  1 ) # v2

    glVertex3f( -1 ,  0 ,  1 ) # v3
    glVertex3f( -1 ,  0 , -1 ) # v7
    glVertex3f(  1 ,  0 , -1 ) # v6

    glNormal3f(1,0,0)
    glVertex3f(  1 ,  1 ,  1 ) # v1
    glVertex3f(  1 ,  0 ,  1 ) # v2
    glVertex3f(  1 ,  0 , -1 ) # v6

    glVertex3f(  1 ,  1 ,  1 ) # v1
    glVertex3f(  1 ,  0 , -1 ) # v6
    glVertex3f(  1 ,  1 , -1 ) # v5

    glNormal3f(-1,0,0)
    glVertex3f( -1 ,  1 ,  1 ) # v0
    glVertex3f( -1 ,  0 , -1 ) # v7
    glVertex3f( -1 ,  0 ,  1 ) # v3

    glVertex3f( -1 ,  1 ,  1 ) # v0
    glVertex3f( -1 ,  1 , -1 ) # v4
    glVertex3f( -1 ,  0 , -1 ) # v7
    glEnd()
    glPopMatrix()
    
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
    glfw.set_drop_callback(window, drop_callback)
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
