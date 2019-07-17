import math

def latlongDistance(lat1, long1, lat2, long2):
    latDiff = lat1 - lat2
    longDiff = long1 - long2

    latDiffDist = latDiff * 111
    longDiffDist = longDiff * (math.radians(lat1) * 111)

    distance = math.sqrt(math.pow(latDiffDist, 2) + math.pow(longDiffDist, 2))

    return distance


# this function takes the top left lat and long coordinate and the size of the grid,
# the size is in km
# returns the four coordinates needed to make a grid of that size
# returns the lat and long in clockwise order, starting at the top left
def createSquare(lat, long, size):
    latTop = lat
    latBottom = -(size/111 - latTop)

    longLeft = long
    longRight = -((size/(math.radians(latTop)*111)) + longLeft)

    points = [latTop, longLeft, latTop, longRight, latBottom, longRight, latBottom, longLeft]

    return points


# this function is the same as the near function, but it does the distance based on lat long coordinates
def latLongNear(lat1, long1, lat2, long2, dist):
    distance = latlongDistance(lat1, long1, lat2, long2)
    if distance <= dist:
        return True
    else:
        return False

# end of file
