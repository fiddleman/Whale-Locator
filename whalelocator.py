from math import sin, cos, asin, acos, atan2, sqrt, pi
from haversine import haversine, inverse_haversine, inverse_haversine_vector, Unit, Direction
from numpy import arange

directory                   = '/Users/mbi/Documents/Programming/Whale Locator/'
filenameBase                = 'Test Run - '
#===================================================================================#
#                                   CONSTANTS                                       #
#===================================================================================#
Rmiles                      = 3960                  # Radius of the earth in miles
feetInMile                  = 5280                  # Number of feet in a mile
#===================================================================================#
#                            UNIT CONVERSIONS FACTORS                               #
#===================================================================================#
milesToNauticalMiles        = 0.868976
milesToMeters               = 1609.34
milesToFeet                 = 5280

nauticalMilesToMiles        = 1.15078
metersToMiles               = 0.000621371
feetToMiles                 = 0.00018939388080000001

degreesToRadians            = pi / 180
radiansToDegrees            = 180 / pi
#===================================================================================#

#===================================================================================#
#                                   PARAMETERS                                      #
#===================================================================================#
obsLatDeg                  = 33.74475                                               #
obsLongDeg                 = -118.4107                                              #
targetBearingDeg           = 290                                                    #
hMiles                     = 143.5 / feetInMile                                     #
#===================================================================================#

#
# Reticle to Mills Table
#
MILS            = 0
METERS          = 1
KILOMETERS      = 2
FEET            = 3
STATUE_MILES    = 4
NAUTICAL_MILES  = 5

retToMils = {
#   RETICLE MILS    METERS      KILOMETERS  FEET            STATUTE MILES   NAUTICAL MILES
    0:      (0,     23599.00,   23.60,      77424.54,       14.66,          12.74),
    0.1:    (0.5,   14021.00,   14.02,      46000.66,       8.71,           7.57),
    0.2:    (1,     11390.00,   11.39,      37368.77,       7.08,           6.15),
    0.4:    (2,     8598.00,    8.60,       28208.66,       5.34,           4.64),
    0.6:    (3,     7010.00,    7.01,       22998.69,       4.36,           3.79),
    0.8:    (4,     5950.00,    5.95,       19521.00,       3.70,           3.21),
    1:      (5,     5183.00,    5.18,       17004.59,       3.22,           2.80),
    1.2:    (6,     4598.00,    4.60,       15085.30,       2.86,           2.48),
    1.4:    (7,     4135.00,    4.14,       13566.27,       2.57,           2.23),
    1.6:    (8,     3759.00,    3.76,       12332.68,       2.34,           2.03),
    1.8:    (9,     3448.00,    3.45,       11312.34,       2.14,           1.86),
    2:      (10,    3184.00,    3.18,       10446.19,       1.98,           1.72),
    2.4:    (12,    2764.00,    2.76,       9068.24,        1.72,           1.49),
    2.6:    (13,    2593.00,    2.59,       8507.22,        1.61,           1.40),
    3:      (15,    2309.00,    2.31,       7575.46,        1.43,           1.25),
    3.4:    (17,    2081.00,    2.08,       6827.43,        1.29,           1.12),
    4:      (20,    1813.00,    1.81,       5948.16,        1.13,           0.98),
    4.6:    (23,    1607.00,    1.61,       5272.31,        1.00,           0.87),
    5:      (25,    1493.00,    1.49,       4898.29,        0.93,           0.81),
    6:      (30,    1269.00,    1.27,       4163.39,        0.79,           0.69),
    7:      (35,    1104.00,    1.10,       3622.05,        0.69,           0.60),
    8:      (40,    977.00,     0.98,       3205.38,        0.61,           0.53),
    9:      (45,    876.00,     0.88,       2874.02,        0.54,           0.47),
    10:     (50,    794.00,     0.79,       2604.99,        0.49,           0.43),
    11:     (55,    726.00,     0.73,       2381.89,        0.45,           0.39),
    12:     (60,    669.00,     0.67,       2194.88,        0.42,           0.36),
    13:     (65,    620.00,     0.62,       2034.12,        0.39,           0.33),
    14:     (70,    577.00,     0.58,       1893.04,        0.36,           0.31),
    15:     (75,    540.00,     0.54,       1771.65,        0.34,           0.29),
    16:     (80,    508.00,     0.51,       1666.67,        0.32,           0.27),
    17:     (85,    479.00,     0.48,       1571.52,        0.30,           0.26),
    18:     (90,    453.00,     0.45,       1486.22,        0.28,           0.24),
    19:     (95,    430.00,     0.43,       1410.76,        0.27,           0.23),
    20:     (100,   409.00,     0.41,       1341.86,        0.25,           0.22)
}

def binarySearch(needle, haystack):
    first = 0
    itemList = list(haystack)
    last = len(itemList) - 1
    while first <= last:
        mid = (first + last) // 2
        if itemList[mid] == needle:
            return needle
        elif needle < itemList[mid]:
            last = mid - 1
        else:
            first = mid + 1

    low = itemList[mid - 1]
    high = itemList[mid]
    if abs(needle - high) <= abs(needle - low):
        return high
    else:
        return low
    
def reticleToDistance(reticle):
    return retToMils[binarySearch(round(reticle, 1), retToMils.keys())]

def dumpLatLongTable(fileName, bearingInDegrees, path):
    if path:
        f = open(f"{path}{fileName}{bearingInDegrees}.csv", "w")
    else:
        f = open(f"{fileName}{bearingInDegrees}.csv", "w")
    census = (33.74475, -118.4107)
    print()
    print("Lattitude, Longitude")
    f.write("Lattitude, Longitude\n")
    for reticle in arange(0, 20.1, 0.1):
        d = reticleToDistance(reticle)
        target = inverse_haversine(census, d[STATUE_MILES], bearingInDegrees * degreesToRadians)
        print(f"{target[0]},{target[1]}")
        f.write(f"{target[0]},{target[1]}\n")
    f.close()

#
# Main Executable
#
if __name__ == "__main__":
    for degrees in range(0, 360, 15):
        dumpLatLongTable(filenameBase, degrees, directory)

