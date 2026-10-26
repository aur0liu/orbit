#all the opengl- rendering-related functions 

import numpy as np
import math as maths
import glfw
from OpenGL.GL import *


#what it says on the tin- compiles the shaders
def compile_shaders(program, vertex_file, frag_file):
    #request shader slots
    vertex = glCreateShader(GL_VERTEX_SHADER)
    fragment = glCreateShader(GL_FRAGMENT_SHADER)
    
    #open shader files and set them as the shader source 
    with open(vertex_file, "r") as vertex_working_file:
        vertex_code = vertex_working_file.read()

    with open(frag_file, "r") as frag_working_file:
        frag_code = frag_working_file.read()


    glShaderSource(vertex, vertex_code)
    glShaderSource(fragment, frag_code)

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



#initialises the graphics system
def initialise_gl():
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


    # --------------------- VBO/VAOS ---------------------
    #request 1 GPU buffer slot and set it as the vertex buffer object
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    #set the vertex array object 
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    return window, program



#calculates vertices of a circular body to send to the shaders
def body_verts(radius, num_sides, WORLD_TO_SCREEN):
    num_verts = num_sides + 2 #need a centre point and the first point repeated (to draw final triangle)


    radius = WORLD_TO_SCREEN * radius

    TWO_PI = maths.pi * 2

    circle_vertex_x = np.zeros(num_verts)
    circle_vertex_y = np.zeros(num_verts)
    circle_vertex_w = np.zeros(num_verts)

    circle_vertex_x[0] = 0
    circle_vertex_y[0] = 0

    for i in range(0, num_verts):
        circle_vertex_x[i] =  (radius * maths.cos(i * TWO_PI/num_sides))
        circle_vertex_y[i] =  (radius * maths.sin(i * TWO_PI/num_sides))
        circle_vertex_w[i] = 1.0

    circle_vertices_all = np.zeros((num_verts, 3))

    for i in range(num_verts):
        circle_vertices_all[i, 0] = circle_vertex_x[i]
        circle_vertices_all[i, 1] = circle_vertex_y[i]
        circle_vertices_all[i, 2] = circle_vertex_w[i]


    return circle_vertices_all




#builds and uploads data
def build_data(bodies):

    #build data
    data_list = []
    for body in bodies:
        data_send = np.zeros([body.num_sides + 2], [("position", np.float32, 3), ("colour", np.float32, 4)])
        data_send['position'] = body.verts_scaled
        data_send['colour'] = body.colour
        data_list.append(data_send)

    data = np.concatenate(data_list)

    #upload CPU data to GPU buffer
    glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)




#calculate stride and offset and send them to the gpu
def attribute_format(data, program):
    
    #tell GPU how to read data
    stride = data.strides[0] #calculates stride (how many bytes the gpu has to skip to get to the next piece of data). 0 means it looks at axis 0 (rows of matrix) and calculates how many bytes each row takes up
    offset = ctypes.c_void_p(0) #sets offset to zero (start reading data from the 0th byte), turns data into C data

    #tell GPU how data is formatted and where it is
    #position attribute
    attrib_loc = glGetAttribLocation(program, "position")
    glEnableVertexAttribArray(attrib_loc) #unlocks slot
    glVertexAttribPointer(attrib_loc, 2, GL_FLOAT, GL_FALSE, stride, offset)

    #colour attribute
    offset = ctypes.c_void_p(12)
    attrib_loc = glGetAttribLocation(program, "colour")
    glEnableVertexAttribArray(attrib_loc) #unlocks slot
    glVertexAttribPointer(attrib_loc, 4, GL_FLOAT, GL_FALSE, stride, offset)



#calculates the new transforming matrix and tells the shaders to draw the bodies each frame
def render_body(body, program, WORLD_TO_SCREEN):
    #calculate new matrix
    matrix = np.array(
        [
        [1.0, 0.0, body.x * WORLD_TO_SCREEN], 
        [0.0, 1.0, body.y * WORLD_TO_SCREEN], 
        [0.0, 0.0, 1.0]
        ],
        dtype = np.float32
        )
    
    #get uniform location for matrix
    uniform_loc = glGetUniformLocation(program, "matrix")
    glUniformMatrix3fv(uniform_loc, 1, GL_TRUE, matrix)


    #draw body
    count = body.num_sides + 2
    glDrawArrays(GL_TRIANGLE_FAN, start_index, count) #GL_TRIANGLE_FAN is a 'drawing primitive'


    start_index += count
