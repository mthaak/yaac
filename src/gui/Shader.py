import os

from OpenGL.GL import *


class Shader:
    def __init__(self):
        # Compile all shaders in shaders folder
        path = 'gui/shaders/'
        shaders = {}
        for filename in os.listdir(path):
            if filename.endswith('.glsl'):
                source = self._get_shader_source(path + filename)
                if filename.endswith('vert.glsl'):
                    shaders[filename] = self._compile_vertex_shader(source)
                elif filename.endswith('frag.glsl'):
                    shaders[filename] = self._compile_fragment_shader(source)

        self.simple_program = self._link_shader_program(shaders['simple.vert.glsl'],
                                                        shaders['simple.frag.glsl'])
        self.normal_program = self._link_shader_program(shaders['vertex_shader.vert.glsl'],
                                                        shaders['fragment_shader.frag.glsl'])
        self.blur_program = self._link_shader_program(shaders['blur_shader.vert.glsl'],
                                                      shaders['blur_shader.frag.glsl'])
        self.depth_program = self._link_shader_program(shaders['depth.vert.glsl'],
                                                       shaders['depth.frag.glsl'])
        self.shadow_program = self._link_shader_program(shaders['shadow.vert.glsl'],
                                                        shaders['shadow.frag.glsl'])

    def useProgram(self, program):
        if program == 'blur':
            glUseProgram(self.blur_program)
        elif not program:
            glUseProgram(0)

    @staticmethod
    def _get_shader_source(filename):
        with open(filename) as file:
            return file.read()

    @staticmethod
    def _compile_vertex_shader(source):
        """Compile a vertex shader from source."""
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, source)
        glCompileShader(vertex_shader)
        # check compilation error
        result = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)
        if not result:
            raise RuntimeError(glGetShaderInfoLog(vertex_shader))
        return vertex_shader

    @staticmethod
    def _compile_fragment_shader(source):
        """Compile a fragment shader from source."""
        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, source)
        glCompileShader(fragment_shader)
        # check compilation error
        result = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS)
        if not result:
            raise RuntimeError(glGetShaderInfoLog(fragment_shader))
        return fragment_shader

    @staticmethod
    def _link_shader_program(vertex_shader, fragment_shader):
        """Create a shader program from compiled shaders."""
        program = glCreateProgram()
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)
        glLinkProgram(program)
        glDetachShader(program, vertex_shader)
        glDetachShader(program, fragment_shader)
        # check linking error
        result = glGetProgramiv(program, GL_LINK_STATUS)
        if not result:
            raise RuntimeError(glGetProgramInfoLog(program))
        return program
