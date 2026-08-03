#coicles in 2D

import glfw
from OpenGL.GL import *
import numpy as np
import fractions
import sympy
import math as maths

from geo_funcs import circle_data


# --------------------- CREATE WINDOW CONTEXT ---------------------
#initialise glfw
glfw.init()

#create window
window = glfw.create_window(800,800,"hi bob!",None,None)

#make sure it knows where its rendering to
glfw.make_context_current(window)


# --------------------- SHADERS ---------------------
#request program and shader slots
program = glCreateProgram()
vertex = glCreateShader(GL_VERTEX_SHADER)
fragment = glCreateShader(GL_FRAGMENT_SHADER)
#shaders code
vertex_code = """
    attribute float theta;
    attribute vec2 position;
    varying vec2 frag_pos;

    void main() { 
        float cosr = cos(theta);
        float sinr = sin(theta);
        float coso = cos(theta/4);
        float sino = sin(theta/4);
        float x = 0.75 * (position.x *cosr - position.y *sinr + (0.7 * coso - 0.7 * sino));
        float y = 0.75 * (position.x *sinr + position.y *cosr + (0.7 * coso + 0.7 * sino));

        frag_pos = position;

        gl_Position = vec4(x, y, 0.0, 1.0); 
    }"""
fragment_code = """
    varying vec2 frag_pos;

    void main() { 

        float r = (frag_pos[0] + 1) * 0.5;
        float g = (frag_pos[1] + 1) * 0.5;
        float b = 1.0 - (r + g);

        gl_FragColor = vec4(r, g, b, 1.0); 
    }"""

#set shaders source
glShaderSource(vertex, vertex_code)
glShaderSource(fragment, fragment_code)

#compile shaders
glCompileShader(vertex)
if not glGetShaderiv(vertex, GL_COMPILE_STATUS):#if compile status is 0
    print(glGetShaderInfoLog(vertex).decode()) #get error, decode binary string, output error
    raise RuntimeError("Vertex shader compilation error") #stop code so it doesn't go haywire

glCompileShader(fragment)
if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
    print(glGetShaderInfoLog(fragment).decode()) 
    raise RuntimeError("Fragment shader compilation error") 

#link shaders to program
glAttachShader(program, vertex)
glAttachShader(program, fragment)
glLinkProgram(program)

if not glGetProgramiv(program, GL_LINK_STATUS): #same error checking logic
    print(glGetProgramInfoLog(program))
    raise RuntimeError('Linking error')

#detach shaders (now obsolete after linking)
glDetachShader(program, vertex)
glDetachShader(program, fragment)


# --------------------- INITIALISE CALCULATION VARIABLES ---------------------
theta = maths.pi / 45
num_sides = 720
num_verts = num_sides + 2
x = 0
y = 0
radius = 0.25

# --------------------- LOOP ---------------------
#set frame rate to vsync
glfw.swap_interval(1)

#make window stay open and display
while not glfw.window_should_close(window):

    # --------------------- CALCULATE NEW ANGLE ---------------------
    theta = theta + (maths.pi/45)

    # --------------------- BUILD DATA ---------------------
    #make a template for the storage of the 4 (x,y) coords in a zero matrix
    data = np.zeros(num_verts, [("position", np.float32, 2), ("theta", np.float32, 1)]) #structured array woooo!
    #assign CPU data
    data['position'] = circle_data(x, y, radius, num_sides) 
    #data['colour'] = [(0.9,0,1,1), (0.1,0.4,1,1), (1,0.5,0,1), (1,0.8,0,1)]
    data['theta'] = theta


    # --------------------- BUFFER ---------------------
    #request 1 GPU buffer slot and set it as the default buffer
    buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, buffer)
    #upload CPU data to GPU buffer
    glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)


    # --------------------- BIND POSITION AND COLOUR ATTRIBUTES ---------------------
    #position
    #tell GPU how to read data
    stride = data.strides[0] #calculates stride (how many bytes the gpu has to skip to get to the next piece of data). 0 means it looks at axis 0 (rows of matrix) and calculates how many bytes each row takes up
    offset = ctypes.c_void_p(0) #sets offset to zero (start reading data from the 0th byte), turns data into C data

    #tell GPU how data is formatted and where it is
    loc = glGetAttribLocation(program, "position")
    glEnableVertexAttribArray(loc) #unlocks slot
    glVertexAttribPointer(loc, 2, GL_FLOAT, GL_FALSE, stride, offset)

    #colour
    #stride is the same
    #offset = ctypes.c_void_p(8)

    #loc = glGetAttribLocation(program, "colour")
    #glEnableVertexAttribArray(loc)
    #glVertexAttribPointer(loc, 4, GL_FLOAT, GL_FALSE, stride, offset)

    #theta
    offset = ctypes.c_void_p(8)

    loc = glGetAttribLocation(program, "theta")
    glEnableVertexAttribArray(loc)
    glVertexAttribPointer(loc, 1, GL_FLOAT, GL_FALSE, stride, offset)


    # --------------------- WINDOW LOOP ---------------------
    glfw.poll_events()
    #set program as default program to be ran by GPU
    glUseProgram(program)

    glClear(GL_COLOR_BUFFER_BIT)
    glDrawArrays(GL_TRIANGLE_FAN, 0, num_verts) #GL_TRIANGLE_FAN is a 'drawing primitive'

    glfw.swap_buffers(window)
        