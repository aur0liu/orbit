#overcomplicated zoom in and out square (no easing)

import glfw
from OpenGL.GL import *
import numpy as np
import fractions
import sympy
import math as maths

# --------------------- CREATE WINDOW CONTEXT ---------------------
#initialise glfw
glfw.init()

#create window
window = glfw.create_window(800,600,"hi bob!",None,None)

#make sure it knows where its rendering to
glfw.make_context_current(window)


# --------------------- SHADERS ---------------------
#request program and shader slots
program = glCreateProgram()
vertex = glCreateShader(GL_VERTEX_SHADER)
fragment = glCreateShader(GL_FRAGMENT_SHADER)
#shaders code
vertex_code = """
    attribute vec2 position;
    attribute vec4 colour;
    varying vec4 v_colour;
    void main() { 
    gl_Position = vec4(position, 0.0, 1.0); 
    v_colour = colour;
    }"""
fragment_code = """
    varying vec4 v_colour;
    void main() { 
    gl_FragColor = v_colour; 
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
zoom = 0
step = fractions.Fraction(1,90) #* sympy.sqrt(2)
vertex1 = [-1 - step, 1 + step]

# --------------------- LOOP ---------------------
#set frame rate to vsync
glfw.swap_interval(1)

#make window stay open and display
while not glfw.window_should_close(window):

    # --------------------- CALCULATE NEW POSITIONS OF VERTICES ---------------------
    if zoom % 2 == 0: #if zoom is 0 or even (getting smaller)
        vertex1 = [vertex1[0]+ step, vertex1[1] - step]
        vertex2 = [-vertex1[0], vertex1[1]]
        vertex3 = [vertex1[0], -vertex1[1]]
        vertex4 = [-vertex1[0], -vertex1[1]]

    else: #if zoom is odd (getting bigger)
        vertex1 = [vertex1[0]- step, vertex1[1] + step]
        vertex2 = [-vertex1[0], vertex1[1]]
        vertex3 = [vertex1[0], -vertex1[1]]
        vertex4 = [-vertex1[0], -vertex1[1]]

    if vertex1 == [0, 0] or (vertex1 ==[-1,1] and zoom != 0) :
        zoom = zoom + 1


    # --------------------- BUILD DATA ---------------------
    #make a template for the storage of the 4 (x,y) coords in a zero matrix
    data = np.zeros(4, [("position", np.float32, 2), ("colour", np.float32, 4)]) #structured array woooo!
    #assign CPU data
    data['position'] = [(vertex1), (vertex2), (vertex3), (vertex4)] 
    data['colour'] = [(0.9,0,1,1), (0.1,0.4,1,1), (1,0.5,0,1), (1,0.8,0,1)]


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
    offset = ctypes.c_void_p(8)

    loc = glGetAttribLocation(program, "colour")
    glEnableVertexAttribArray(loc)
    glVertexAttribPointer(loc, 4, GL_FLOAT, GL_FALSE, stride, offset)


    # --------------------- WINDOW LOOP ---------------------
    glfw.poll_events()
    #set program as default program to be ran by GPU
    glUseProgram(program)

    glClear(GL_COLOR_BUFFER_BIT)
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    glfw.swap_buffers(window)
        