from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import sys
import math
import copy
from trackball import Trackball
import pygame, OpenGL
from pygame.locals import *


def on_draw():
    global translate

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    trackball.push()
    if is_wheel_down:
        glTranslate(translate[0], -1 * translate[1], 0)
    draw_axis()
    view_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
    viewer_pos = view_matrix[3]
    viewer_pos = [viewer_pos[0], viewer_pos[1], viewer_pos[2]]
    draw_bottle(2.000001, 0.21, viewer_pos)
    trackball.pop()

    glutSwapBuffers()


def draw_bottle(a, step, viewer_pos):
    big_lines = []
    for u in np.arange(0, 2 * math.pi, step):
        lines = []
        for v in np.arange(0, 2 * math.pi, step):
            line = []
            line.append(calc_bottle_coordinates(u, v, a) + [u / 2 * math.pi, v / 2 * math.pi])
            line.append(calc_bottle_coordinates(u, v + step, a) + [u / 2 * math.pi, v + step / 2 * math.pi])
            lines.append(copy.deepcopy(line))

        big_lines.append(copy.deepcopy(lines))

    glBegin(GL_TRIANGLES)

    for index, big_line in enumerate(big_lines[:-1]):
        for inner_index, line in enumerate(big_line[:-1]):
            next_adjacent_line = big_lines[index + 1][inner_index]

            if index < len(big_lines) - 2 and inner_index < len(big_line):
                next_next_adjacent_line_upper = big_lines[index + 2][inner_index + 1]
            else:
                next_next_adjacent_line_upper = None

            if index < len(big_lines) and inner_index < len(big_line):
                next_adjacent_line_upper = big_lines[index + 1][inner_index + 1]
            else:
                next_adjacent_line_upper = None

            if index > 0:
                prev_adjacent_line = big_lines[index - 1][inner_index]

            else:
                prev_adjacent_line = None

            if inner_index > 0:
                bottom_line = big_lines[index][inner_index - 1]
            else:
                bottom_line = None

            if index < len(big_line) and inner_index > 0:
                next_bottom_line = big_lines[index + 1][inner_index - 1]
            else:
                next_bottom_line = None

            if inner_index < len(big_line):
                upper_line = big_lines[index][inner_index + 1]
            else:
                upper_line = None

            if index > 0 and inner_index < len(big_line):
                prev_adjacent_line_upper = big_lines[index - 1][inner_index + 1]
            else:
                prev_adjacent_line_upper = None

            if index < len(big_lines) - 2 and inner_index > 0:
                next_next_adjacent_line_bottom = big_lines[index + 2][inner_index -1]
            else:
                next_next_adjacent_line_bottom = None

            if index < len(big_lines) - 2:
                next_next_adjacent_line = big_lines[index + 2][inner_index]
            else:
                next_next_adjacent_line = None

            # Light position
            light_pos = [5, 5, 5]
            ambient = 0.4
            shininess = 0.2
            d_light = [0.2, 0.4, 0.8]
            s_light = [0.2, 0.4, 0.8]
            material_color = [0.255, 0.412, 0.882]


            # Triangle1

            # Point1
            n = calc_vertex_normal(prev_adjacent_line,
                                   line,
                                   next_adjacent_line,
                                   next_bottom_line,
                                   bottom_line)

            vertex = [line[0][0], line[0][1], line[0][2]]
            tex_coord = [line[0][3], line[0][4]]
            l = calc_vector(light_pos, vertex)

            v = calc_vector(viewer_pos, vertex)

            color = calc_vector_color(material_color, n, l, v, ambient, d_light, s_light, shininess)

            glColor3f(color[0], color[1], color[2])
            glTexCoord2f(tex_coord[0], tex_coord[1])
            glVertex3f(vertex[0], vertex[1], vertex[2])

            # Point2
            n = calc_vertex_normal(prev_adjacent_line_upper,
                                   [line[1], upper_line[0]],
                                   next_adjacent_line_upper,
                                   next_adjacent_line,
                                   line)

            vertex = [line[1][0], line[1][1], line[1][2]]
            tex_coord = [line[1][3], line[1][4]]
            l = calc_vector(light_pos, vertex)

            v = calc_vector(viewer_pos, vertex)

            color = calc_vector_color(material_color, n, l, v, ambient, d_light, s_light, shininess)

            glColor3f(color[0], color[1], color[2])
            glTexCoord2f(tex_coord[0], tex_coord[1])
            glVertex3f(vertex[0], vertex[1], vertex[2])

            # Point3
            n = calc_vertex_normal(line,
                                   next_adjacent_line,
                                   next_next_adjacent_line,
                                   next_next_adjacent_line_bottom,
                                   next_bottom_line)

            vertex = [next_adjacent_line[0][0], next_adjacent_line[0][1], next_adjacent_line[0][2]]
            tex_coord = [next_adjacent_line[0][3], next_adjacent_line[0][4]]
            l = calc_vector(light_pos, vertex)

            v = calc_vector(viewer_pos, vertex)

            color = calc_vector_color(material_color, n, l, v, ambient, d_light, s_light, shininess)

            glColor3f(color[0], color[1], color[2])
            glTexCoord2f(tex_coord[0], tex_coord[1])
            glVertex3f(vertex[0], vertex[1], vertex[2])

            # Triangle2

            #Point2
            n = calc_vertex_normal(prev_adjacent_line_upper,
                                   [line[1], upper_line[0]],
                                   next_adjacent_line_upper,
                                   next_adjacent_line,
                                   line)

            vertex = [line[1][0], line[1][1], line[1][2]]
            tex_coord = [line[1][3], line[1][4]]
            l = calc_vector(light_pos, vertex)

            v = calc_vector(viewer_pos, vertex)

            color = calc_vector_color(material_color, n, l, v, ambient, d_light, s_light, shininess)

            glColor3f(color[0], color[1], color[2])
            glTexCoord2f(tex_coord[0], tex_coord[1])
            glVertex3f(vertex[0], vertex[1], vertex[2])

            #Point3
            n = calc_vertex_normal(line,
                                   next_adjacent_line,
                                   next_next_adjacent_line,
                                   next_next_adjacent_line_bottom,
                                   next_bottom_line)

            vertex = [next_adjacent_line[0][0], next_adjacent_line[0][1], next_adjacent_line[0][2]]
            tex_coord = [next_adjacent_line[0][3], next_adjacent_line[0][4]]
            l = calc_vector(light_pos, vertex)

            v = calc_vector(viewer_pos, vertex)

            color = calc_vector_color(material_color, n, l, v, ambient, d_light, s_light, shininess)

            glColor3f(color[0], color[1], color[2])
            glTexCoord2f(tex_coord[0], tex_coord[1])
            glVertex3f(vertex[0], vertex[1], vertex[2])

            #Point4
            n = calc_vertex_normal(upper_line,
                                   next_adjacent_line_upper,
                                   next_next_adjacent_line_upper,
                                   next_next_adjacent_line,
                                   next_adjacent_line)

            vertex = [next_adjacent_line[1][0], next_adjacent_line[1][1], next_adjacent_line[1][2]]
            tex_coord = [next_adjacent_line[1][3], next_adjacent_line[1][4]]
            l = calc_vector(light_pos, vertex)

            v = calc_vector(viewer_pos, vertex)

            color = calc_vector_color(material_color, n, l, v, ambient, d_light, s_light, shininess)

            glColor3f(color[0], color[1], color[2])
            glTexCoord2f(tex_coord[0], tex_coord[1])
            glVertex3f(vertex[0], vertex[1], vertex[2])

    glEnd()


