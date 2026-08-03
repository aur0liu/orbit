import numpy as np
import math as maths
from OpenGL.GL import *

def circle_data(x, y, radius, num_sides):
    num_verts = num_sides + 2 #need a centre point and the first point repeated (to draw final triangle)

    TWO_PI = maths.pi * 2

    circle_vertex_x = np.zeros(num_verts)
    circle_vertex_y = np.zeros(num_verts)

    circle_vertex_x[0] = x
    circle_vertex_y[0] = y

    for i in range(0, num_verts):
        circle_vertex_x[i] = x + (radius * maths.cos(i * TWO_PI/num_sides))
        circle_vertex_y[i] = y + (radius * maths.sin(i * TWO_PI/num_sides))

    circle_vertices_all = np.zeros((num_verts, 2))

    for i in range(num_verts):
        circle_vertices_all[i, 0] = circle_vertex_x[i]
        circle_vertices_all[i, 1] = circle_vertex_y[i]

    return circle_vertices_all



def body_verts(x, y, radius, num_sides, WORLD_TO_SCREEN):
    num_verts = num_sides + 2 #need a centre point and the first point repeated (to draw final triangle)

    x = WORLD_TO_SCREEN * x
    y = WORLD_TO_SCREEN * y
    radius = WORLD_TO_SCREEN * radius

    TWO_PI = maths.pi * 2

    circle_vertex_x = np.zeros(num_verts)
    circle_vertex_y = np.zeros(num_verts)
    circle_vertex_w = np.zeros(num_verts)

    circle_vertex_x[0] = x
    circle_vertex_y[0] = y

    for i in range(0, num_verts):
        circle_vertex_x[i] = x + (radius * maths.cos(i * TWO_PI/num_sides))
        circle_vertex_y[i] = y + (radius * maths.sin(i * TWO_PI/num_sides))
        circle_vertex_w[i] = 1.0

    circle_vertices_all = np.zeros((num_verts, 3))

    for i in range(num_verts):
        circle_vertices_all[i, 0] = circle_vertex_x[i]
        circle_vertices_all[i, 1] = circle_vertex_y[i]
        circle_vertices_all[i, 2] = circle_vertex_w[i]


    return circle_vertices_all

    

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




                


# input: data to be built ()
# output: none
# result: data built into a  ready to be sent to the gpu
def build_data():
    ...