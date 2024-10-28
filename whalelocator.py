#!/opt/homebrew/anaconda3/bin/python

from math import sin, cos, asin, acos, atan2, sqrt, pi
from haversine import haversine, inverse_haversine, inverse_haversine_vector, Unit, Direction
from numpy import arange

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

horizonCoefficient          = 1.22459
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
                    return self.distance
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
                    return self.distance
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
                    return self.distance
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
                    return self.distance
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
                    return self.height
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
                    return self.height
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
                    return self.height * milesToMeters
                case Unit.METERS:
                    return self.height
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
                    return self.height
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
                    return self.height
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
def reticleToDistance(observer, reticle):
        h = observer.height().meters()
        m = reticle * 5
        if m < 0:
            raise(Exception(f"Mils cannot be negative: {m}"))
        if m > 0:
            return Distance(round(h * 1000 / m, 1), Unit.METERS)
        else:
            return Distance(horizonCoefficient * sqrt(h), Unit.METERS)

#===================================================================================#
#                                    OUTPUT FILES                                   #
#===================================================================================#
directory                   = '/Users/mbi/Documents/Programming/Whale Locator/'
filenameBase                = 'Test Run - '
def dumpLatLongTable(observer: Location, bearing: Bearing):
    if directory:
        f = open(f"{directory}{filenameBase}{bearing.degrees()}.csv", "w")
    else:
        f = open(f"{filenameBase}{bearing.degrees()}.csv", "w")

    f.write("Lattitude, Longitude\n")
    for reticle in arange(0, 20.1, 0.1):
        d = reticleToDistance(observer, reticle)
        target = inverse_haversine(census.latLonRad(), d.miles(), bearing.radians())
        l = Location(target[0], target[1], 0, Unit.RADIANS)
        # print(f"{l.latDeg()}, {l.lonDeg()}")
        f.write(f"{l.latDeg()}, {l.lonDeg()}\n")

#
# Main Executable
#
if __name__ == "__main__":
    for degrees in range(0, 360, 15):
        bearing = Bearing(degrees, Unit.DEGREES)
        dumpLatLongTable(census, bearing)