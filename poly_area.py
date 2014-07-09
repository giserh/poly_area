###############################################################################
#
# ::: POLY_AREA :::
#
# AUTHOR
#
#    Yoshua Wakeham
#        email: yoshwakeham@gmail.com
#        www  : github.com/yoshw
#        tweet: @yoshw
#
# DATE CREATED
#
#    9 July 2014
#
# NOTES
#
#    Poly_area is a simple script for calculating the surface area
#    of a polygon in the Cartesian (x-y) plane, when the polygon
#    is specified by an arbitrary sequence of vertices contained in
#    a CSV file.
#
#    The algorithm traverses the vertices in the given order, and
#    uses a line integral/summation method based on Green's Theorem
#    to compute the surface area.
#
#    (See https://en.wikipedia.org/wiki/Green%27s_theorem for more.)
#
#    Poly_area may be run as a command-line script, or imported as
#    a standard Python module.
#
#    This code is designed to be run with Python 2.7x. It was
#    written and tested on a MacBook Pro running OSX 10.9 Mavericks.
#
# COPYING
#
#    This program is free software: you can redistribute it
#    and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either
#    version 3 of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import csv, sys


### FUNCTIONS #################################################################

def readpoints(fname):
    """
    readpoints(fname) -> list of x-y co-ords stored as 2-tuples

    Reads the contents of the input file, assumed to be in CSV format,
    and provided the contents are well-formed, converts the CSV data
    into a list of 2-tuples representing Cartesian co-ordinates.
    """
    try:
        file = open(fname,"r")
    except IOError, e:
        print(e)
        exit()
    reader = csv.reader(file)
    points = []
    for row in reader:
        if len(row)!=2:
            print("Error: input row must have exactly 2 entries:{}".format(row))
            file.close()
            exit()
        try:
            points.append((float(row[0]),float(row[1])))
        except ValueError:
            print("Error: numeric conversion of input failed for file: {}."\
                    .format(fname))
            file.close()
            exit()
    file.close()
    return points


def getarea(points):
    """
    getarea(list of floating pt 2-tuples) -> surface area (float)

    Calculates the surface area of a polygon in
    the x-y plane, using a simplified form of Green's Theorem.
    Assumes that the input list is a sequence of vertices,
    stored as floating point 2-tuples. The algorithm traverses
    these vertices in a clockwise fashion.
    """
    area = 0.0
    for i in range(len(points)-1):
        area += seg_integral(points[i],points[i+1])
    # calculate final segment, closing the polygon
    area += seg_integral(points[-1],points[0])
    return area


def seg_integral(p1,p2):
    """
    seg_integral((float, float), (float, float)) -> integral value (float)

    Calculate a line integral for the line segment with
    endpoints p1 and p2. This is a simplified form of the
    integral of the field (-y,x)/2 along the line. When the
    segment integrals are summed over a closed, piecewise
    continuous boundary, we obtain the surface area of the
    enclosed region.
    """
    try:
        (x1,y1) = p1
        (x2,y2) = p2
    except (TypeError, ValueError):
        print("Error: invalid input to function seg_integral()")
        exit()
    xavg = (x1 + x2) / 2
    yavg = (y1 + y2) / 2
    dx = x2 - x1
    dy = y2 - y1
    return (xavg * dy - yavg * dx) / 2


### MAIN ROUTINE #########################################################

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc != 2:
        print("poly_area: usage: python poly_area.py fname")
        exit()

    fname = sys.argv[1]
    print("Reading input file ...")
    points = readpoints(fname)
    print("Input file read.")
    print("Calculating area ...")
    area = getarea(points)
    print("Calculation complete.")

    print("The surface area of the polygon specified in {}".format(fname))
    print("is {} magical, dimensionless units.".format(area))
