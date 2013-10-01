#!/usr/local/bin/python
# coding: utf-8
"""
    >>> poly = Polygon([1, 1], [4, 4], [7, 1], [4, -4])
    >>> poly.vertices # doctest: +ELLIPSIS
    [[1, 1], ..., [4, -4]]

    >>> poly = Polygon((1, 1), (4, 4), (7, 1), (4, -4))
    >>> poly.vertices # doctest: +ELLIPSIS
    [(1, 1), ..., (4, -4)]

    >>> poly._Polygon__min_max_slice()
    >>> poly.right_slice
    [(4, 4), (7, 1), (4, -4)]
    >>> poly.left_slice
    [(4, -4), (1, 1), (4, 4)]

    >>> poly._Polygon__test_in_line((2, 3), (1, 3), (3, 3))
    True
    >>> poly._Polygon__test_in_line((4, 3), (1, 3), (3, 3))
    False

    >>> poly._Polygon__test_side((1, 3), (2, 4), (2, 2))  # vertical aligned
    'left'
    >>> poly._Polygon__test_side((3, 3), (2, 4), (2, 2))  # vertical aligned
    'right'
    >>> poly._Polygon__test_side((0, 3), (2, 4), (3, 2))  # vertical not aligned
    'left'
    >>> poly._Polygon__test_side((5, 3), (2, 4), (3, 2))  # vertical not aligned
    'right'
    >>> poly._Polygon__test_side((0, 3), (-1, 1), (-2, 4))  # vertical not aligned
    'right'
    >>> poly._Polygon__test_side((-5, 3), (-1, 1), (-2, 4))  # vertical not aligned
    'left'

    >>> right_poly = [(1, 10), (2, 8), (3, 6), (4, 4), (2, 0)]
    >>> poly._Polygon__right_test((1, 5), right_poly)
    True
    >>> poly._Polygon__right_test((20, 5), right_poly)
    False

    >>> left_poly = [(-2, 0), (-4, 4), (-3, 6), (-1, 8), (1, 10)]
    >>> poly._Polygon__left_test((1, 5), left_poly)
    True
    >>> poly._Polygon__left_test((-10, 5), left_poly)
    False

    >>> poly = Polygon((-2, 5), (2, 5), (4, 2), (3, -1), (2, -4), (-1, -5), (-3, -2), (-3, 2))
    >>> poly.is_on_polygon((6, 0))  # outside the polygon on the side
    False
    >>> poly. is_on_polygon((0, 6))  # outside the polygon on top
    False
    >>> poly.is_on_polygon((1, -2)) # inside the polygon
    True
    >>> poly.is_on_polygon((0, 5))  # on the horizontal line
    True
    >>> poly.is_on_polygon((-3, 0))  # on the vertical line
    True
    >>> poly.is_on_polygon((3, 3.5))  # on the diagonal line
    True
    >>> poly.is_on_polygon((-2, -2))  # inside the polygon aligned with one vertex
    True
"""

from __future__ import division

class Polygon:
    """Class Polygon"""
    def __init__(self, *vert):
        self.vertices = list(vert)

    def __min_max_slice(self):
        """Divide the polygon into left and right according
        with the vertices of the highest and lowest y"""

        min_v = 0
        max_v = 0
        for i in range(len(self.vertices)):
            if self.vertices[i][1] > self.vertices[max_v][1]:
                max_v = i
            elif self.vertices[i][1] < self.vertices[min_v][1]:
                min_v = i

        if max_v <= min_v:
            self.right_slice = self.vertices[max_v:min_v+1]
            self.left_slice = self.vertices[min_v:] + self.vertices[:max_v+1]
        else:
            self.left_slice = self.vertices[min_v:max_v+1]
            self.right_slice = self.vertices[max_v:] + self.vertices[:min_v+1]

    def __test_in_line(self, p, q1, q2):
        """Test to treat the case when the point is on the superior or inferior 
        rim of the polygon"""

        if q1[0] <= p[0] and p[0] <= q2[0]:
            self.__in_line = True
            return True
        return False

    def __test_side(self, p, q1, q2):
        """Test whether this point of the left or right side of the line"""

        if q1[0] == q2[0]:
            x = q1[0]
        else:
            m = (q1[1] - q2[1]) / (q1[0] - q2[0])
            x = ((p[1] - q1[1]) / m) + q1[0]
        
        if p[0] < x:
            return 'left'
        elif p[0] > x:
            return 'right'
        else:
            return 'inline'

    def __right_test(self, point, r_verts):
        """Test for the right side"""

        num_verts = len(r_verts)
        mid = num_verts // 2

        if num_verts == 2:
            if r_verts[0][1] == r_verts[-1][1]:
                return self.__test_in_line(point, r_verts[0], r_verts[-1])

            test = self.__test_side(point, r_verts[0], r_verts[-1])
            if test == 'left' or test == 'inline':
                return True
            else:
                return False

        if point[1] <= r_verts[0][1] and point[1] > r_verts[mid][1]:
            return self.__right_test(point, r_verts[:mid+1])
        elif point[1] <= r_verts[mid][1] and point[1] >= r_verts[-1][1]:
            return self.__right_test(point, r_verts[mid:])
        else:
            return False

    def __left_test(self, point, r_verts):
        """Test for the left side"""

        num_verts = len(r_verts)
        mid = num_verts // 2

        if num_verts == 2:
            if r_verts[0][1] == r_verts[-1][1]:
                return self.__test_in_line(point, r_verts[0], r_verts[-1])

            test = self.__test_side(point, r_verts[0], r_verts[-1])
            if test == 'right' or test == 'inline':
                return True
            else:
                return False

        if point[1] >= r_verts[0][1] and point[1] <= r_verts[mid][1]:
            return self.__left_test(point, r_verts[:mid+1])
        elif point[1] > r_verts[mid][1] and point[1] <= r_verts[-1][1]:
            return self.__left_test(point, r_verts[mid:])
        else:
            return False

    def is_on_polygon(self, point):
        """Find out if the point is in the polygon"""

        self.__in_line = False
        self.__min_max_slice()

        if (self.__right_test(point, self.right_slice) and 
            self.__left_test(point, self.left_slice)):
            return True

        if self.__in_line:
            return True

        return False
