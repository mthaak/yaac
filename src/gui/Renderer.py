import math
import os

import OpenGL.arrays.vbo as glvbo
import numpy
from OpenGL.GLU import *

from src.alg.ACO import RabbitColor
from src.gui.Shader import Shader
from src.gui.objloader import *
from src.map.Map import *

ENABLE_SHADERS = True


class TileModel(Enum):
    FLAT_DIRT = 'naturepack_extended/Models/naturePack_001.obj'
    RIVER_STRAIGHT_DIRT = 'naturepack_extended/Models/naturePack_002.obj'
    DECLINE_DIRT = 'naturepack_extended/Models/naturePack_003.obj'
    INCLINE_DIRT = 'naturepack_extended/Models/naturePack_004.obj'
    RIVER_CORNER_DIRT = 'naturepack_extended/Models/naturePack_091.obj'
    CLIFF_TOP_CORNER_DIRT = 'naturepack_extended/Models/naturePack_115.obj'
    CLIFF_TOP_WATERFALL_DIRT = 'naturepack_extended/Models/naturePack_125.obj'
    CLIFF_TOP_DIRT = 'naturepack_extended/Models/naturePack_127.obj'
    RIVER_END_DIRT = 'naturepack_extended/Models/naturePack_145.obj'
    RIVER_TJUNCTION_DIRT = 'naturepack_extended/Models/naturePack_146.obj'
    RIVER_JUNCTION_DIRT = 'naturepack_extended/Models/naturePack_147.obj'


class LayerType(Enum):
    TILES = 1
    FLOOR = 2
    PROPS_ENTITIES = 3


