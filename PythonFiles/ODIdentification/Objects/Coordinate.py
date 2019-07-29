from Objects import LatLongMath
import math


class Coordinate:
    def __init__(self, lat, long):
        self.lat = float(lat)
        self.long = float(long)
        self.district = "blank"

    def getDistrict(self):
        return self.district

    def setDistrict(self, d: str):
        self.district = d

    def getLong(self):
        return self.long

    def getLat(self):
        return self.lat

    def getDist(self, point):
        return LatLongMath.latlongDistance(self.lat, self.long, point.getLat(), point.getLong())

    def close(self, point, dd):
        return LatLongMath.latLongNear(self.lat, self.long, point.getLat(), point.getLong(), dd)

    def equals(self, point):
        if self.lat == point.getLat():
            if self.long == point.getLong():
                return True
        return False

    def toString(self):
        return str(self.lat) + ", " + str(self.long)

    def toStringShort(self):
        return str(self.lat)[0:6] + ", " + str(self.long)[0:6]

    def print(self):
        print(str(self.lat) + ", " + str(self.long))

    def __eq__(self, other):
        if self.lat.__eq__(other.getLat()):
            if self.long.__eq__(other.getLong()):
                return True
            else:
                return False
        else:
            return False

    # returns the point that is dist distance away from self to the east
    # dist is in km
    def getEast(self, da):
        newLong = ((da / (math.radians(self.lat) * 111)) + self.long)
        point = Coordinate(self.lat, newLong)
        return point

    # returns the point that is dist distance away from self to the south
    # dist is in km
    def getSouth(self, da):
        newLat = -(da / 111 - self.lat)
        point = Coordinate(newLat, self.long)
        return point

    # creates a grid with area size^2 with num^2 number of points
    # size is in km
    def createGrid(self, size, num):

        # the array of points
        points = []

        # the distance between the points (horizontally or vertically)
        dist = size / (num - 1)

        curPoint = self
        rowStart = self

        # iterate for number of rows
        for a in range(0, num):

            # append the first row point
            points.append(rowStart)

            # set up the row
            # head east
            for b in range(0, num - 1):
                # find the next point
                newRow = curPoint.getEast(dist)

                # add the newest point to the list
                points.append(newRow)

                # change the reference point
                curPoint = newRow

            # go to the next row
            newPoint = rowStart.getSouth(dist)

            # rearrange points
            curPoint = newPoint
            rowStart = newPoint

        return points



# end of file
