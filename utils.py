# coding=utf-8
"""Utility functions package"""
from point import Point
from OpenGL.GL import *
import numpy as np
import math


# CONSTS
NEAR = 10
FAR = 20000
D_EYE = 35
CONVERGENCE = 2000
FOV = 45


def draw_parallelepiped(point: Point, width: float, height: float, length: float):
        """Draw parallelepiped from the point in the center of the bottom surface"""
        half_width = width / 2
        half_height = height / 2
        p1 = Point(point.x - half_width, point.y, point.z - half_height)
        p2 = Point(point.x + half_width, point.y, point.z - half_height)
        p3 = Point(point.x + half_width, point.y, point.z + half_height)
        p4 = Point(point.x - half_width, point.y, point.z + half_height)
        p5 = Point(point.x - half_width, point.y + length, point.z - half_height)
        p6 = Point(point.x + half_width, point.y + length, point.z - half_height)
        p7 = Point(point.x + half_width, point.y + length, point.z + half_height)
        p8 = Point(point.x - half_width, point.y + length, point.z + half_height)

        # Bottom
        draw_line(p1, p2)
        draw_line(p2, p3)
        draw_line(p3, p4)
        draw_line(p4, p1)
        # # Top
        draw_line(p5, p6)
        draw_line(p6, p7)
        draw_line(p7, p8)
        draw_line(p8, p5)
        # # Sides
        draw_line(p1, p5)
        draw_line(p2, p6)
        draw_line(p3, p7)
        draw_line(p4, p8)


def draw_line(p1: Point, p2: Point):
    """Draw line"""
    # glColor3f(0.2, 0.2, 0.8)
    glLineWidth(5)
    glBegin(GL_LINES)
    glVertex3f(p1.x * 0.2, p1.y * 0.2, p1.z * 0.2)
    glVertex3f(p2.x * 0.2, p2.y * 0.2, p2.z * 0.2)
    glEnd()


def dotproduct(v1, v2):
    return sum((a*b) for a, b in zip(v1, v2))


def length(v):
    return math.sqrt(dotproduct(v, v))


def vectors_angle(vector1, vector2):
    return math.acos(dotproduct(vector1, vector2) / (length(vector1) * length(vector2)))


def normalize_vector(vector):
    """Normalize vector"""
    return vector / np.linalg.norm(vector)


def calc_frustum_vars(aspect_rat: float):
    top = NEAR * math.tan(FOV / 2)
    bottom = - top
    a = aspect_rat * math.tan(FOV / 2) * CONVERGENCE
    b = a - D_EYE / 2
    c = a + D_EYE / 2

    return top, bottom, a, b, c


def apply_left_frustum(aspect_rat: float):
    top, bottom, a, b, c = calc_frustum_vars(aspect_rat)
    left = -b * NEAR / CONVERGENCE
    right = c * NEAR / CONVERGENCE

    # glMatrixMode(GL_PROJECTION)
    # glLoadIdentity()
    glFrustum(left, right, bottom, top, NEAR, FAR)
    # glMatrixMode(GL_MODELVIEW)
    # glLoadIdentity()
    glTranslatef(D_EYE / 2, 0, 0)


def apply_right_frustum(aspect_rat: float):
    top, bottom, a, b, c = calc_frustum_vars(aspect_rat)
    left = -c * NEAR / CONVERGENCE
    right = b * NEAR / CONVERGENCE

    # glMatrixMode(GL_PROJECTION)
    # glLoadIdentity()
    glFrustum(left, right, bottom, top, NEAR, FAR)
    # glMatrixMode(GL_MODELVIEW)
    # glLoadIdentity()
    glTranslatef(-D_EYE / 2, 0, 0)
