#! /usr/bin/python
import math
import numpy as np

###############################################################################
def geocentrique2geographique(x, y, z):

    V = [0.0, 0.0, 0.0]
    f = 1/298.257222101
    a = 6378137.0

    e2 = 1 - (1 - f) * (1 - f)

    P = math.sqrt(x * x + y * y)
    R = math.sqrt(x * x + y * y + z * z)

    V[0] = 2 * math.atan(y / (x + P))

    m = math.atan(z / P * (1 - f + e2 * a / R))
    num = z * (1 - f) + e2 * a * math.pow(math.sin(m), 3)

    deno = (1 - f) * (P - e2 * a * math.pow(math.cos(m), 3))

    V[1] = math.atan(num / deno)
    V[2] = P * math.cos(V[1]) + z * math.sin(V[1])-a * math.sqrt(1-e2 * math.sin(V[1]) * math.sin(V[1]))

    return V

###############################################################################
def geocentrique2local(x, y, z):
    geoc = [[x],[y],[z]]
    geog = geocentrique2geographique(x, y, z)
    long = geog[0]
    lat = geog[1]
    rotation_matrix = [
        [ -math.sin(long), math.cos(long), 0 ],
        [ -math.cos(long) * math.sin(lat), -math.sin(long) * math.sin(lat), math.cos(lat) ],
        [ math.cos(long)*math.cos(lat), math.sin(long)*math.cos(lat), math.sin(lat) ]
    ]
    return np.dot(rotation_matrix, geoc)
