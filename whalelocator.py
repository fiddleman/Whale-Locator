#!/opt/homebrew/anaconda3/bin/python

from math import sin, cos, asin, acos, atan2, sqrt, pi
from haversine import haversine, inverse_haversine, inverse_haversine_vector, Unit, Direction
from numpy import arange

#===================================================================================#
#                                    OUTPUT FILES                                   #
#===================================================================================#
directory                   = '/Users/mbi/Documents/Programming/Whale Locator/'
filenameBase                = 'Test Run - '

#===================================================================================#
#                        UNIT CONVERSIONS FACTOR CONSTANTS                          #
#===================================================================================#
feetToMiles                 = 0.000189394
feetToMeters                = 0.30480030800000379454
feetToKilometers            = 0.0003048000097536
feetToNauticalMiles         = 0.000164579

milesToFeet                 = 5280
milesToMeters               = 1609.34
milesToKilometers           = 1.60934
milesToNauticalMiles        = 0.868976

metersToFeet                = 3.28084
metersToMiles               = 0.000621371
metersToKilometers          = 0.001
metersToNauticalMiles       = 0.000539957349081371537

kilometersToFeet            = 3280.84
kilometersToMiles           = 0.621371
kilometersToMeters          = 1000
kilometersToNauticalMiles   = 0.53995734908137149599

nauticalMilesToFeet         = 6076.11568
nauticalMilesToMiles        = 1.15078
nauticalMilesToMeters       = 1852.000059264
nauticalMilesToKilometers   = 1.852

degreesToRadians            = pi / 180
radiansToDegrees            = 180 / pi


#===================================================================================#
#                    CLASSES FOR LOCATION, BEARING AND DISTANCE                     #
#===================================================================================#
class Bearing:
        def __init__(self, bearing: float, unit:Unit = None):
             self.bearing = bearing
             self.unit    = unit

        def __str__(self):
             return f"Bearing: {self.bearing} {self.unit.value}"
        
        def degrees(self):
            if self.unit == Unit.DEGREES:
                return self.bearing
            else:
                return self.bearing * radiansToDegrees
        def radians(self):
            if (self.unit == Unit.RADIANS):
                return self.bearing
            else:
                return self.bearing * degreesToRadians

        def convertTo(self, unit: Unit):
            if unit == self.unit:
                return self
            match unit:
                case Unit.DEGREES:
                    return Bearing(self.degrees(), unit)
                case Unit.RADIANS:
                    return Bearing(self.radians(), unit)
                case _:
                    raise Exception(f"Invalid Bearing unit specified: {unit}")
                 

            
            
