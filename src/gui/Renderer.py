import math
import os

import numpy
from OpenGL.GL import *
from OpenGL.GLU import *

from src.gui.objloader import *
from src.map.Map import *


class TileModel(Enum):
    FLAT_DIRT = 1
    RIVER_STRAIGHT_DIRT = 2
    DECLINE_DIRT = 3
    INCLINE_DIRT = 4
    RIVER_CORNER_DIRT = 91
    CLIFF_TOP_CORNER_DIRT = 115
    CLIFF_TOP_WATERFALL_DIRT = 125
    CLIFF_TOP_DIRT = 127
    RIVER_END_DIRT = 145
    RIVER_TJUNCTION_DIRT = 146
    RIVER_JUNCTION_DIRT = 147


class Renderer:
    def __init__(self):
        self.phi, self.theta = 0, 350
        self.zpos = 15

        model_ids = [TileModel.FLAT_DIRT,
                     TileModel.RIVER_STRAIGHT_DIRT,
                     TileModel.DECLINE_DIRT,
                     TileModel.INCLINE_DIRT,
                     TileModel.RIVER_CORNER_DIRT,
                     TileModel.CLIFF_TOP_CORNER_DIRT,
                     TileModel.CLIFF_TOP_WATERFALL_DIRT,
                     TileModel.CLIFF_TOP_DIRT,
                     TileModel.RIVER_END_DIRT,
                     TileModel.RIVER_TJUNCTION_DIRT,
                     TileModel.RIVER_JUNCTION_DIRT]

        # Load map models
        os.chdir('../res/naturepack_extended/Models/')  # to prevent file path problems
        self.models = {}
        self.models_mono = {}
        for model_id in model_ids:
            model_path = "naturePack_{0:03d}.obj".format(model_id.value)
            self.models[model_id] = OBJ(model_path, swapyz=True)
            self.models_mono[model_id] = OBJ(model_path, swapyz=True, monocolor=True)
        os.chdir('../../../src')  # change back

        # Load entity models
        os.chdir('../res/rabbit')
        self.rabbit_models = []
        self.rabbit_frame_time = 300
        self.rabbit_frame = 0
        self.rabbit_frame_counter = 0
        model1 = OBJ("rabbit_0.obj", swapyz=True)
        for i in range(17):
            self.rabbit_models.append(model1)
            # self.rabbit_models.append(OBJ("rabbit_{0}.obj".format(str(i)), swapyz=True))
        os.chdir('../../src')

        # Prepare string textures
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" \
                "0123456789 !@#$%^&*()-=_+\|[]{};:'\",.<>/?`~"
        self.char_texs = {}
        for char in chars:
            self.char_texs[char] = self.charTexFromBMP(char)

        # Initialise OpenGL settings
        glLightfv(GL_LIGHT0, GL_POSITION, (-40, 200, 100, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)  # most obj files expect to be smooth-shaded

    def setView(self, viewport):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        width, height = viewport
        gluPerspective(90.0, width / float(height), 1, 100.0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)

        self.SplashTex = self.TexFromPNG("res/background.png")

    def TexFromPNG(self, filename):
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

    def charTexFromBMP(self, char):
        # Draw coordinates
        os.chdir('gui/bmpfont')
        from src.gui.bmpfont.bmpfont import BmpFont
        bmpfont = BmpFont()
        img = pygame.image.load('font.png')
        img_data = numpy.array(list(img.get_view().raw), numpy.uint8)

        width, height = 8, 16
        img_x, img_y = bmpfont.chartable[char]
        img_char = numpy.array([])
        for y in range(img_y, img_y + height):
            img_char = numpy.append(img_char,
                                    img_data[4 * (y * 8 * width + img_x):4 * (y * 8 * width + img_x + width)])

        texture = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 8, 16, 0, GL_RGBA, GL_UNSIGNED_BYTE,
                     img_char)
        os.chdir('../..')
        return texture

    def loadBackgroundTexture(self):
        glBindTexture(GL_TEXTURE_2D, self.SplashTex)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        # Varray = numpy.array([[0, 0], [0, 256], [224, 256], [224, 0]], numpy.uint16)
        # glVertexPointer(2, GL_SHORT, 0, Varray)
        # indices = [0, 1, 2, 3]
        # glDrawElements(GL_QUADS, 1, GL_UNSIGNED_SHORT, indices)

    def renderBackground(self):
        self.loadBackgroundTexture()

        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glEnable(GL_TEXTURE_2D)

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

        glDisable(GL_TEXTURE_2D)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)

    def renderMap(self, map, select=None):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.renderBackground()

        glEnable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)

        glLoadIdentity()

        # Calculate the camera position using the angles and zoom
        self.setCamera()

        self.renderTiles(map, select=select)

        self.renderGrid(*map.getSize())

    def renderEntities(self, entities):

        glEnable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)
        glColor(1.0, 1.0, 1.0)

        glLoadIdentity()
        self.setCamera()

        scale = 0.1
        dev_x, dev_y = 1.5, -1  # deviation
        for entity in entities:
            glTranslate(3 * entity.i, -3 * entity.j, 0.25)
            glTranslate(dev_x, dev_y, 0)
            glRotate(-entity.orient + 180, 0, 0, 1)

            glScale(scale, scale, scale)
            glCallList(self.rabbit_models[self.rabbit_frame].gl_list)
            self.rabbit_frame_counter += 30
            if self.rabbit_frame_counter > self.rabbit_frame_time:
                self.rabbit_frame = (self.rabbit_frame + 1) % 17
                self.rabbit_frame_counter = 0
            glScale(1 / scale, 1 / scale, 1 / scale)

            glRotate(entity.orient - 180, 0, 0, 1)
            glTranslate(-dev_x, -dev_y, 0)
            glTranslate(-3 * entity.i, 3 * entity.j, -0.25)

    def renderGrid(self, width, height):
        glLoadIdentity()
        self.setCamera()
        glLineWidth(1.0)
        glColor3f(1.0, 0.0, 0.0)
        x_dev = 2.3
        y_dev = 2.3

        # Draw grid
        glBegin(GL_LINES)
        for i in range(1, width):
            glVertex3f(3 * i, -y_dev, 0.32)
            glVertex3f(3 * i, -3 * height + y_dev, 0.32)
        for j in range(1, height):
            glVertex3f(x_dev, -3 * j, 0.32)
            glVertex3f(3 * width - x_dev, -3 * j, 0.32)
        glEnd()

        # Draw coordinates of grid
        glColor(1.0, 1.0, 1.0, 1.0)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        offset = 0.1
        char_width = 0.6
        char_height = 0.6
        for i in range(0, width):
            for j in range(0, height):
                string = '{0},{1}'.format(i, j)
                for k, c in enumerate(string):
                    glBindTexture(GL_TEXTURE_2D, self.char_texs[c])
                    glBegin(GL_QUADS)
                    glTexCoord2f(0, 0)
                    glVertex3f(3 * i + offset + char_width * k, -3 * j - offset, 0.32)
                    glTexCoord2f(1, 0)
                    glVertex3f(3 * i + offset + char_width + char_width * k, -3 * j - offset, 0.32)
                    glTexCoord2f(1, 1)
                    glVertex3f(3 * i + offset + char_width + char_width * k, -3 * j - offset - char_height, 0.32)
                    glTexCoord2f(0, 1)
                    glVertex3f(3 * i + offset + char_width * k, -3 * j - offset - char_height, 0.32)
                    glEnd()

        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)

    def setCamera(self):
        center_x = 5.5 * 3
        center_y = -4 * 3
        center_z = 0
        to_rad = (math.pi / 180)
        cam_x = center_x + self.zpos * math.cos(self.phi * to_rad) * math.sin(self.theta * to_rad)
        cam_y = center_y + self.zpos * math.sin(self.phi * to_rad) * math.sin(self.theta * to_rad)
        eye_z = center_z + self.zpos * math.cos(self.theta * to_rad)
        # Set the camera position and look at point
        gluLookAt(cam_x, cam_y, eye_z,  # camera position
                  center_x, center_y, center_z,  # look at point
                  0.0, 0.0, 1.0)  # up vector

    def renderTiles(self, map, select=None, pick=False):
        if pick:
            glDisable(GL_TEXTURE_2D)
            glDisable(GL_LIGHTING)
            self.colorToTile = {}

        width, height = map.getSize()
        for j in range(height):
            for i in range(width):
                # Determine tile model id and orientation
                model_id, orientation = self.getTile(map, i, j)
                glRotate(-orientation, 0, 0, 1)
                if orientation == 90 or orientation == 180:
                    glTranslate(0, 3, 0)
                if orientation == 180 or orientation == 270:
                    glTranslate(-3, 0, 0)

                if model_id == TileModel.CLIFF_TOP_DIRT \
                        or model_id == TileModel.CLIFF_TOP_WATERFALL_DIRT:  # the cliff edges have a deviation
                    glTranslate(2.5, 0, 0)

                if model_id == TileModel.CLIFF_TOP_CORNER_DIRT:  # the cliff corners have a deviation as well
                    glTranslate(2.08, 0, 0)

                if pick:
                    color = (int(i / width * 255), int(j / height * 255), 255)
                    glColor3ub(*color)
                    self.colorToTile[color] = (i, j)
                    glCallList(self.models_mono[model_id].gl_list)  # draw mono tile model
                elif select == (i, j):
                    glColorMask(True, False, False, False)  # draw only red
                    glCallList(self.models[model_id].gl_list)  # draw tile model
                    glColorMask(True, True, True, True)
                else:
                    glCallList(self.models[model_id].gl_list)  # draw tile model

                if model_id == TileModel.CLIFF_TOP_DIRT \
                        or model_id == TileModel.CLIFF_TOP_WATERFALL_DIRT:  # the edges have a deviation
                    glTranslate(-2.5, 0, 0)

                if model_id == TileModel.CLIFF_TOP_CORNER_DIRT:  # the cliff corners have a deviation as well
                    glTranslate(-2.08, 0, 0)

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

    def getTile(self, map, i, j):
        tiles = map.getTiles()
        width, height = map.getSize()
        model_id, orientation = 0, 0
        if ((i == 0 or i == width - 1) and not (j == 0 or j == height - 1)) \
                or ((j == 0 or j == height - 1) and not (i == 0 or i == width - 1)):
            if tiles[i][j] == Tile.LAND.value:
                model_id = TileModel.CLIFF_TOP_DIRT
            elif tiles[i][j] == Tile.WATER.value:
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
            if tiles[i][j] == Tile.LAND.value:
                model_id = TileModel.FLAT_DIRT
            elif tiles[i][j] == Tile.WATER.value:
                neighbours = n, e, s, w = tiles[i][j - 1], tiles[i + 1][j], tiles[i][j + 1], tiles[i - 1][j]
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

    def getTileCoords(self, map, x, y):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.setCamera()
        self.renderTiles(map, pick=True)
        color = tuple(glReadPixels(x, 600 - y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE))
        if color in list(self.colorToTile.keys()):
            return self.colorToTile[color]
        else:
            return None

    def setOrbit(self, phi, theta):
        self.phi, self.theta = phi, theta

    def setZoom(self, zpos):
        self.zpos = zpos
