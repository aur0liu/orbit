#a planet orbiting a star in 2D

import glfw
from OpenGL.GL import *
import numpy as np
import math as maths

from geo_funcs import *


# --------------------- CREATE WINDOW CONTEXT ---------------------
#initialise glfw, create core profile (modern) context
glfw.init()
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

#create window
window = glfw.create_window(800,800,"hi bob!",None,None)

#make sure it knows where its rendering to
glfw.make_context_current(window)

#set frame rate to vsync
glfw.swap_interval(1)

# --------------------- SHADERS ---------------------
#request program and shader slots
program = glCreateProgram()
compile_shaders(program, 'vertex_code.glsl', 'fragment_code.glsl')


# --------------------- INITIALISE SYSTEM STATE ---------------------
#constants
G = (6.674 * 10**11) * ((6 * 10**24)/(10**27))
    #real value         #scale factor
#worldspace to screenspace multiplier
WORLD_TO_SCREEN = 1/175
#timestep
dt = 1/60


class Body:
    def __init__(self, mass, x, y, vx, vy, radius, num_sides, colour, rotate):
        self.mass: int = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

        self.radius = radius
        self.num_sides = num_sides
        self.colour = colour
        self.rotate = rotate 

        self.verts_raw = body_verts(self.x, self.y, self.radius, self.num_sides, 1)
        self.verts_scaled = body_verts(self.x, self.y, self.radius, self.num_sides, WORLD_TO_SCREEN)
        



planet = Body(1, 150, 0, 0, 0, 6, 30, (0.1,1,0.1,1), 0)
star = Body(333000, 0, 0, 0, 0, 10, 80, (1,0.9,0,1), 0)

bodies = [planet, star]

#determine initial velocity for stable orbit
for body in bodies: #for each body calculate its initial velocity
    velocity = 0
    total_vx = 0
    total_vy = 0
    for other in bodies: #caclulate force on body from every other body
        if other != body and (body.mass/other.mass) < 0.01: #only calculate this if mass of body is much smaller than other body
            dx = other.x - body.x
            dy = other.y - body.y
            r = maths.sqrt(dx**2 + dy**2)
            
            velocity += maths.sqrt((G*other.mass*body.mass)/r) #find velocity by equating gravitational force with required centripetal force
            total_vx += velocity * (-dy/r) 
            total_vy += velocity * (dx/r)
    body.vx = total_vx 
    body.vy = total_vy 
    print(f'initial vx is {body.vx}, initial vy is {body.vy}')



# --------------------- VBO/VAOS ---------------------
#request 1 GPU buffer slot and set it as the vertex buffer object
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)

#set the vertex array object 
vao = glGenVertexArrays(1)
glBindVertexArray(vao)


# --------------------- BUILD DATA ---------------------
#make a template for the storage of the data in a zero matrix

data_list = []
for body in bodies:
    data_send = np.zeros([body.num_sides + 2], [("position", np.float32, 3), ("colour", np.float32, 4)])
    data_send['position'] = body.verts_scaled
    data_send['colour'] = body.colour
    data_list.append(data_send)

data = np.concatenate(data_list)

# --------------------- BUFFER ---------------------
#upload CPU data to GPU buffer
glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)


# --------------------- BIND DATA ---------------------
#position
#tell GPU how to read data
stride = data.strides[0] #calculates stride (how many bytes the gpu has to skip to get to the next piece of data). 0 means it looks at axis 0 (rows of matrix) and calculates how many bytes each row takes up
offset = ctypes.c_void_p(0) #sets offset to zero (start reading data from the 0th byte), turns data into C data

#tell GPU how data is formatted and where it is
attrib_loc = glGetAttribLocation(program, "position")
glEnableVertexAttribArray(attrib_loc) #unlocks slot
glVertexAttribPointer(attrib_loc, 2, GL_FLOAT, GL_FALSE, stride, offset)


offset = ctypes.c_void_p(12)

attrib_loc = glGetAttribLocation(program, "colour")
glEnableVertexAttribArray(attrib_loc) #unlocks slot
glVertexAttribPointer(attrib_loc, 4, GL_FLOAT, GL_FALSE, stride, offset)



# --------------------- WINDOW LOOP ---------------------
while not glfw.window_should_close(window):
    start_index = 0

    glClear(GL_COLOR_BUFFER_BIT)
    glfw.poll_events()
    #set program as default program to be ran by GPU
    glUseProgram(program)

    
   

    for body in bodies: 
        acc_x = 0
        acc_y = 0

        for other in bodies:
            if other != body and (body.mass/other.mass) < 0.01:
                #calculate distance between bodies
                dx = other.x - body.x
                dy = other.y - body.y
                print(f'dx: {dx}, dy: {dy}')
                r = maths.sqrt(dx**2 + dy**2)
                print(f'r:{r}')

                #acceleration
                acc = G * (other.mass)/(r**2)
                print(f'acc:{acc}')

                acc_x += acc * (dx/r) #using trig ratios rather than trig functions to calculate acc
                acc_y += acc * (dy/r)
                print(f'acc_x: {acc_x}, acc_y: {acc_y}')
                
        #velocity
        body.vx += acc_x * dt #euler integration further pure yayyy
        body.vy += acc_y * dt
        print(f'vx:{body.vx}, vy:{body.vy}')
        
        #position
        body.x += body.vx * dt
        body.y += body.vy * dt  
        print(f'x:{body.x}, y:{body.y}') 


        #calculate new matrix
        matrix = np.array(
            [
            [1.0, 0.0, body.x * WORLD_TO_SCREEN], 
            [0.0, 1.0, body.y * WORLD_TO_SCREEN], 
            [0.0, 0.0, 1.0]
            ],
            dtype = np.float32
            )
        print(matrix)
        
        #get uniform location for matrix
        uniform_loc = glGetUniformLocation(program, "matrix")
        glUniformMatrix3fv(uniform_loc, 1, GL_FALSE, matrix)


        #draw body
        count = body.num_sides + 2
        glDrawArrays(GL_TRIANGLE_FAN, start_index, count) #GL_TRIANGLE_FAN is a 'drawing primitive'


        start_index += count

    quit()
    

    glfw.swap_buffers(window)
            