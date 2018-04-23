from OpenGL.GL import *
from point import Point
from vector import Vector
from utils import draw_parallelepiped, vectors_angle


class Phalanx:
    def __init__(self, width: float, height: float, length: float):
        self.width = width
        self.height = height
        self.length = length


class Finger:
    def __init__(self,
                 position: Point,
                 r: Vector,
                 angle: int,
                 phalanx1: Phalanx,
                 phalanx2: Phalanx,
                 phalanx3: Phalanx,
                 is_regular: bool = True):
        self.position = position
        self.r = r
        self.is_regular = is_regular
        self.__angle = angle
        self.phalanx1 = phalanx1
        self.phalanx2 = phalanx2
        self.phalanx3 = phalanx3

    def bend(self, step):
        self.__angle += step

    def unbend(self, step):
        self.__angle -= step

    def draw(self):
        """Draw finger"""
        phalanx1 = self.phalanx1
        phalanx2 = self.phalanx2
        phalanx3 = self.phalanx3
        rotate_axis = vectors_angle(self.r.get_list(), (1, 0, 0))
        rotate_axis = 360 if not self.is_regular else rotate_axis

        glPushMatrix()

        glTranslate(self.position.x * 0.2,
                    self.position.y * 0.2,
                    self.position.z * 0.2)

        glRotatef(rotate_axis, 0, 0, 1)
        glRotatef(self.__angle, 1, 0, 0)

        glPushMatrix()

        draw_parallelepiped(Point(0, 0, 0),
                            phalanx1.width,
                            phalanx1.height,
                            phalanx1.length)

        glPopMatrix()

        glRotatef(self.__angle, 1, 0, 0)
        glTranslate(0, phalanx1.length * 0.2, 0)

        glPushMatrix()

        draw_parallelepiped(Point(0, 0, 0),
                            phalanx2.width,
                            phalanx2.height,
                            phalanx2.length)

        glPopMatrix()

        glRotatef(self.__angle, 1, 0, 0)
        glTranslate(0, phalanx2.length * 0.2, 0)
        glPushMatrix()

        draw_parallelepiped(Point(0, 0, 0),
                            phalanx3.width,
                            phalanx3.height,
                            phalanx3.length)

        glPopMatrix()

        glPopMatrix()


class Palm:
    def __init__(self):
        self.color = (0.5, 0.5, 0.5)
        self.palm_base_point = Point(-2, 2, 0)
        # L Width Height
        self.palm_size = (14, 2, 14)

        self.fingers = [
            # Finger 1 (little)
            Finger(Point(-8, 17, 0),
                   Vector(2, 0.3, 0),
                   355,
                   Phalanx(1.3, 1.8, 4.47),
                   Phalanx(1, 1.3, 4.12),
                   Phalanx(0.7, 0.9, 3.16)),
            # Finger 2
            Finger(Point(-4, 17, 0),
                   Vector(2, 0.1, 0),
                   355,
                   Phalanx(1.3, 1.8, 6.2),
                   Phalanx(1, 1.3, 4.12),
                   Phalanx(0.7, 0.9, 3.32)),
            # Finger 3
            Finger(Point(0, 17, 0),
                   Vector(2.5, 0, 0),
                   355,
                   Phalanx(1.3, 1.8, 7),
                   Phalanx(1, 1.3, 5),
                   Phalanx(0.7, 0.9, 3.32)),
            # Finger 4
            Finger(Point(4, 17, 0),
                   Vector(2, -0.1, 0),
                   355,
                   Phalanx(1.3, 1.8, 6.7),
                   Phalanx(1, 1.3, 4.12),
                   Phalanx(0.7, 0.9, 3.32)),
            # Finger 5 (big)
            Finger(Point(6, 8, 0),
                   Vector(0.5, 0.5, 0),
                   355,
                   Phalanx(1.3, 1.8, 5),
                   Phalanx(1, 1.3, 4.24),
                   Phalanx(0.4, 0.9, 2.54),
                   False),
        ]

    def draw(self):
        """Draw palm"""
        palm_p = self.palm_base_point
        palm_s = self.palm_size

        self.fingers[0].draw()
        self.fingers[1].draw()
        self.fingers[2].draw()
        self.fingers[3].draw()
        self.fingers[4].draw()

        draw_parallelepiped(palm_p,
                            palm_s[0],
                            palm_s[1],
                            palm_s[2])

    def bend_finger(self, index: int, step: int):
        self.fingers[index].bend(step)

    def unbend_finger(self, index: int, step: int):
        self.fingers[index].unbend(step)