def calc_vector(v1, v2):
    return np.array([v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]])


def calc_vector_color(material, n, l, v, ambient, d_light, s_light, shininess):
    r = calc_vertex_color_component(material[0], n, l, v, ambient, d_light[0], s_light[0], shininess)
    g = calc_vertex_color_component(material[1], n, l, v, ambient, d_light[1], s_light[1], shininess)
    b = calc_vertex_color_component(material[2], n, l, v, ambient, d_light[2], s_light[2], shininess)
    return [r, g, b]


def calc_vertex_color_component(material, n, l, v, ambient, d_light, s_light, shininess):
    l = normalize_vector(l)
    v = normalize_vector(v)
    r = l - 2 * np.cross(np.cross(n, l), n)
    i_amb = ambient
    i_dir = max(np.dot(l, n), 0) * d_light * material
    i_spec = math.pow(max(np.dot(r, v), 0), shininess) * material * s_light
    return i_amb + i_dir + i_spec


def calc_vertex_normal(v12, v03, v4, v5, v6):
    n_list = []
    v0 = v03[0]
    v3 = v03[1]
    v0v3 = calc_vector(v0, v3)

    if v4 is not None:
        v4 = v4[0]
        v0v4 = calc_vector(v0, v4)
        n_list.append(np.cross(v0v3, v0v4))

    if v12 is not None:
        v1 = v12[0]
        v2 = v12[1]
        v0v1 = calc_vector(v0, v1)
        v0v2 = calc_vector(v0, v2)
        n_list.append(np.cross(v0v1, v0v2))
        n_list.append(np.cross(v0v2, v0v3))

    if v5 is not None:
        v5 = v5[0]
        v0v5 = calc_vector(v0, v5)
        n_list.append(np.cross(v0v4, v0v5))

    if v6 is not None:
        v6 = v6[0]
        v0v6 = calc_vector(v0, v6)

    if v6 is not None and v5 is not None:
        n_list.append(np.cross(v0v5, v0v6))

    if v6 is not None and v12 is not None:
        n_list.append(np.cross(v0v6, v0v1))

    sum_n = np.array([0, 0, 0])
    for n in n_list:
        sum_n = sum_n + n

        sum_n = np.asarray(sum_n, dtype=np.float)

    return sum_n / np.linalg.norm(sum_n)


