import Coordinate
import PathNode
import TimeNode
import ODNode
import HashTable
from datetime import datetime, timedelta


"""create a list of times in an OD node"""

"""map a timenode to the correct node in the OD list of timeNodes"""

"""PersonA took PathB at TimeC from OriginD to DestinationE"""

timeTolerance = 30
"""the variables that PersonA used"""
OriginD = Coordinate.Coordinate(40, -78)
DestinationE = Coordinate.Coordinate(50, -80)

timeCString = "08:00"
timeCDate = datetime.strptime(timeCString, "%H:%M")
TimeC = TimeNode.TimeNode(timeCDate, timeTolerance)

pathB = "66W"

"""process to capture event"""

"""create a hashTable"""
ODNodes = HashTable.HashTable(1)
odNode = ODNode.ODNode(Coordinate.Coordinate(40.5, -78), Coordinate.Coordinate(50.5, -80), 0)
ODNodes.insert(odNode)

"""create a list of times to be looked at"""
odNode.createTimeIntervals("06:00", "10:00", timeTolerance)

# print("initial Node with Times Added")
# print(odNode.toString())

"""see if PersonA's origin and destination can be mapped"""
tempNode = ODNode.ODNode(OriginD, DestinationE, 0)

if ODNodes.__contains__(tempNode, 100, 100):
    """find and increment the correct node"""
    n = ODNodes.find(tempNode, 100, 100)

    """increment the count on this node"""
    n.inc()

    # print("after the odnode was mapped")
    # print(odNode.toString())

    """if PersonA left at a time that can be mapped"""
    if n.__contains__(TimeC):
        t = n.findTime(TimeC)

        t.inc()

        # print("after time was found and incremented")
        # print(odNode.toString())

        PathB = PathNode.PathNode(pathB)

        """if PersonA took a recognizable trip"""
        if t.contains(PathB):
            path = t.findPath(PathB)
            path.inc()
        else:
            t.addPath(PathB)
            path = t.findPath(PathB)
            path.inc()

        # print("after trip had been found")
        # print(odNode.toString())

'''personB starts and ends at the same places as personA, and takes the same path, but leaves an hour earlier'''
# print("\n\n            PERSONB              ")
timeFString = "07:00"
timeFDate = datetime.strptime(timeFString, "%H:%M")
TimeF = TimeNode.TimeNode(timeFDate, timeTolerance)


"""see if PersonA's origin and destination can be mapped"""
tempNode = ODNode.ODNode(OriginD, DestinationE, 0)

if ODNodes.__contains__(tempNode, 100, 100):
    """find and increment the correct node"""
    n = ODNodes.find(tempNode, 100, 100)

    """increment the count on this node"""
    n.inc()

    # print("after the odnode was mapped")
    # print(odNode.toString())

    """if PersonA left at a time that can be mapped"""
    if n.__contains__(TimeF):
        t = n.findTime(TimeF)

        t.inc()

        # print("after time was found and incremented")
        # print(odNode.toString())

        PathB = PathNode.PathNode(pathB)

        """if PersonA took a recognizable trip"""
        if t.contains(PathB):
            path = t.findPath(PathB)
            path.inc()
        else:
            t.addPath(PathB)
            path = t.findPath(PathB)
            path.inc()

        # print("after trip had been found")
        print(odNode.toString())





""""""





# end of file