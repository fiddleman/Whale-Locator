from math import sin, cos, asin, acos, atan2, sqrt, pi
from bisect import bisect_left

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

def reticleToMils(reticle):
    return reticle

def dumpLatLongTable():
    print(f"reticle  LookupMil        Dist1         Dist2")
    for reticle in (0.001, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 15, 17, 20, 23, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100):
        mils = reticleToMils(reticle)
        print(CalculateNewPositoin(obsLatDeg, obsLongDeg, hMiles, targetBearingDeg, mils))

        # print(f"{reticle:7}  {mils:9}   {milsToDistance1(mils, hMiles):10}    {milsToDistance2(mils, hMiles):10}")
    print(f"reticle  LookupMil        Dist1         Dist2")


#
# Main Executable
#
if __name__ == "__main__":
    dumpLatLongTable()