def normalize_vector(vec):
    return vec / np.linalg.norm(vec)


def calc_bottle_coordinates(u, v, a):
    x = (a + math.cos(u / 2) * math.sin(v) - math.sin(u / 2) * math.sin(2 * v)) * math.cos(u)
    y = (a + math.cos(u / 2) * math.sin(v) - math.sin(u / 2) * math.sin(2 * v)) * math.sin(u)
    z = math.sin(u / 2) * math.sin(v) + math.cos(u / 2) * math.sin(2 * v)
    return [x, y, z]


def draw_axis():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)

    glVertex3f(0, 0, 0)
    glVertex3f(10, 0, 0)

    glColor3f(0.0, 1.0, 0.0)

    glVertex3f(0, 0, 0)
    glVertex3f(0, 10, 0)

    glColor3f(0.0, 0.0, 1.0)

    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 10)

    glEnd()


def on_wheel(button, direction, x, y):
    if direction > 0:
        trackball.zoom_to(x, y, 0, +10)
    else:
        trackball.zoom_to(x, y, 0, -10)
    glutPostRedisplay()


def on_mouse(button, state, x, y):
    global is_right_button_down
    global is_wheel_down
    global prevPos
    global translate

    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            prevPos[0] = x
            prevPos[1] = y
            is_right_button_down = True
        elif state == GLUT_UP:
            is_right_button_down = False

    if button == GLUT_WHEEL:
        if state == GLUT_DOWN:
            prevPos[0] = x
            prevPos[1] = y
            is_wheel_down = True
        elif state == GLUT_UP:
            is_wheel_down = False


