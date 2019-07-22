import sys
import csv
from datetime import datetime, timedelta
import time
import math
from Objects import Coordinate, HashTable, ODNode, TimeNode, PathNode, LatLongMath

sys.argv.pop(0)                                 # ignore this program's name
inputFileName = sys.argv.pop(0)
outputFileName = sys.argv.pop(0)

'''running counters'''
TripCounter = 0
TripsOfInterestCounter = 0
ODCounter = 0
TimeCounter = 0
PathCounter = 0

'''create the OD Nodes'''
# create a grid of Origins
# create the top left coordinate
TLNovaLat = 39.03815
TLNovaLong = -77.63416
TLNovaCoor = Coordinate.Coordinate(TLNovaLat, TLNovaLong)
# the size of the grid, this is in km
novaSize = 60
# the number of sections wanted
novaNum = int(novaSize / 4.82)
# create the actual grid
novaGrid = TLNovaCoor.createGrid(novaSize, novaNum)

# create a grid of Desitinations
TLDcLat = 39.11
TLDcLong = -77.284
TLDcCoor = Coordinate.Coordinate(TLDcLat, TLDcLong)
dcSize = 40
dcNum = 3
dcGrid = TLDcCoor.createGrid(dcSize, dcNum)

# the variable that is the distance for a point to be close to another
novaClose = (1 / 2) * (novaSize / (novaNum - 1)) * math.sqrt(2)
dcClose = (1 / 2) * (dcSize / (dcNum - 1)) * math.sqrt(2)

# the time information
startAM = "00:00"
endAM = "24:00"
timeInterval = 30

# create a complete list of OD nodes
# each origin has all of the destinations
minSizeOfHashTable = dcGrid.__len__() * novaGrid.__len__() * 2
ODNodes = HashTable.HashTable(minSizeOfHashTable)  # a container of OD Nodes

print("creating od grid...")
for nova in novaGrid:
    for dc in dcGrid:
        # create inbound node
        inBoundNode = ODNode.ODNode(nova, dc, 0)
        inBoundNode.createTimeIntervals(startAM, endAM, timeInterval)
        inBoundNode.setInbound(True)

        # create outbound node
        outBoundNode = ODNode.ODNode(dc, nova, 0)
        outBoundNode.createTimeIntervals(startAM, endAM, timeInterval)
        outBoundNode.setInbound(False)

        # append to container
        ODNodes.insert(inBoundNode)
        ODNodes.insert(outBoundNode)

