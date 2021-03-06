import pygame
from OpenGL.GL import *


def MTL(filename):
    contents = {}
    mtl = None
    for line in open(filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue
        if values[0] == 'newmtl':
            mtl = contents[values[1]] = {}
        elif mtl is None:
            raise ValueError("mtl file doesn't start with newmtl stmt")
        elif values[0] == 'map_Kd':
            # load the texture referred to by this declaration
            mtl[values[0]] = values[1]
            surf = pygame.image.load(mtl['map_Kd'])
            image = pygame.image.tostring(surf, 'RGBA', 1)
            ix, iy = surf.get_rect().size
            texid = mtl['texture_Kd'] = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texid)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                            GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                            GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,
                         GL_UNSIGNED_BYTE, image)
        elif values[0] == 'map_Bump':
            pass  # do nothing
        elif values[0] == 'map_d':
            pass  # do nothing
        else:
            mtl[values[0]] = list(map(float, values[1:]))
    return contents


class OBJ:
    def __init__(self, filename, swapyz=False, monocolor=False):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        min_x, max_x = 100, -100
        min_y, max_y = 100, -100
        min_z, max_z = 100, -100

        material = None
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = map(float, values[1:4])
                v_list = list(v)
                if swapyz:
                    v_list = v_list[0], v_list[2], v_list[1]
                self.vertices.append(v_list)
                # Determine min/max
                min_x = min(v_list[0], min_x)
                max_x = max(v_list[0], max_x)
                min_y = min(v_list[1], min_y)
                max_y = max(v_list[1], max_y)
                min_z = min(v_list[2], min_z)
                max_z = max(v_list[2], max_z)
            elif values[0] == 'vn':
                v = map(float, values[1:4])
                v_list = list(v)
                if swapyz:
                    v_list = v_list[0], v_list[2], v_list[1]
                self.normals.append(v_list)
            elif values[0] == 'vt':
                texs = list(map(float, values[1:3]))  # added list
                self.texcoords.append(texs)
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                self.mtl = MTL(values[1])
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))

        # Determine model size
        self.dx = max_x - min_x
        self.dy = max_y - min_y
        self.dz = max_z - min_z

        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        if not monocolor:
            glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        for face in self.faces:
            vertices, normals, texture_coords, material = face

            if not monocolor:
                mtl = self.mtl[material]
                if 'texture_Kd' in mtl:
                    # use diffuse texmap
                    glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
                else:
                    # just use diffuse colour
                    colours = mtl['Kd']
                    glColor3f(colours[0], colours[1], colours[2])

            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        if not monocolor:
            glBindTexture(GL_TEXTURE_2D, 0)
            glDisable(GL_TEXTURE_2D)
        glEndList()
