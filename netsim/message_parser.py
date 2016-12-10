#!/usr/bin/env python3
#
# code adapted to Python from
# http://stackoverflow.com/questions/19723641/find-intersecting-point-of-three-circles-programmatically

from math import sqrt


EPSILON = 0.000001
triangulate_output_format = 'INTERSECTION Circle1 AND Circle2 AND Circle3: ({}, {})'
BAD_RESULT = None


def triangulate(x0, y0, r0, x1, y1, r1, x2, y2, r2):
    # dx and dy are the vertical and horizontal distances between the circle centers.
    dx = x1 - x0
    dy = y1 - y0

    # Determine the straight-line distance between the centers.
    d = sqrt((dy*dy) + (dx*dx))

    # Check for solvability.
    if d > (r0 + r1):
        return BAD_RESULT

    if d < abs(r0 - r1):
        return BAD_RESULT

    a = ((r0*r0) - (r1*r1) + (d*d)) / (2.0 * d)

    point2_x = x0 + (dx * a/d)
    point2_y = y0 + (dy * a/d)

    h = sqrt((r0*r0) - (a*a))
    rx = -dy * (h/d)
    ry = dx * (h/d)

    intersection_point1_x = point2_x + rx
    intersection_point2_x = point2_x - rx
    intersection_point1_y = point2_y + ry
    intersection_point2_y = point2_y - ry

    dx = intersection_point1_x - x2
    dy = intersection_point1_y - y2
    d1 = sqrt((dy*dy) + (dx*dx))

    dx = intersection_point2_x - x2
    dy = intersection_point2_y - y2
    d2 = sqrt((dy*dy) + (dx*dx))

    if abs(d1 - r2) < EPSILON:
        return (intersection_point1_x, intersection_point1_y)
    elif abs(d2 - r2) < EPSILON:
        return (intersection_point2_x, intersection_point2_y)
    else:
        return BAD_RESULT


triangulate(1, 1, 1.41421356237, 0, 1, 1, 1, 0, 1)
