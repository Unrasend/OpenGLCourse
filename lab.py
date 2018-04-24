from OpenGL.GL import *
from OpenGL.GLUT import *
import sys
from trackball import Trackball
from palm import Palm
from utils import NEAR, D_EYE, apply_left_frustum, apply_right_frustum


def on_draw():
    """Handle on draw event"""
    global translate
    global palm
    global aspect_ratio

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    trackball.push()
    if is_wheel_down:
        glTranslate(translate[0], -1 * translate[1], 0)
    draw_axis()

    glColor3f(0.8, 0.2, 0.8)

    glColorMask(True, False, False, False)
    apply_left_frustum(aspect_ratio)

    palm.draw()

    glClear(GL_DEPTH_BUFFER_BIT)

    apply_right_frustum(aspect_ratio)
    glColorMask(False, True, True, False)

    palm.draw()

    glColorMask(True, True, True, False)

    trackball.pop()

    glutSwapBuffers()


def draw_axis():
    """Draw axis"""
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
    """Handle on wheel"""
    if direction > 0:
        trackball.zoom_to(x, y, 0, +10)
    else:
        trackball.zoom_to(x, y, 0, -10)
    glutPostRedisplay()


def on_mouse(button, state, x, y):
    """Handle mouse"""
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
    """Handle Motion"""
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
    """Handle reshape"""
    global aspect_ratio
    aspect_ratio = width / height
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)


def on_keyboard(code, x, y):
    """Handle keyboard"""
    glutPostRedisplay()


def on_special(code, x, y):
    """Handle special buttons"""
    step = 10

    if code == GLUT_KEY_UP:
        trackball.zoom_to(x, y, 0, +10)
    if code == GLUT_KEY_DOWN:
        trackball.zoom_to(x, y, 0, -10)

    if code == GLUT_KEY_F1:
        palm.bend_finger(0, step)
    if code == GLUT_KEY_F2:
        palm.unbend_finger(0, step)
    if code == GLUT_KEY_F3:
        palm.bend_finger(1, step)
    if code == GLUT_KEY_F4:
        palm.unbend_finger(1, step)
    if code == GLUT_KEY_F5:
        palm.bend_finger(2, step)
    if code == GLUT_KEY_F6:
        palm.unbend_finger(2, step)
    if code == GLUT_KEY_F7:
        palm.bend_finger(3, step)
    if code == GLUT_KEY_F8:
        palm.unbend_finger(3, step)
    if code == GLUT_KEY_F9:
        palm.bend_finger(4, step)

    glutPostRedisplay()


# Main entry
palm = Palm()
glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowPosition(50, 50)
glutInitWindowSize(800, 600)
glutCreateWindow("COME GET SOME STEREO IMAGE")

GLUT_WHEEL = 1

prevPos = [0, 0]
translate = [0, 0]
is_right_button_down = False
is_wheel_down = False
aspect_ratio = 800 / 600
trackball = Trackball(45, 135, 5, 4)

glutMouseFunc(on_mouse)
glutMouseWheelFunc(on_wheel)
glutReshapeFunc(on_reshape)
glutDisplayFunc(on_draw)
glutMotionFunc(on_motion)
glutKeyboardFunc(on_keyboard)
glutSpecialFunc(on_special)
glutMainLoop()