class Renderer:
    def __init__(self, viewport, map, alg):
        self.viewport = viewport
        self.map = map
        self.alg = alg
        if ENABLE_SHADERS:
            self.shader = Shader()

        # OPTIONS
        self.show_grid = False  # TODO currently used for question marks
        self.show_edges = True

        width, height = map.getSize()
        self.center_x = width / 2 * 3
        self.center_y = height / 2 * -3
        self.phi, self.theta = 90, 350  # used for camera position
        self.zpos = 15  # camera zoom

        self.background = self._texFromPNG('res/sky.png')

        self.tile_models = {}
        self.tile_models_mono = {}  # monocolored tiles

        self.prop_models = {}
        self.prop_models_mono = {}  # monocolored props

        self.rabbit_models = []
        self.rabbit_anim_frame = 0
        self.rabbit_anim_frames = 17
        self.rabbit_anim_counter = 0
        self.rabbit_anim_frame_length = 1

        self.entity_move_frame = 0
        self.entity_move_frames = 20

        self._loadModels()
        self.question_mark = self._charTexFromPNG('?', color=(255, 0, 0))  # used for show entity is lost

        # Used for selection
        self.selected_tile = None
        self.move_prop = None
        self.new_prop = None
        self.old_prop = None
        self.new_entity = None

        # Set up data for texture layers
        if ENABLE_SHADERS:
            self.data = numpy.array([
                -1.0, 1.0, 0.0, 0, 1.0,
                -1.0, -1.0, 0.0, 0, 0,
                1.0, -1.0, 0.0, 1.0, 0,
                1.0, 1.0, 0.0, 1.0, 1.0,
            ], dtype=numpy.float32)
            self.vbo = glvbo.VBO(self.data)

        # Set initial view settings
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        width, height = viewport
        gluPerspective(90.0, width / float(height), 1, 100.0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)
        glViewport(0, 0, self.viewport[0], self.viewport[1])

        # Initialise OpenGL settings
        glLightfv(GL_LIGHT0, GL_POSITION, (-40, 200, 100, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)  # most obj files expect to be smooth-shaded

        self.num_blur_layers = 5
        # Tile layers + grid layer + edges layer + prop layers
        self.num_layers = self.num_blur_layers + 2 + self.num_blur_layers
        self.grid_layer = self.num_blur_layers
        self.edges_layer = self.num_blur_layers + 1
        self.framebuffer, self.layers = self._createFrameBuffer(self.num_layers)
        self.current_layer = 0  # user for decreasing number of layer changes

    def reset(self):
        self.selected_tile = None
        self.move_prop = None
        self.new_prop = None
        self.old_prop = None
        self.new_entity = None
        self.rabbit_anim_frame = 0
        self.rabbit_anim_counter = 0
        self.entity_move_frame = 0

    def renderHUD(self, screen):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glDisable(GL_DEPTH_TEST)
        glLoadIdentity()
        screen.display()
        glEnable(GL_DEPTH_TEST)

    def renderLayers(self, selectedTile=None, selectedProp=None, redProp=None, greenProp=None):
        """Renders all the layers."""
        glEnable(GL_DEPTH_TEST)

        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)
        glViewport(0, 0, self.viewport[0], self.viewport[1])

        # Clear layers
        for i in range(self.num_layers):
            self._changeLayer(i)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glColor(1.0, 1.0, 1.0)
        glBindTexture(GL_TEXTURE_2D, 0)

        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)

        if self.show_edges:
            self._renderEdges()

        self._renderTiles(select=selectedTile)

        self._renderProps()

        self._renderEntities()

    def render(self):
        self.renderLayers()
        self._draw()

    def isAnimationDone(self):
        return self.entity_move_frame == 0

    def getTileCoords(self, x, y):
        """Gets the tile coordinates (i,j) for the tile under screen coordinates x, y."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self._resetCamera()
        self._renderTiles(pick=True)
        color = tuple(glReadPixels(x, self.viewport[1] - y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE))
        if color in list(self.colorToTile.keys()):
            return self.colorToTile[color]
        else:  # tile not found
            return None

    def getPropCoords(self, x, y):
        """Gets the prop coordinates (i,j) for the prop under screen coordinates x, y."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self._resetCamera()
        self._renderProps(pick=True)
        color = tuple(glReadPixels(x, self.viewport[1] - y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE))
        if color in list(self.colorToProp.keys()):
            return self.colorToProp[color]
        else:  # prop not found
            return None

    def toggleShowGrid(self):
        self.show_grid = not self.show_grid
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)
        # self._renderGrid()

    def toggleShowEdges(self):
        self.show_edges = not self.show_edges

    def updateGrid(self):
        self._renderGrid()

    def _createFrameBuffer(self, num_layers=1):
        framebuffer = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, framebuffer)

        # Create layers
        layers = []
        for _ in range(num_layers):
            texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture)

            # Give an empty image to OpenGL
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.viewport[0], self.viewport[1], 0, GL_RGBA, GL_UNSIGNED_BYTE,
                         None)

            # Poor filtering. Needed !
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            layers.append(texture)

        # The depth buffer
        depthrenderbuffer = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, depthrenderbuffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, self.viewport[0], self.viewport[1])
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, depthrenderbuffer)

        # Set colour attachment #0
        glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, layers[0], 0)

        # Set the list of draw buffers.
        glDrawBuffers(1, [GL_COLOR_ATTACHMENT0, GL_DEPTH_ATTACHMENT])

        # Always check that our framebuffer is ok
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            return False

        return framebuffer, layers

    def _resetCamera(self):
        """Sets the view such that it looks at the center of the map from the sky."""
        glLoadIdentity()
        width, height = self.map.getSize()
        self.center_x = 3 * width / 2
        self.center_y = -3 * height / 2
        self.center_z = 0.3
        to_rad = (math.pi / 180)
        self.cam_x = self.center_x + self.zpos * math.cos(self.phi * to_rad) * math.sin(self.theta * to_rad)
        self.cam_y = self.center_y + self.zpos * math.sin(self.phi * to_rad) * math.sin(self.theta * to_rad)
        self.cam_z = self.center_z + self.zpos * math.cos(self.theta * to_rad)
        # Set the camera position and look at point
        gluLookAt(self.cam_x, self.cam_y, self.cam_z,  # camera position
                  self.center_x, self.center_y, self.center_z,  # look at point
                  0.0, 0.0, 1.0)  # up vector

    def _draw(self):
        if ENABLE_SHADERS:
            self.vbo.bind()

        if ENABLE_SHADERS:
            # Prepare the shader
            position_attrib = glGetAttribLocation(self.shader.blur_program, 'position')
            coords_attrib = glGetAttribLocation(self.shader.blur_program, 'texCoords')
            res_uniform = glGetUniformLocation(self.shader.blur_program, 'iResolution')
            radius_uniform = glGetUniformLocation(self.shader.blur_program, 'radius')
            tex_uniform = glGetUniformLocation(self.shader.blur_program, 'iChannel0')
            bg_uniform = glGetUniformLocation(self.shader.blur_program, 'backgroundTexture')
            use_bg_uniform = glGetUniformLocation(self.shader.blur_program, 'useBG')
            fg_uniform = glGetUniformLocation(self.shader.blur_program, 'foregroundTexture')
            use_fg_uniform = glGetUniformLocation(self.shader.blur_program, 'useFG')

        if ENABLE_SHADERS:
            # Tell OpenGL that the VBO contains an array of vertices
            glEnableVertexAttribArray(0)
            glEnableVertexAttribArray(1)
            # these vertices contain 2 single precision coordinates
            glVertexAttribPointer(position_attrib, 3, GL_FLOAT, GL_FALSE, 20, None)
            glVertexAttribPointer(1, 2, GL_FLOAT, GL_TRUE, 20, ctypes.c_void_p(12))

        # Render to the screen
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glViewport(0, 0, self.viewport[0], self.viewport[
            1])  # Render on the whole framebuffer, complete from the lower left corner to the upper right

        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glNormal3f(0.0, 0.0, 1.0)  # reset normal

        if ENABLE_SHADERS:
            glUseProgram(self.shader.normal_program)

        glBindTexture(GL_TEXTURE_2D, self.background)
        if ENABLE_SHADERS:
            glDrawArrays(GL_QUADS, 0, 4)
        else:
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0)
            glVertex2f(-1.0, -1.0)
            glTexCoord2f(1, 0)
            glVertex2f(1.0, -1.0)
            glTexCoord2f(1, 1)
            glVertex2f(1.0, 1.0)
            glTexCoord2f(0, 1)
            glVertex2f(-1.0, 1.0)
            glEnd()

        if ENABLE_SHADERS:
            glUseProgram(self.shader.blur_program)
            glUniform3f(res_uniform, self.viewport[0], self.viewport[1], 1.0)
            glUniform1i(tex_uniform, 0)
            glUniform1i(bg_uniform, 1)
            glUniform1i(fg_uniform, 2)

        max_radius = 4
        step_radius = max_radius / int((self.num_blur_layers - 1) / 2)

        # Draw tile layers
        for i in range(0, self.num_blur_layers):
            center_i = int(self.num_blur_layers / 2)
            radius = abs(center_i - i) * step_radius
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.layers[i])
            if ENABLE_SHADERS:
                glUniform1f(radius_uniform, radius)
                if i > 0:
                    glUniform1f(use_bg_uniform, True)
                    glActiveTexture(GL_TEXTURE1)
                    glBindTexture(GL_TEXTURE_2D, self.layers[i - 1])
                else:
                    glUniform1f(use_bg_uniform, False)
                if i < self.num_blur_layers - 1:
                    glUniform1f(use_fg_uniform, True)
                    glActiveTexture(GL_TEXTURE2)
                    glBindTexture(GL_TEXTURE_2D, self.layers[i + 1])
                else:
                    glUniform1f(use_fg_uniform, False)

                glDrawArrays(GL_QUADS, 0, 4)
            else:
                glBegin(GL_QUADS)
                glTexCoord2f(0, 0)
                glVertex2f(-1.0, -1.0)
                glTexCoord2f(1, 0)
                glVertex2f(1.0, -1.0)
                glTexCoord2f(1, 1)
                glVertex2f(1.0, 1.0)
                glTexCoord2f(0, 1)
                glVertex2f(-1.0, 1.0)
                glEnd()
        glActiveTexture(GL_TEXTURE0)

        if ENABLE_SHADERS:
            glUseProgram(self.shader.normal_program)

        if self.show_edges:
            glBindTexture(GL_TEXTURE_2D, self.layers[self.edges_layer])
            if ENABLE_SHADERS:
                glDrawArrays(GL_QUADS, 0, 4)
            else:
                glBegin(GL_QUADS)
                glTexCoord2f(0, 0)
                glVertex2f(-1.0, -1.0)
                glTexCoord2f(1, 0)
                glVertex2f(1.0, -1.0)
                glTexCoord2f(1, 1)
                glVertex2f(1.0, 1.0)
                glTexCoord2f(0, 1)
                glVertex2f(-1.0, 1.0)
                glEnd()

        # TODO fix - does not do anything
        # if self.show_grid:
        #     glBindTexture(GL_TEXTURE_2D, self.layers[self.grid_layer])
        #     if ENABLE_SHADERS:
        #         glDrawArrays(GL_QUADS, 0, 4)
        #     else:
        #         glBegin(GL_QUADS)
        #         glTexCoord2f(0, 0)
        #         glVertex2f(-1.0, -1.0)
        #         glTexCoord2f(1, 0)
        #         glVertex2f(1.0, -1.0)
        #         glTexCoord2f(1, 1)
        #         glVertex2f(1.0, 1.0)
        #         glTexCoord2f(0, 1)
        #         glVertex2f(-1.0, 1.0)
        #         glEnd()

        if ENABLE_SHADERS:
            glUseProgram(self.shader.blur_program)

        # Draw prop layers (with entities)
        if ENABLE_SHADERS:
            glUniform1f(use_bg_uniform, False)
            glUniform1f(use_fg_uniform, False)
        for i in range(self.num_blur_layers + 2, self.num_layers):
            center_i = self.num_blur_layers + 2 + int(self.num_blur_layers / 2)
            radius = abs(center_i - i) * step_radius
            if ENABLE_SHADERS:
                glUniform1f(radius_uniform, radius)
            glBindTexture(GL_TEXTURE_2D, self.layers[i])
            if ENABLE_SHADERS:
                glDrawArrays(GL_QUADS, 0, 4)
            else:
                glBegin(GL_QUADS)
                glTexCoord2f(0, 0)
                glVertex2f(-1.0, -1.0)
                glTexCoord2f(1, 0)
                glVertex2f(1.0, -1.0)
                glTexCoord2f(1, 1)
                glVertex2f(1.0, 1.0)
                glTexCoord2f(0, 1)
                glVertex2f(-1.0, 1.0)
                glEnd()

        if ENABLE_SHADERS:
            glUseProgram(0)

        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_LIGHTING)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)

        if ENABLE_SHADERS:
            self.vbo.unbind()
            glBindVertexArray(0)
            glDisableVertexAttribArray(0)
            glDisableVertexAttribArray(1)

    def _renderGrid(self):
        """Prepares a display list for the grid."""
        # Load textures for characters
        chars = '0123456789,'
        # chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz' \
        #         '0123456789 !@#$%^&*()-=_+\|[]{};:\'",.<>/?`~'
        char_textures = {}
        for char in chars:
            char_textures[char] = self._charTexFromPNG(char)
        x_dev, y_dev = 2.3, 2.3
        width, height = self.map.getSize()

        self._changeLayer(self.grid_layer)

        self._resetCamera()

        glLineWidth(1.0)
        glColor3f(1.0, 0.0, 0.0)
        glDisable(GL_DEPTH_TEST)
        # Draw grid
        glBegin(GL_LINES)
        for i in range(1, width):
            glVertex3f(3 * i, -y_dev, 0.32)
            glVertex3f(3 * i, -3 * height + y_dev, 0.32)
        for j in range(1, height):
            glVertex3f(x_dev, -3 * j, 0.32)
            glVertex3f(3 * width - x_dev, -3 * j, 0.32)
        glEnd()

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Draw coordinates of grid cells
        char_width, char_height, margin = 0.6, 0.6, 0.1
        for i in range(0, width):
            for j in range(0, height):
                string = '{0},{1}'.format(i, j)
                for k, c in enumerate(string):
                    glBindTexture(GL_TEXTURE_2D, char_textures[c])
                    glBegin(GL_QUADS)
                    glTexCoord2f(0, 0)
                    glVertex3f(3 * i + margin + char_width * k, -3 * j - margin, 0.32)
                    glTexCoord2f(1, 0)
                    glVertex3f(3 * i + margin + char_width + char_width * k, -3 * j - margin, 0.32)
                    glTexCoord2f(1, 1)
                    glVertex3f(3 * i + margin + char_width + char_width * k, -3 * j - margin - char_height, 0.32)
                    glTexCoord2f(0, 1)
                    glVertex3f(3 * i + margin + char_width * k, -3 * j - margin - char_height, 0.32)
                    glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)

    def _renderEdges(self):
        edges = self.alg.edges

        self._changeLayer(self.edges_layer)  # TODO fix hack
        # glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, self.layers[self.edges_layer], 0)

        self._resetCamera()

        glLineWidth(1.0)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glBegin(GL_LINES)
        for (i, j, idest, jdest, r) in edges.keys():
            phero = edges[(i, j, idest, jdest, r)][1]
            glColor3f(0.015, phero, phero)  # 0.015 is chosen to distinguish the edge
            if not edges[(idest, jdest, i, j, (r + 180) % 360)][1] > phero:  # prevent draw in both directions
                glVertex3f(3 * i + 1.5, -3 * j - 1.5, 0.35)
                glVertex3f(3 * (i + idest) / 2 + 1.5, -3 * (j + jdest) / 2 - 1.5, 0.35)
                glVertex3f(3 * idest + 1.5, -3 * jdest - 1.5, 0.35)
                glVertex3f(3 * (i + idest) / 2 + 1.5, -3 * (j + jdest) / 2 - 1.5, 0.35)
            if r == 0:
                glVertex3f(3 * idest + 1.5, -3 * jdest - 1.5, 0.35)
                glVertex3f(3 * idest + 1.5 - 0.2, -3 * jdest - 1.5 - 0.5, 0.35)
                glVertex3f(3 * idest + 1.5, -3 * jdest - 1.5, 0.35)
                glVertex3f(3 * idest + 1.5 + 0.2, -3 * jdest - 1.5 - 0.5, 0.35)
            if r == 90:
                glVertex3f(3 * idest + 1.5, -3 * jdest - 1.5, 0.35)
                glVertex3f(3 * idest + 1.5 - 0.5, -3 * jdest - 1.5 + 0.2, 0.35)
                glVertex3f(3 * idest + 1.5, -3 * jdest - 1.5, 0.35)
                glVertex3f(3 * idest + 1.5 - 0.5, -3 * jdest - 1.5 - 0.2, 0.35)
            if r == 180:
                glVertex3f(3 * idest + 1.5, -3 * jdest - 1.5, 0.35)
                glVertex3f(3 * idest + 1.5 - 0.2, -3 * jdest - 1.5 + 0.5, 0.35)
                glVertex3f(3 * idest + 1.5, -3 * jdest - 1.5, 0.35)
                glVertex3f(3 * idest + 1.5 + 0.2, -3 * jdest - 1.5 + 0.5, 0.35)
            if r == 270:
                glVertex3f(3 * idest + 1.5, -3 * jdest - 1.5, 0.35)
                glVertex3f(3 * idest + 1.5 + 0.5, -3 * jdest - 1.5 + 0.2, 0.35)
                glVertex3f(3 * idest + 1.5, -3 * jdest - 1.5, 0.35)
                glVertex3f(3 * idest + 1.5 + 0.5, -3 * jdest - 1.5 - 0.2, 0.35)
        glEnd()
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)

    def _renderTiles(self, select=None, pick=False):
        """Renders the tiles.
        :type select: tuple (i,j), the selected tile
        :type pick: boolean, whether a tile was picked so that every tile should get a different color
        """
        self._resetCamera()

        if pick:
            glDisable(GL_TEXTURE_2D)
            glDisable(GL_LIGHTING)
            self.colorToTile = {}

        glDisable(GL_CULL_FACE)

        width, height = self.map.getSize()
        for j in range(height):
            for i in range(width):
                # Determine tile model id and orientation
                model_id, orientation = self._getTile(i, j)
                glRotate(-orientation, 0, 0, 1)
                if orientation == 90 or orientation == 180:
                    glTranslate(0, 3, 0)
                if orientation == 180 or orientation == 270:
                    glTranslate(-3, 0, 0)

                if model_id == TileModel.CLIFF_TOP_DIRT \
                        or model_id == TileModel.CLIFF_TOP_WATERFALL_DIRT:  # the cliff edges have a deviation
                    glTranslate(2.5, 0, 0.01)

                if model_id == TileModel.CLIFF_TOP_CORNER_DIRT:  # the cliff corners have a deviation as well
                    glTranslate(2.08, 0, 0.01)

                if pick:
                    color = (int(i / width * 255), int(j / height * 255), 255)
                    glColor3ub(*color)
                    self.colorToTile[color] = (i, j)
                    glCallList(self.tile_models_mono[model_id].gl_list)  # draw mono tile model
                elif select == (i, j):
                    glDisable(GL_LIGHTING)  # so that tile gets a slightly different shade (depends on angle though)
                    glCallList(self.tile_models[model_id].gl_list)  # draw tile model
                    glEnable(GL_LIGHTING)
                else:
                    x, y, z = 3 * i, -3 * j, 0
                    layer = self._determineLayer(LayerType.TILES, x, y, z)
                    self._changeLayer(layer)
                    glCallList(self.tile_models[model_id].gl_list)  # draw tile model

                if model_id == TileModel.CLIFF_TOP_DIRT \
                        or model_id == TileModel.CLIFF_TOP_WATERFALL_DIRT:  # the edges have a deviation
                    glTranslate(-2.5, 0, -0.01)

                if model_id == TileModel.CLIFF_TOP_CORNER_DIRT:  # the cliff corners have a deviation as well
                    glTranslate(-2.08, 0, -0.01)

                if orientation == 90 or orientation == 180:
                    glTranslate(0, -3, 0)
                if orientation == 180 or orientation == 270:
                    glTranslate(3, 0, 0)
                glRotate(orientation, 0, 0, 1)

                glTranslate(3, 0, 0)
            glTranslate(-3 * width, -3, 0)

        if pick:
            glEnable(GL_LIGHTING)
            glEnable(GL_TEXTURE_2D)

    def _renderProps(self, pick=False):
        self._resetCamera()

        props = self.map.getProps()
        if self.move_prop and type(self.move_prop) == Prop:
            selected_prop = [self.move_prop]
        else:
            selected_prop = []
        if self.new_prop:
            new_prop = [self.new_prop]
        else:
            new_prop = []

        if pick:
            glDisable(GL_TEXTURE_2D)
            glDisable(GL_LIGHTING)
            self.colorToProp = {}

        width, height = self.map.getSize()
        for prop in props + selected_prop + new_prop:
            if prop.i < 0 or prop.j < 0:  # not allowed
                continue

            dx, dy = self.prop_models_mono[prop.model].dx, self.prop_models_mono[prop.model].dy
            x, y, z = 3 * prop.i, -3 * prop.j, 0.3

            glTranslate(x + 0.5 * (3 - dx), y - 0.5 * (3 - dy), z)
            glRotate(-prop.r, 0, 0, 1)
            if prop.r == 90 or prop.r == 180:
                glTranslate(0, dx, 0)
            if prop.r == 180 or prop.r == 270:
                glTranslate(-dy, 0, 0)

            if pick:
                color = (int(prop.i / width * 255), int(prop.j / height * 255), 255)
                glColor3ub(*color)
                self.colorToProp[color] = (prop.i, prop.j)
                glCallList(self.prop_models_mono[prop.model].gl_list)  # draw mono prop model
            else:
                layer = self._determineLayer(LayerType.PROPS_ENTITIES, x, y, z)
                self._changeLayer(layer)
                if self.move_prop and \
                        ((type(self.move_prop) == tuple
                          and prop.i == self.move_prop[0] and prop.j == self.move_prop[1])
                         or (type(self.move_prop) == Prop
                             and prop.i == self.move_prop.i and prop.j == self.move_prop.j)):
                    glColor3f(1.0, 1.0, 1.0)
                    glCallList(self.prop_models_mono[prop.model].gl_list)  # draw prop model
                elif self.new_prop and prop.i == self.new_prop.i and prop.j == self.new_prop.j:
                    glColor3f(0.0, 1.0, 0.0)
                    glCallList(self.prop_models_mono[prop.model].gl_list)  # draw mono prop model
                elif self.old_prop and prop.i == self.old_prop[0] and prop.j == self.old_prop[1]:
                    glColor3f(1.0, 0.0, 0.0)
                    glCallList(self.prop_models_mono[prop.model].gl_list)  # draw mono prop model
                else:
                    glCallList(self.prop_models[prop.model].gl_list)  # draw prop model

            if prop.r == 90 or prop.r == 180:
                glTranslate(0, -dx, 0)
            if prop.r == 180 or prop.r == 270:
                glTranslate(dy, 0, 0)
            glRotate(prop.r, 0, 0, 1)

            glTranslate(-3 * prop.i - 0.5 * (3 - dx), 3 * prop.j + 0.5 * (3 - dy), -0.3)

        if pick:
            glEnable(GL_LIGHTING)
            glEnable(GL_TEXTURE_2D)

    def _renderEntities(self):
        """Renders all the entities."""
        entities = self.alg.getEntities()
        if self.new_entity:
            new_entity = [self.new_entity]
        else:
            new_entity = []

        self._resetCamera()

        scale = 0.05
        dev_x, dev_y = 1.5, -1.5
        for i, entity in enumerate(entities + new_entity):
            if entity.i < 0 or entity.j < 0:  # not allowed
                continue
            if entity.is_waiting or entity.is_home:
                if self.entity_move_frame == self.entity_move_frames - 1:
                    entity.in_home = True
            else:
                entity.in_home = False
            if hasattr(entity, 'in_home') and entity.in_home:
                continue  # do not draw if in home

            x, y, z = 3 * entity.i, -3 * entity.j, 0
            layer = self._determineLayer(LayerType.TILES, x, y, z)
            self._changeLayer(layer)

            glTranslate(3 * entity.i, -3 * entity.j, 0.25)

            glRotate(-entity.orient, 0, 0, 1)

            if entity.orient == 90 or entity.orient == 180:
                glTranslate(0, 3, 0)
            if entity.orient == 180 or entity.orient == 270:
                glTranslate(-3, 0, 0)

            glTranslate(dev_x, dev_y, 0)

            if not entity == self.new_entity:
                glTranslate(0, - 3 + self.entity_move_frame / self.entity_move_frames * 3, 0)

            if entity.is_lost:
                # Draw question mark
                rotation = entity.orient + self.phi + 90
                glRotate(rotation, 0, 0, 1)
                glTranslate(-0.25, 0, 1)
                glEnable(GL_TEXTURE_2D)
                glEnable(GL_BLEND)
                glDisable(GL_LIGHTING)
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
                glBindTexture(GL_TEXTURE_2D, self.question_mark)
                glBegin(GL_QUADS)
                glTexCoord2f(0, 0)
                glVertex3f(0, 0, 1)
                glTexCoord2f(1, 0)
                glVertex3f(1, 0, 1)
                glTexCoord2f(1, 1)
                glVertex3f(1, 0, 0)
                glTexCoord2f(0, 1)
                glVertex3f(0, 0, 0)
                glEnd()
                glEnable(GL_LIGHTING)
                glDisable(GL_BLEND)
                glDisable(GL_TEXTURE_2D)
                glTranslate(0.5, 0, -1)
                glRotate(-rotation, 0, 0, 1)

            glScale(scale, scale, scale)
            if entity == self.new_entity:
                glColor3f(0.0, 1.0, 0.0)  # draw in green
            # Give the rabbits a different color
            elif entity.color == RabbitColor.WHITE:
                glColor(1.0, 1.0, 1.0)
            elif entity.color == RabbitColor.GREY:
                glColor(0.1, 0.1, 0.1)
            elif entity.color == RabbitColor.BLACK:
                glColor(0.0, 0.0, 0.0)
            elif entity.color == RabbitColor.BROWN:
                glColor(0.40, 0.27, 0.20)
            elif entity.color == RabbitColor.BEIGE:
                glColor(0.95, 0.84, 0.62)
            elif entity.color == RabbitColor.ORANGE:
                glColor(0.80, 0.39, 0.16)
            glCallList(self.rabbit_models[self.rabbit_anim_frame].gl_list)
            glScale(1 / scale, 1 / scale, 1 / scale)

            glTranslate(-dev_x, -dev_y, 0)

            if not entity == self.new_entity:
                glTranslate(0, 3 - self.entity_move_frame / self.entity_move_frames * 3, 0)

            if entity.orient == 90 or entity.orient == 180:
                glTranslate(0, -3, 0)
            if entity.orient == 180 or entity.orient == 270:
                glTranslate(3, 0, 0)

            glRotate(entity.orient, 0, 0, 1)
            glTranslate(-3 * entity.i, 3 * entity.j, -0.25)

        self.rabbit_anim_counter += 1
        if self.rabbit_anim_counter > self.rabbit_anim_frame_length:
            self.rabbit_anim_frame = (self.rabbit_anim_frame + 1) % self.rabbit_anim_frames
            self.rabbit_anim_counter = 0

        self.entity_move_frame = (self.entity_move_frame + 1) % self.entity_move_frames

    def _getTile(self, i, j):
        """Determines model id and orientation for some tile."""
        tiles = self.map.getTiles()
        width, height = self.map.getSize()
        model_id, orientation = 0, 0
        if ((i == 0 or i == width - 1) and not (j == 0 or j == height - 1)) \
                or ((j == 0 or j == height - 1) and not (i == 0 or i == width - 1)):
            if tiles[i][j] == TileType.LAND.value:
                model_id = TileModel.CLIFF_TOP_DIRT
            elif tiles[i][j] == TileType.WATER.value:
                model_id = TileModel.CLIFF_TOP_WATERFALL_DIRT
            if i == 0:
                orientation = 0
            elif j == 0:
                orientation = 90
            elif i == width - 1:
                orientation = 180
            elif j == height - 1:
                orientation = 270

        elif (i == 0 or i == width - 1) and (j == 0 or j == height - 1):
            model_id = TileModel.CLIFF_TOP_CORNER_DIRT
            if i == 0 and j == 0:
                orientation = 90
            elif i == 0 and j == height - 1:
                orientation = 0
            elif i == width - 1 and j == 0:
                orientation = 180
            elif i == width - 1 and j == height - 1:
                orientation = 270
        else:
            if tiles[i][j] == TileType.LAND.value:
                model_id = TileModel.FLAT_DIRT
            elif tiles[i][j] == TileType.WATER.value:
                neighbours = tiles[i][j - 1], tiles[i + 1][j], tiles[i][j + 1], tiles[i - 1][j]  # n, e, s, w
                if neighbours == (0, 0, 0, 0):
                    model_id = TileModel.RIVER_END_DIRT  # TODO create water pool
                elif neighbours == (1, 0, 0, 0):
                    model_id = TileModel.RIVER_END_DIRT
                    orientation = 0
                elif neighbours == (0, 1, 0, 0):
                    model_id = TileModel.RIVER_END_DIRT
                    orientation = 90
                elif neighbours == (0, 0, 1, 0):
                    model_id = TileModel.RIVER_END_DIRT
                    orientation = 180
                elif neighbours == (0, 0, 0, 1):
                    model_id = TileModel.RIVER_END_DIRT
                    orientation = 270
                elif neighbours == (1, 0, 1, 0):
                    model_id = TileModel.RIVER_STRAIGHT_DIRT
                elif neighbours == (0, 1, 0, 1):
                    model_id = TileModel.RIVER_STRAIGHT_DIRT
                    orientation = 90
                elif neighbours == (1, 1, 0, 0):
                    model_id = TileModel.RIVER_CORNER_DIRT
                    orientation = 180
                elif neighbours == (0, 1, 1, 0):
                    model_id = TileModel.RIVER_CORNER_DIRT
                    orientation = 270
                elif neighbours == (0, 0, 1, 1):
                    model_id = TileModel.RIVER_CORNER_DIRT
                    orientation = 0
                elif neighbours == (1, 0, 0, 1):
                    model_id = TileModel.RIVER_CORNER_DIRT
                    orientation = 90
                elif neighbours == (1, 1, 1, 0):
                    model_id = TileModel.RIVER_TJUNCTION_DIRT
                    orientation = 180
                elif neighbours == (0, 1, 1, 1):
                    model_id = TileModel.RIVER_TJUNCTION_DIRT
                    orientation = 270
                elif neighbours == (1, 0, 1, 1):
                    model_id = TileModel.RIVER_TJUNCTION_DIRT
                    orientation = 0
                elif neighbours == (1, 1, 0, 1):
                    model_id = TileModel.RIVER_TJUNCTION_DIRT
                    orientation = 90
                elif neighbours == (1, 1, 1, 1):
                    model_id = TileModel.RIVER_JUNCTION_DIRT
        return model_id, orientation

    def _determineLayer(self, layer_type, x, y, z):
        assert layer_type in LayerType
        if layer_type == LayerType.FLOOR:
            layer = self.num_blur_layers
        else:
            cam_dist = math.sqrt((x - self.cam_x) ** 2 +
                                 (y - self.cam_y) ** 2 +
                                 (z - self.cam_z) ** 2)
            focus_dist = 25  # zoom such that item is in focus
            focus_layer = int(self.num_blur_layers / 2)
            max_blur_dist = 30
            min_layer, max_layer = 0, self.num_blur_layers - 1
            step = max_blur_dist / self.num_blur_layers
            layer = min(max(focus_layer + int((focus_dist - cam_dist) / step), min_layer), max_layer)
            if layer_type == LayerType.PROPS_ENTITIES:
                layer += self.num_blur_layers + 2  # tile layers, grid layer and edges layer
        return layer

    def _changeLayer(self, layer):
        if layer != self.current_layer:
            glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, self.layers[layer], 0)
            self.current_layer = layer

    def _loadModels(self):
        os.chdir('../res/')

        # Load tiles
        os.chdir('naturepack_extended/Models/')
        for model in TileModel:
            filename = os.path.basename(model.value)
            self.tile_models[model] = OBJ(filename, swapyz=True)
            self.tile_models_mono[model] = OBJ(filename, swapyz=True, monocolor=True)
        os.chdir('../../')

        # Load props
        os.chdir('naturepack_extended/Models/')
        for model in PropModel:
            if type(model.value) == str and 'naturepack_extended' in model.value:
                filename = os.path.basename(model.value)
                self.prop_models[model] = OBJ(filename, swapyz=True)
                self.prop_models_mono[model] = OBJ(filename, swapyz=True, monocolor=True)
        os.chdir('../../')  # change back
        self.prop_models[PropModel.HOLE] = OBJ(PropModel.HOLE.value, swapyz=True)
        self.prop_models_mono[PropModel.HOLE] = OBJ(PropModel.HOLE.value, swapyz=True, monocolor=True)

        # Load entities
        os.chdir('rabbit/anim_run/')
        for frame in range(self.rabbit_anim_frames):
            self.rabbit_models.append(OBJ('rabbit_{0:06d}.obj'.format(frame), swapyz=True, monocolor=True))
        os.chdir('../../')

        os.chdir('../src/')

    def _texFromPNG(self, filename):
        """Creates a texture from a PNG image."""
        img = pygame.image.load('../' + filename)
        img_data = numpy.array(list(img.get_view().raw), numpy.uint8)

        texture = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.get_size()[0], img.get_size()[1], 0, GL_RGBA, GL_UNSIGNED_BYTE,
                     img_data)
        return texture

    def _charTexFromPNG(self, char, color=None):
        """Creates a texture of a text character from a image of characters."""
        # Draw coordinates
        os.chdir('gui/bmpfont')
        from src.gui.bmpfont.bmpfont import BmpFont
        bmpfont = BmpFont()
        img = pygame.image.load('font.png')
        os.chdir('../..')
        img_data = numpy.array(list(img.get_view().raw), numpy.uint8)

        if color:
            for i in range(0, len(img_data), 4):
                if img_data[i] != 255 or img_data[i + 1] != 255 or img_data[i + 2] != 255:
                    img_data[i], img_data[i + 1], img_data[i + 2] = color[0], color[1], color[2]

        width, height, chars_per_line = 8, 16, 8
        img_x, img_y = bmpfont.chartable[char]
        img_char = numpy.array([])  # pixels of character
        for y in range(img_y, img_y + height):
            img_char = numpy.append(img_char,
                                    img_data[4 * (y * chars_per_line * width + img_x):
                                    4 * (y * chars_per_line * width + img_x + width)])

        texture = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 8, 16, 0, GL_RGBA, GL_UNSIGNED_BYTE,
                     img_char)
        return texture
