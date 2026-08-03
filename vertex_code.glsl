#version 330 core

in vec3 position;
in vec4 colour;
out vec4 vertColour;
uniform mat3 matrix;



void main() {

    vec3 transformed_pos = matrix * position;
    //vec3 transformed_pos = position;

    gl_Position = vec4(transformed_pos, 1.0);

    vertColour = colour;

}