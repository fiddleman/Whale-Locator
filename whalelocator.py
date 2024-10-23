from math import sin, cos, asin, acos, atan2, sqrt, pi
from numpy import arange

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

#=======================================================================================#
#                                   PARAMETERS                                          #
#=======================================================================================#
obsLatDeg                  = 33.74475                                                   #
obsLongDeg                 = -118.4107                                                  #
targetBearingDeg           = 270                                                        #
hMiles                     = 143.5 / feetInMile                                         #
#=======================================================================================#

#
# Reticle to Mills Table
#
retToMils = {
    0:0.001,
    0.1:0.5,
    0.2:1,
    0.4:2,
    0.6:3,
    0.8:4,
    1:5,
    1.2:6,
    1.4:7,
    1.6:8,
    1.8:9,
    2:10,
    2.4:12,
    2.6:13,
    3:15,
    3.4:17,
    4:20,
    4.6:23,
    5:25,
    6:30,
    7:35,
    8:40,
    9:45,
    10:50,
    11:55,
    12:60,
    13:65,
    14:70,
    15:75,
    16:80,
    17:85,
    18:90,
    19:95,
    20:100
}

#
# Here is the formula to find the second point, when first point, bearing and distance is known:
#
def CalculateNewPositoin(latDeg, lonDeg, h, bearingDeg, mils):
    # Convert lattitude, longitude and heading to target lattitude/`longitude
    latRad       = latDeg * degreesToRadians
    lonRad       = lonDeg * degreesToRadians
    bearingRad   = bearingDeg * degreesToRadians

    angDistMiles = milsToDistance1(mils, h)

    newLatRad  = asin(sin(latRad) * 
                            cos(angDistMiles) + cos(latRad) * 
                            sin(angDistMiles) * 
                            cos(bearingRad))

    newLonRad = lonRad + \
                            atan2(sin(bearingRad) * 
                            sin(angDistMiles) * 
                            cos(latRad),
                            cos(angDistMiles) - sin(latRad) * 
                            sin(newLatRad))
    
    newLatDeg = newLatRad * radiansToDegrees
    newLonDeg = newLonRad * radiansToDegrees
    return [round(newLatDeg, 4), round(newLonDeg, 4)]

#
# Calculate range from mils
#
def milsToDistance1(mils, h):
    return round((Rmiles * acos(Rmiles/(Rmiles + h))/mils), 4)

def milsToDistance2(mils, h):
    return round(sqrt(((Rmiles + h) ** 2) - (Rmiles ** 2))/mils, 4)

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
    
def reticleToMils(reticle):
    return retToMils[binarySearch(round(reticle, 1), retToMils.keys())]

def dumpLatLongTable():
    for reticle in arange(0, 20.1, 0.1):
        mils = reticleToMils(reticle)
        print(mils, CalculateNewPositoin(obsLatDeg, obsLongDeg, hMiles, targetBearingDeg, mils))


#
# Main Executable
#
if __name__ == "__main__":
    dumpLatLongTable()


