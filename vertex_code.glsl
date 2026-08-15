#version 330 core

in vec2 position;
in vec4 colour;
out vec4 vertColour;
uniform mat3 matrix;



void main() {

    vec3 homogenous_pos = vec3(position, 1.0);
    vec3 transformed_pos = matrix * homogenous_pos;
    //vec3 transformed_pos = position;

    gl_Position = vec4(transformed_pos.xy, 0.0, 1.0);

    vertColour = colour;

}