class Distance:
        def __init__(self, distance: float, unit: Unit = Unit.MILES):
            self.distance = distance
            self.unit     = unit

        def __str__(self):
             return f"Distance: {self.distance} {self.unit.value}"

        def feet(self):
            match self.unit:
                case Unit.FEET:
                    return self.distance
                case Unit.MILES:
                    return self.distance * milesToFeet
                case Unit.METERS:
                    return self.distance * metersToFeet
                case Unit.KILOMETERS:
                    return self.distance * kilometersToFeet
                case Unit.NAUTICAL_MILES:
                    return self.distance * nauticalMilesToFeet
                case _:
                    raise Exception(f"Invalid Distance unit specified: {unit}")

        def miles(self):
            match self.unit:
                case Unit.FEET:
                    return self.distance * feetToMiles
                case Unit.MILES:
                    return self
                case Unit.METERS:
                    return self.distance * metersToMiles
                case Unit.KILOMETERS:
                    return self.distance * kilometersToMiles
                case Unit.NAUTICAL_MILES:
                    return self.distance * nauticalMilesToMiles
                case _:
                    raise Exception(f"Invalid Distance unit specified: {unit}")

        def meters(self):
            match self.unit:
                case Unit.FEET:
                    return self.distance * feetToMeters
                case Unit.MILES:
                    return self.distance * milesToMeters
                case Unit.METERS:
                    return self
                case Unit.KILOMETERS:
                    return self.distance * kilometersToMeters
                case Unit.NAUTICAL_MILES:
                    return self.distance * nauticalMilesToMeters
                case _:
                    raise Exception(f"Invalid Distance unit specified: {unit}")

        def kilometers(self):
            match self.unit:
                case Unit.FEET:
                    return self.distance * feetToKilometers
                case Unit.MILES:
                    return self.distance * milesToKilometers
                case Unit.METERS:
                    return self.distance * metersToKilometers
                case Unit.KILOMETERS:
                    return self
                case Unit.NAUTICAL_MILES:
                    return self.distance * nauticalMilesToKilometers
                case _:
                    raise Exception(f"Invalid Distance unit specified: {unit}")

        def nauticalMiles(self):
            match self.unit:
                case Unit.FEET:
                    return self.distance * feetToNauticalMiles
                case Unit.MILES:
                    return self.distance * milesToNauticalMiles
                case Unit.METERS:
                    return self.distance * metersToNauticalMiles
                case Unit.KILOMETERS:
                    return self.distance * kilometersToNauticalMiles
                case Unit.NAUTICAL_MILES:
                    return self
                case _:
                    raise Exception(f"Invalid Distance unit specified: {unit}")

        def convertTo(self, unit: Unit):
            if unit == self.unit:
                return self
            match unit:
                case Unit.FEET:
                    return Distance(self.feet(), unit)
                case Unit.MILES:
                    return Distance(self.miles(), unit)
                case Unit.METERS:
                    return Distance(self.meters(), unit)
                case Unit.KILOMETERS:
                    return Distance(self.kilometers(), unit)
                case Unit.NAUTICAL_MILES:
                    return Distance(self.nauticalMiles(), unit)
                case _:
                    raise Exception(f"Invalid Distance unit specified: {unit}")

class Height:
        def __init__(self, height: float, unit = Unit.MILES):
            self.height = height
            self.unit   = unit

        def __str__(self):
             return f"Height: {self.height} {self.unit.value}"

        def feet(self):
            match self.unit:
                case Unit.FEET:
                    return self
                case Unit.MILES:
                    return self.height * milesToFeet
                case Unit.METERS:
                    return self.height * metersToFeet
                case Unit.KILOMETERS:
                    return self.height * kilometersToFeet
                case Unit.NAUTICAL_MILES:
                    return self.height * nauticalMilesToFeet
                case _:
                    raise Exception(f"Invalid Height unit specified: {unit}")
                
        def miles(self):
            match self.unit:
                case Unit.FEET:
                    return self.height * feetToMiles
                case Unit.MILES:
                    return self
                case Unit.METERS:
                    return self.height * metersToMiles
                case Unit.KILOMETERS:
                    return self.height * kilometersToMiles
                case Unit.NAUTICAL_MILES:
                    return self.height * nauticalMilesToMiles
                case _:
                    raise Exception(f"Invalid Height unit specified: {unit}")


        def meters(self):
            match self.unit:
                case Unit.FEET:
                    return self.height * feetToMeters
                case Unit.MILES:
                    return self.height * milesToMeters, Unit.METERS
                    return self
                case Unit.KILOMETERS:
                    return self.height * kilometersToMeters
                case Unit.NAUTICAL_MILES:
                    return self.height * nauticalMilesToMeters
                case _:
                    raise Exception(f"Invalid Height unit specified: {unit}")

        def kilometers(self):
            match self.unit:
                case Unit.FEET:
                    return self.height * feetToKilometers
                case Unit.MILES:
                    return self.height * milesToKilometers
                case Unit.METERS:
                    return self.height * metersToKilometers
                case Unit.KILOMETERS:
                    return self
                case Unit.NAUTICAL_MILES:
                    return self.height * nauticalMilesToKilometers
                case _:
                    raise Exception(f"Invalid Height unit specified: {unit}")

        def nauticalMiles(self):
            match self.unit:
                case Unit.FEET:
                    return self.height * feetToNauticalMiles
                case Unit.MILES:
                    return self.height * milesToNauticalMiles
                case Unit.METERS:
                    return self.height * metersToNauticalMiles
                case Unit.KILOMETERS:
                    return self.height * kilometersToNauticalMiles
                case Unit.NAUTICAL_MILES:
                    return self
                case _:
                    raise Exception(f"Invalid Height unit specified: {unit}")

        def convertTo(self, unit: Unit):
            if unit == self.unit:
                return self
            match unit:
                case Unit.FEET:
                    return Height(self.feet(), unit)
                case Unit.MILES:
                    return Height(self.miles(), unit)
                case Unit.METERS:
                    return Height(self.meters(), unit)
                case Unit.KILOMETERS:
                    return Height(self.kilometers(), unit)
                case Unit.NAUTICAL_MILES:
                    return Height(self.nauticalMiles(), unit)
                case _:
                    raise Exception(f"Invalid Height unit specified: {unit}")


