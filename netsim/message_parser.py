#code adapted to Python from http://stackoverflow.com/questions/19723641/find-intersecting-point-of-three-circles-programmatically

EPSILON = 0.000001
import math

def triangulate(x0, y0, r0, x1, y1, r1, x2, y2, r2):

	# dx and dy are the vertical and horizontal distances between the circle centers.
	dx = x1 - x0
	dy = y1 - y0

	# Determine the straight-line distance between the centers.
	d = math.sqrt((dy*dy) + (dx*dx))

	# Check for solvability.
	if (d > (r0 + r1)):
		return false

	if (d < abs(r0 - r1)):
		return false

	a = ((r0*r0) - (r1*r1) + (d*d)) / (2.0 * d)

	point2_x = x0 + (dx * a/d)
	point2_y = y0 + (dy * a/d)

	h = math.sqrt((r0*r0) - (a*a))
	rx = -dy * (h/d)
	ry = dx * (h/d)

	intersectionPoint1_x = point2_x + rx
	intersectionPoint2_x = point2_x - rx
	intersectionPoint1_y = point2_y + ry
	intersectionPoint2_y = point2_y - ry

	dx = intersectionPoint1_x - x2
	dy = intersectionPoint1_y - y2
	d1 = math.sqrt((dy*dy) + (dx*dx))

	dx = intersectionPoint2_x - x2
	dy = intersectionPoint2_y - y2
	d2 = math.sqrt((dy*dy) + (dx*dx))

	if(abs(d1 - r2) < EPSILON):
		print "INTERSECTION Circle1 AND Circle2 AND Circle3: (" + str(intersectionPoint1_x) + "," + str(intersectionPoint1_y) + ")"
	elif(abs(d2 - r2) < EPSILON):
		print "INTERSECTION Circle1 AND Circle2 AND Circle3: (" + str(intersectionPoint2_x) + "," + str(intersectionPoint2_y) + ")"
	else:
		print "INTERSECTION Circle1 AND Circle2 AND Circle3: NONE"


triangulate(1,1,1.41421356237,0,1,1,1,0,1)