'''update the virtual objects based on the output of other files'''
print("reading output file...")
with open(outputFileName, 'r') as outputFile:

    for line in outputFile:

        line = line.strip()

        '''get the general attributes from the outputfile'''
        if line.__contains__("Total Trips"):
            TripCounter += int(line[13:])
        if line.__contains__("Int Trips"):
            TripsOfInterestCounter += int(line[13:])
        if line.__contains__("OD Maps"):
            ODCounter += int(line[13:])
        if line.__contains__("Time Maps"):
            TimeCounter += int(line[13:])
        if line.__contains__("Path Maps"):
            PathCounter += int(line[13:])

        '''if we are looking at a new od node'''
        while line.__contains__("Index"):

            '''get the origin of the od node'''
            voriginLine = outputFile.readline().strip()
            if voriginLine == '':
                break

            vorigin = voriginLine[8:]
            vcommaIndex = vorigin.index(",")
            voriginLat = vorigin[:vcommaIndex]
            voriginLong = vorigin[vcommaIndex + 1:]
            voriginC = Coordinate.Coordinate(float(voriginLat), float(voriginLong))

            '''get the destination of the od node'''
            vdestLine = outputFile.readline().strip()
            vdestination = vdestLine[13:]
            vcommaIndex = vdestination.index(",")
            vdestlat = vdestination[:vcommaIndex]
            vdestlong = vdestination[vcommaIndex + 1:]
            vdestC = Coordinate.Coordinate(float(vdestlat), float(vdestlong))

            '''readout the direction'''
            direction = outputFile.readline()

            '''get the count of the od node'''
            vcountLine = outputFile.readline().strip()
            vcount = vcountLine[7:]

            '''get the am count of the od node'''
            vamCountLine = outputFile.readline().strip()
            vamCount = vamCountLine[9:]

            '''get the pm count of the od node'''
            vpmCountLine = outputFile.readline().strip()
            vpmCount = vpmCountLine[9:]

            '''create the od node'''
            vodnode = ODNode.ODNode(voriginC, vdestC, int(vcount))
            vodnode.createTimeIntervals(startAM, endAM, timeInterval)

            '''update the period counts of the od node'''
            vodnode.setAmCount(int(vamCount))
            vodnode.setPmCount(int(vpmCount))

            '''readout the "Times: "'''
            readOut = outputFile.readline().strip()

            '''update the times of the od node'''
            vt = outputFile.readline().strip()

            '''for all the timenodes listed'''
            while vt.__contains__("WeekDay"):
                '''get the weekday, time, and count'''
                weekday = int(vt[9:11])
                vtime = vt[19:24]
                vcount = int(vt[32:])

                '''create the TimeNode'''
                vdt = datetime.strptime(vtime, "%H:%M")
                vtimenode = TimeNode.TimeNode(vdt, weekday, timeInterval)
                vtimenode.setCount(vcount)

                '''the dict to be used as the dict of paths for timenode'''
                paths = {}

                '''read the next line in the file'''
                nl = outputFile.readline().strip()

                # changed the output of the hashtable to be correct
                if nl.__contains__("Paths"):

                    nl = outputFile.readline().strip()

                    while nl.__contains__("PathID"):

                        '''get the PathNode attributes'''
                        countIndex = nl.index("Count:")
                        path = nl[8:countIndex - 1]
                        count = nl[countIndex + 7:]

                        '''create the pathNode'''
                        pathNode = PathNode.PathNode(path)
                        pathNode.setCount(int(count))

                        '''add the PathNode to the dict of PathNodes'''
                        paths[path] = pathNode

                        nl = outputFile.readline().strip()

                    vt = nl

                '''set the paths of the time node'''
                vtimenode.setPaths(paths)

                vt = nl

                '''add the time node to the list of times in od node'''
                vodnode.addTimeNode(vtimenode)

            if vt.__contains__("Index"):
                line = vt

            '''update the actual node in the HashTable'''
            '''only have to update if the node info is not 0'''
            if vodnode.getCount() > 0:
                for temp in ODNodes.table:
                    if temp.__eq__(vodnode):
                        temp.setCount(vodnode.getCount())
                        temp.setTimes(vodnode.getTimes())
                        temp.setPmCount(vodnode.getPmCount())
                        temp.setAmCount(vodnode.getAmCount())

outputFile.close()

print("reading input file...")