class Coordinate:
        def __init__(self, coord: float, unit: Unit = Unit.RADIANS):
            self.coord  = coord
            self.unit   = unit

        def __str__(self):
            return f"Coordinate: {self.coord} {self.unit.value}"
        
        def radians(self):
            match self.unit:
                case Unit.DEGREES:
                    return self.coord * degreesToRadians
                
                case Unit.RADIANS:
                    return self.coord
            
        def degrees(self):
            match self.unit:
                case Unit.DEGREES:
                    return self.coord
                
                case Unit.RADIANS:
                    return self.coord * radiansToDegrees

        def convertTo(self, unit: Unit):
            if unit == self.unit:
                return self
            match unit:
                case Unit.DEGREES:
                    return Coordinate(self.degrees(), unit)
                case Unit.RADIANS:
                    return Coordinate(self.radians(), unit)
                case _:
                    raise Exception(f"Invalid Coordinate unit specified: {unit}")
                    
            
class Location:
        def __init__(self, lat: float, lon: float, h: Height, cUnit: Unit = Unit.DEGREES):
            self.lat   = Coordinate(lat, cUnit)
            self.lon   = Coordinate(lon, cUnit)
            self.h     = h

        def __str__(self):
            return f"Location: {self.lat}, {self.lon}, {self.h}"
        
        def latRad(self):
            return self.lat.radians()
        
        def latDeg(self):
            return self.lat.degrees()
        
        def lonRad(self):
            return self.lon.radians()
        
        def lonDeg(self):
            return self.lon.degrees()
        
        def latLonRad(self):
            return self.latRad(), self.lonRad()
        
        def latLonDeg(self):
            return self.latDeg(), self.lonDeg()
        
        def height(self):
            return self.h

        def convertTo(self, unit: Unit):
            match unit:
                case Unit.DEGREES:
                    return Location(self.lat.degrees(),self.lon.degrees(), self.h, unit)
                case Unit.RADIANS:
                    return Location(self.lat.radians(),self.lon.radians(), self.h, unit)
                case _:
                    raise Exception(f"Invalid Location unit specified: {unit}")


#===================================================================================#
#                                   CONSTANTS                                       #
#===================================================================================#
R                           = Distance(3960, Unit.MILES)                            # Radius of the earth

#===================================================================================#
#                                   PARAMETERS                                      #
#===================================================================================#
census                          = Location(33.74475, -118.4107, Height(143.5, Unit.FEET))
#===================================================================================#

#
# Reticle to Mills Table
#
MILS            = 0
DISTANCE        = 1

