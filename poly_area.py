###############################################################################
#
# ::: POLY AREA :::
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
#    xx July 2014
#
# NOTES
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

import csv
import sys


### FUNCTIONS #################################################################

def readpoints(fname):
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
            exit()
        try:
            points.append((float(row[0]),float(row[1])))
        except ValueError:
            print("Error: numeric conversion of input failed for file: {}."\
                    .format(fname))
            exit()
    return points


def getarea(points):
    """
    Calculates the surface area of a polygon in
    the x-y plane, using a reduced form of Green's Theorem.
    Assumes that the polygon is specified by a sequence
    of vertices, in order of counterclockwise traversal.
    """
    area = 0.0
    for i in range(len(points)-1):
        area += segmentint(points[i],points[i+1])
    area += segmentint(points[-1],points[0])
    return area


def segmentint(p1,p2):
    """
    Calculate a line integral for a line segment which,
    when summed over a closed piecewise continuous boundary,
    gives the surface area of the enclosed region.
    """
    try:
        (x1,y1) = p1
        (x2,y2) = p2
    except (TypeError, ValueError):
        print("Error: invalid input to function segmentint()")
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
