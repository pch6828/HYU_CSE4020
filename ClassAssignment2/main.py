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

wiremode = True
smooth = False

ivarr = np.array([], 'float32')
iarr = np.array([])
varr = np.array([], 'float32')

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
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

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
    if wiremode:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
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

    # glScalef(.001,.001,.001)
    if smooth:
        drawObject_glDrawElements()
    else:
        drawObject_glDrawArray()
    glDisable(GL_LIGHTING)
    
def drawObject_glDrawElements():
    global ivarr, iarr

    IVARR = ivarr
    IARR = iarr
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)

    glNormalPointer(GL_FLOAT, 6*IVARR.itemsize, IVARR)
    glVertexPointer(3, GL_FLOAT, 6*IVARR.itemsize, ctypes.c_void_p(IVARR.ctypes.data + 3*IVARR.itemsize))
    glDrawElements(GL_TRIANGLES, IARR.size, GL_UNSIGNED_INT, IARR)

def drawObject_glDrawArray():
    global varr

    VARR = varr
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*VARR.itemsize, VARR)
    glVertexPointer(3, GL_FLOAT, 6*VARR.itemsize, ctypes.c_void_p(VARR.ctypes.data + 3*VARR.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(VARR.size/6))

    
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

def drop_callback(window, paths):
    global ivarr, iarr, varr
    file = open(paths[0])

    tvarr = []
    tnarr = []
    inarr = []
    varr = []
    iarr = []
    ivarr = []

    cnttotal = 0;
    cnt3 = 0
    cnt4 = 0
    cntn = 0
    
    while True:
        line = file.readline()
        if not line:
            break
        parsedline = line.split()
        if len(parsedline)==0:
            continue
        if parsedline[0] == 'v':
            list.append(tvarr, (float(parsedline[1]), float(parsedline[2]), float(parsedline[3])))
            list.append(inarr, np.array([0,0,0], 'float32'))
        elif parsedline[0] == 'vn':
            list.append(tnarr, (float(parsedline[1]), float(parsedline[2]), float(parsedline[3])))
        elif parsedline[0] == 'f':
            fv = 0
            t = 0
            fn = -1
            p = parsedline[1].split('/')
            fv = p[0]
            if len(p)>=3:
                fn = p[2]
            fv = int(fv)
            fn = int(fn)
            sv = None
            sn = None
            face_normal = np.array([0.,0.,0.])
            cnt = 0
            it = ()
            cnttotal += 1
            
            for pl in parsedline[2:]:
                a = 0
                b = 0
                c = -1
                p = pl.split('/')
                a = p[0]
                if len(p)>=3:
                    c = p[2]
                a = int(a)
                c = int(c)
                if (sv != None) and (sn != None):
                    list.append(varr, tuple(np.array(tnarr[fn-1])/np.sqrt(np.dot(np.array(tnarr[fn-1]), np.array(tnarr[fn-1])))))
                    list.append(varr, tvarr[fv-1])
                    # inarr[fv-1] += np.array(tnarr[fn-1])
                    it += (fv-1,)
                    
                    list.append(varr, tuple(np.array(tnarr[sn-1])/np.sqrt(np.dot(np.array(tnarr[sn-1]), np.array(tnarr[sn-1])))))
                    list.append(varr, tvarr[sv-1])                   
                    # inarr[sv-1] += np.array(tnarr[sn-1])
                    it += (sv-1,)

                    list.append(varr, tuple(np.array(tnarr[c-1])/np.sqrt(np.dot(np.array(tnarr[c-1]), np.array(tnarr[c-1])))))
                    list.append(varr, tvarr[a-1])
                    # inarr[a-1] += np.array(tnarr[c-1])
                    it += (a-1,)

                    face_normal = np.cross(np.array(tvarr[sv - 1]) - np.array(tvarr[fv - 1]), np.array(tvarr[a - 1]) - np.array(tvarr[fv - 1]))
                    face_normal /= np.sqrt(np.dot(face_normal, face_normal))
                    
                    inarr[sv-1] += face_normal
                    
                    list.append(iarr, it)
                    it = ()
                    cnt += 1
                sv = a
                sn = c
            inarr[fv-1] += face_normal
            inarr[sv-1] += face_normal
            if cnt == 1:
                cnt3 += 1
            elif cnt == 2:
                cnt4 += 1
            else:
                cntn += 1
    varr = np.array(varr, 'float32')
    for i in range(len(tvarr)):
        d = np.sqrt(np.dot(inarr[i], inarr[i]))
        if d == 0:
            d = 1
        list.append(ivarr, tuple(inarr[i]/d))
        list.append(ivarr, tvarr[i])
    ivarr = np.array(ivarr, 'float32')
    
    iarr = np.array(iarr)

    print('file name : ' + paths[0])
    print('total # of faces : '+str(cnttotal))
    print('total # of faces with 3 vertices : '+str(cnt3))
    print('total # of faces with 4 vertices : '+str(cnt4))
    print('total # of faces with n vertices : '+str(cntn))
    
def key_callback(window, key, scancode, action, mods):
    global wiremode
    global smooth
    if action == glfw.PRESS:
        if key == glfw.KEY_Z:
            wiremode = not wiremode
        if key == glfw.KEY_S:
            smooth = not smooth
    
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