def on_motion(cur_x, cur_y):
    global prevPos
    global trackball
    global translate

    if is_right_button_down:
        x = prevPos[0]
        y = prevPos[1]
        dx = cur_x - prevPos[0]
        dy = cur_y - prevPos[1]

        trackball.drag_to(0.2 * x, 0.2 * y, 0.2 * dx, 0.2 * dy)
        glutPostRedisplay()

    if is_wheel_down:
        dx = cur_x - prevPos[0]
        dy = cur_y - prevPos[1]
        translate = [dx, dy]
        glutPostRedisplay()


def on_reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)


def on_keyboard(code, x, y):
    glutPostRedisplay()


def on_special(code, x, y):
    if code == GLUT_KEY_UP:
        trackball.zoom_to(x, y, 0, +100)
    elif code == GLUT_KEY_DOWN:
        trackball.zoom_to(x, y, 0, -100)
    glutPostRedisplay()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowPosition(50, 50)
glutInitWindowSize(800, 600)
glutCreateWindow(b"Some User Interaction")
glShadeModel(GL_SMOOTH)

img512 = pygame.image.load('./textures/texture_512.png')
img256 = pygame.image.load('./textures/texture_256.png')
img128 = pygame.image.load('./textures/texture_128.png')
img64 = pygame.image.load('./textures/texture_64.png')
img32 = pygame.image.load('./textures/texture_32.png')
img16 = pygame.image.load('./textures/texture_16.png')
img8 = pygame.image.load('./textures/texture_8.png')
img4 = pygame.image.load('./textures/texture_4.png')
img2 = pygame.image.load('./textures/texture_2.png')
img1 = pygame.image.load('./textures/texture_1.png')
textureData512 = pygame.image.tostring(img512, 'RGB', 1)
textureData256 = pygame.image.tostring(img256, 'RGB', 1)
textureData128 = pygame.image.tostring(img128, 'RGB', 1)
textureData64 = pygame.image.tostring(img64, 'RGB', 1)
textureData32 = pygame.image.tostring(img32, 'RGB', 1)
textureData16 = pygame.image.tostring(img16, 'RGB', 1)
textureData8 = pygame.image.tostring(img8, 'RGB', 1)
textureData4 = pygame.image.tostring(img4, 'RGB', 1)
textureData2 = pygame.image.tostring(img2, 'RGB', 1)
textureData1 = pygame.image.tostring(img1, 'RGB', 1)


im = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, im)

# glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 512, 512, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData512)
glTexImage2D(GL_TEXTURE_2D, 1, GL_RGB, 256, 256, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData256)
glTexImage2D(GL_TEXTURE_2D, 2, GL_RGB, 128, 128, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData128)
glTexImage2D(GL_TEXTURE_2D, 3, GL_RGB, 64, 64, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData64)
glTexImage2D(GL_TEXTURE_2D, 4, GL_RGB, 32, 32, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData32)
glTexImage2D(GL_TEXTURE_2D, 5, GL_RGB, 16, 16, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData16)
glTexImage2D(GL_TEXTURE_2D, 6, GL_RGB, 8, 8, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData8)
glTexImage2D(GL_TEXTURE_2D, 7, GL_RGB, 4, 4, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData4)
glTexImage2D(GL_TEXTURE_2D, 8, GL_RGB, 2, 2, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData2)
glTexImage2D(GL_TEXTURE_2D, 9, GL_RGB, 1, 1, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData1)
glEnable(GL_TEXTURE_2D)

GLUT_WHEEL = 1

prevPos = [0, 0]
translate = [0, 0]
is_right_button_down = False
is_wheel_down = False
trackball = Trackball(45, 135, 5, 4)

glutMouseFunc(on_mouse)
glutMouseWheelFunc(on_wheel)
glutReshapeFunc(on_reshape)
glutDisplayFunc(on_draw)
glutMotionFunc(on_motion)
glutKeyboardFunc(on_keyboard)
glutSpecialFunc(on_special)
glutMainLoop()