retToMils = {
#   RETICLE MILS    METERS
    0:      (0,     Distance(23599.00, Unit.METERS)),
    0.1:    (0.5,   Distance(14021.00, Unit.METERS)),
    0.2:    (1,     Distance(11390.00, Unit.METERS)),
    0.4:    (2,     Distance( 8598.00, Unit.METERS)),
    0.6:    (3,     Distance( 7010.00, Unit.METERS)),
    0.8:    (4,     Distance( 5950.00, Unit.METERS)),
    1:      (5,     Distance( 5183.00, Unit.METERS)),
    1.2:    (6,     Distance( 4598.00, Unit.METERS)),
    1.4:    (7,     Distance( 4135.00, Unit.METERS)),
    1.6:    (8,     Distance( 3759.00, Unit.METERS)),
    1.8:    (9,     Distance( 3448.00, Unit.METERS)),
    2:      (10,    Distance( 3184.00, Unit.METERS)),
    2.4:    (12,    Distance( 2764.00, Unit.METERS)),
    2.6:    (13,    Distance( 2593.00, Unit.METERS)),
    3:      (15,    Distance( 2309.00, Unit.METERS)),
    3.4:    (17,    Distance( 2081.00, Unit.METERS)),
    4:      (20,    Distance( 1813.00, Unit.METERS)),
    4.6:    (23,    Distance( 1607.00, Unit.METERS)),
    5:      (25,    Distance( 1493.00, Unit.METERS)),
    6:      (30,    Distance( 1269.00, Unit.METERS)),
    7:      (35,    Distance( 1104.00, Unit.METERS)),
    8:      (40,    Distance(  977.00, Unit.METERS)),
    9:      (45,    Distance(  876.00, Unit.METERS)),
    10:     (50,    Distance(  794.00, Unit.METERS)),
    11:     (55,    Distance(  726.00, Unit.METERS)),
    12:     (60,    Distance(  669.00, Unit.METERS)),
    13:     (65,    Distance(  620.00, Unit.METERS)),
    14:     (70,    Distance(  577.00, Unit.METERS)),
    15:     (75,    Distance(  540.00, Unit.METERS)),
    16:     (80,    Distance(  508.00, Unit.METERS)),
    17:     (85,    Distance(  479.00, Unit.METERS)),
    18:     (90,    Distance(  453.00, Unit.METERS)),
    19:     (95,    Distance(  430.00, Unit.METERS)),
    20:     (100,   Distance(  409.00, Unit.METERS))
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

def dumpLatLongTable(observer: Location, bearing: Bearing):
    # print("Lattitude, Longitude")
    for reticle in arange(0, 20.1, 0.1): 
        d = reticleToDistance(reticle)
        target = inverse_haversine(census.latLonRad(), d[DISTANCE].miles(), bearing.radians())
        l = Location(target[0], target[1], 0, Unit.RADIANS)
        print(f"{round(reticle, 2)} - {bearing}: {l.latLonDeg()}")

#
# Main Executable
#
if __name__ == "__main__":
    for degrees in range(0, 360, 15):
        bearing = Bearing(degrees, Unit.DEGREES)
        dumpLatLongTable(census, bearing)
        print()
        print("=====================================")
        print(census.convertTo(Unit.DEGREES))
        print(census.convertTo(Unit.RADIANS))
        print()
        print(bearing.convertTo(Unit.DEGREES))
        print(bearing.convertTo(Unit.RADIANS))
        print()
        d = Distance(.98765, Unit.METERS)
        print(d)
        print(d.convertTo(Unit.FEET))
        print(d.convertTo(Unit.METERS))
        print(d.convertTo(Unit.KILOMETERS))
        print(d.convertTo(Unit.MILES))
        print(d.convertTo(Unit.NAUTICAL_MILES))

        print()
        h = Height(143.5, Unit.FEET)
        print(h)
        print(h.convertTo(Unit.FEET))
        print(h.convertTo(Unit.METERS))
        print(h.convertTo(Unit.KILOMETERS))
        print(h.convertTo(Unit.MILES))
        print(h.convertTo(Unit.NAUTICAL_MILES))

        print()
        c = Coordinate(75, Unit.DEGREES)
        print(c)
        print(c.convertTo(Unit.RADIANS))

        print()
        l = Location(33, -118, h, Unit.DEGREES)
        print(l)
        print(l.convertTo(Unit.RADIANS))

        print()
        h = Height(143.5, Unit.FEET)
        print(h)
        print(h.convertTo(Unit.FEET))
        print(h.convertTo(Unit.METERS))
        print(h.convertTo(Unit.KILOMETERS))
        print(h.convertTo(Unit.MILES))
        print(h.convertTo(Unit.NAUTICAL_MILES))
