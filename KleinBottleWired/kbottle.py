from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import sys
import math
from trackball import Trackball


def on_draw():
    global translate

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    trackball.push()
    if is_wheel_down:
        glTranslate(translate[0], -1 * translate[1], 0)
    draw_axis()
    draw_bottle(2.000001, 0.09)
    trackball.pop()

    glutSwapBuffers()


def draw_bottle(a, step):
    glBegin(GL_LINE_STRIP)
    for u in np.arange(0, 2 * math.pi, step):
        for v in np.arange(0, 2 * math.pi, step):
            glColor3f(0.5, 0.5, 0.5)
            coordinates = calc_bottle_coordinates(u, v, a)
            glVertex3f(coordinates[0], coordinates[1], coordinates[2])
    glEnd()

    glBegin(GL_LINE_STRIP)
    for u in np.arange(0, 2 * math.pi, step):
        for v in np.arange(0, 2 * math.pi, step):
            glColor3f(0.5, 0.5, 0.5)
            coordinates = calc_bottle_coordinates(v, u, a)
            glVertex3f(coordinates[0], coordinates[1], coordinates[2])
    glEnd()


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
    glutPostRedisplay()


glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowPosition(50, 50)
glutInitWindowSize(800, 600)
glutCreateWindow(b"Some User Interaction")

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
