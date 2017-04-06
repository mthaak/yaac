#version 110
//in vec4 color;
varying vec4 colorV;
void main()
{
    gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * gl_Vertex;
    colorV = gl_Color;
}