'''read in one of the partial output files and update the nodes accordingly'''
with open(inputFileName, 'r') as inputfile:

    for line in inputfile:

        line = line.strip()

        '''get the general attributes from the outputfile'''
        if line.__contains__("Total Trips"):
            TripCounter += int(line[13:])
        if line.__contains__("Int Trips"):
            TripsOfInterestCounter += int(line[13:])
        if line.__contains__("OD Maps"):
            ODCounter += int(line[13:])
        if line.__contains__("Time Maps"):
            TimeCounter += int(line[13:])
        if line.__contains__("Path Maps"):
            PathCounter += int(line[13:])

        '''if we are looking at a new od node'''
        while line.__contains__("Index"):

            '''get the origin of the od node'''
            voriginLine = inputfile.readline().strip()
            if voriginLine == '':
                break

            vorigin = voriginLine[8:]
            vcommaIndex = vorigin.index(",")
            voriginLat = vorigin[:vcommaIndex]
            voriginLong = vorigin[vcommaIndex + 1:]
            voriginC = Coordinate.Coordinate(float(voriginLat), float(voriginLong))

            '''get the destination of the od node'''
            vdestLine = inputfile.readline().strip()
            vdestination = vdestLine[13:]
            vcommaIndex = vdestination.index(",")
            vdestlat = vdestination[:vcommaIndex]
            vdestlong = vdestination[vcommaIndex + 1:]
            vdestC = Coordinate.Coordinate(float(vdestlat), float(vdestlong))

            '''readout the direction'''
            direction = inputfile.readline()

            '''get the count of the od node'''
            vcountLine = inputfile.readline().strip()
            vcount = vcountLine[7:]

            '''get the am count of the od node'''
            vamCountLine = inputfile.readline().strip()
            vamCount = vamCountLine[9:]

            '''get the pm count of the od node'''
            vpmCountLine = inputfile.readline().strip()
            vpmCount = vpmCountLine[9:]

            '''create the od node'''
            vodnode = ODNode.ODNode(voriginC, vdestC, int(vcount))

            '''update the period counts of the od node'''
            vodnode.setAmCount(int(vamCount))
            vodnode.setPmCount(int(vpmCount))

            realODNode = ODNode.ODNode(Coordinate.Coordinate(0, 0), Coordinate.Coordinate(0, 0), 0 )

            for node in ODNodes.table:
                if node.__eq__(vodnode):
                    realODNode = node

            # realODNode = ODNodes.find(vodnode, novaClose, dcClose)
            realODNode.setCount(realODNode.getCount() + vodnode.getCount())
            realODNode.setAmCount(realODNode.getAmCount() + vodnode.getAmCount())
            realODNode.setPmCount(realODNode.getPmCount() + vodnode.getPmCount())

            '''readout the "Times: "'''
            readOut = inputfile.readline().strip()

            '''update the times of the od node'''
            vt = inputfile.readline().strip()

            '''for all the timenodes listed'''
            while vt.__contains__("WeekDay"):
                '''get the weekday, time, and count'''
                weekday = int(vt[9:11])
                vtime = vt[19:24]
                vcount = int(vt[32:])

                '''create the TimeNode'''
                vdt = datetime.strptime(vtime, "%H:%M")
                vtimenode = TimeNode.TimeNode(vdt, weekday, timeInterval)
                vtimenode.setCount(vcount)

                vtimecode = str(vtimenode.getTimeID() + str(vtimenode.getWeekDay()))

                '''update the real time node'''
                realTimeNode = realODNode.findTime(vtimenode)
                realTimeNode.setCount(realTimeNode.getCount() + vtimenode.getCount())

                '''the dict to be used as the dict of paths for timenode'''
                paths = {}

                '''read the next line in the file'''
                nl = inputfile.readline().strip()

                # changed the output of the hashtable to be correct
                if nl.__contains__("Paths"):

                    nl = inputfile.readline().strip()

                    while nl.__contains__("PathID"):
                        '''get the PathNode attributes'''
                        countIndex = nl.index("Count:")
                        path = nl[8:countIndex - 1]
                        count = nl[countIndex + 7:]

                        '''if this path has already been seen'''
                        if realTimeNode.getPaths().__contains__(path) is True:
                            old = realTimeNode.getPaths()
                            new = old
                            timeNode = new[path]
                            oldCount = timeNode.getCount()
                            newCount = oldCount + count
                            timeNode.setCount(newCount)
                            new[path] = timeNode
                            realTimeNode.setPaths(new)

                        '''if this node has not already been seen'''
                        if realTimeNode.getPaths().__contains__(path) is False:
                            old = realTimeNode.getPaths()
                            new = old
                            pathNode = PathNode.PathNode(path)
                            pathNode.inc()
                            new[path] = pathNode
                            realTimeNode.setPaths(new)

                        nl = inputfile.readline().strip()

                    vt = nl

                vt = nl

            if vt.__contains__("Index"):
                line = vt

inputfile.close()

'''put the results into the final file'''
with open(outputFileName, 'w') as outputTextFile:
    '''write the header'''
    outputTextFile.write("Total Trips: " + str(TripCounter))
    outputTextFile.write("\nInt Trips  : " + str(TripsOfInterestCounter))
    outputTextFile.write("\nOD Maps    : " + str(ODCounter))
    outputTextFile.write("\nTime Maps  : " + str(TimeCounter))
    outputTextFile.write("\nPath Maps  : " + str(PathCounter))
    outputTextFile.write("\n" + ODNodes.toString())
outputTextFile.close()


# end of file
