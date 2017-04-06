#version 330
uniform sampler2D texUnit;
in vec2 theCoords;
out vec4 outputColour;
void main()
{
    outputColour = texture(texUnit, theCoords);
}