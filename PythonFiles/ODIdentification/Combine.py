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
totalTripCount = 0
interestTripCount = 0
odMapCount = 0
timeMapCount = 0
pathMapCount = 0

'''create the OD Nodes'''
# create a grid of Origins
# create the top left coordinate
TLNovaLat = 39.0646
TLNovaLong = -78.65719
TLNovaCoor = Coordinate.Coordinate(TLNovaLat, TLNovaLong)
# the size of the grid, this is in km
novaSize = 240
# the number of sections wanted
novaNum = 3
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

for nova in novaGrid:
    for dc in dcGrid:
        # create inbound node
        inBoundNode = ODNode.ODNode(nova, dc, 0)
        inBoundNode.createTimeIntervals(startAM, endAM, timeInterval)

        # create outbound node
        outBoundNode = ODNode.ODNode(dc, nova, 0)
        outBoundNode.createTimeIntervals(startAM, endAM, timeInterval)

        # append to container
        ODNodes.insert(inBoundNode)
        ODNodes.insert(outBoundNode)

for i in range(0, 2):
    '''the real input file name'''
    inputIterFileName = inputFileName + "-" + str(i) + ".txt"

    '''update the virtual objects based on the output of other files'''
    with open(inputIterFileName, 'r') as inputFile:

        for line in inputFile:
            line = line.strip()

            '''get the general attributes from the outputfile'''
            if line.__contains__("Total Trips"):
                totalTripCount += int(line[13:])
            if line.__contains__("Int Trips"):
                interestTripCount += int(line[13:])
            if line.__contains__("OD Maps"):
                odMapCount += int(line[13:])
            if line.__contains__("Time Maps"):
                timeMapCount += int(line[13:])
            if line.__contains__("Path Maps"):
                pathMapCount += int(line[13:])

            '''if we are looking at a new od node'''
            while line.__contains__("Index"):

                '''get the origin of the od node'''
                voriginLine = inputFile.readline().strip()
                if voriginLine == '':
                    break

                vorigin = voriginLine[8:]
                vcommaIndex = vorigin.index(",")
                voriginLat = vorigin[:vcommaIndex]
                voriginLong = vorigin[vcommaIndex + 1:]
                voriginC = Coordinate.Coordinate(float(voriginLat), float(voriginLong))

                '''get the destination of the od node'''
                vdestLine = inputFile.readline().strip()
                vdestination = vdestLine[13:]
                vcommaIndex = vdestination.index(",")
                vdestlat = vdestination[:vcommaIndex]
                vdestlong = vdestination[vcommaIndex + 1:]
                vdestC = Coordinate.Coordinate(float(vdestlat), float(vdestlong))

                '''get the count of the od node'''
                vcountLine = inputFile.readline().strip()
                vcount = vcountLine[7:]

                '''get the am count of the od node'''
                vamCountLine = inputFile.readline().strip()
                vamCount = vamCountLine[9:]

                '''get the pm count of the od node'''
                vpmCountLine = inputFile.readline().strip()
                vpmCount = vpmCountLine[9:]

                '''create the od node'''
                vodnode = ODNode.ODNode(voriginC, vdestC, int(vcount))

                '''update the period counts of the od node'''
                vodnode.setAmCount(int(vamCount))
                vodnode.setPmCount(int(vpmCount))

                '''readout the "Times: "'''
                readOut = inputFile.readline().strip()

                '''update the times of the od node'''
                vt = inputFile.readline().strip()

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
                    nl = inputFile.readline().strip()

                    # changed the output of the hashtable to be correct
                    if nl.__contains__("Paths"):

                        nl = inputFile.readline().strip()

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

                            nl = inputFile.readline().strip()

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
                            temp.setCount(vodnode.getCount() + temp.getCount())
                            temp.setPmCount(vodnode.getPmCount() + temp.getAmCount())
                            temp.setAmCount(vodnode.getAmCount() + temp.getAmCount())

    inputFile.close()

'''output the results to the outputfile'''
with open(outputFileName, 'w') as outputTextFile:
    '''write the header'''
    outputTextFile.write("Total Trips: " + str(totalTripCount))
    outputTextFile.write("\nInt Trips  : " + str(interestTripCount))
    outputTextFile.write("\nOD Maps    : " + str(odMapCount))
    outputTextFile.write("\nTime Maps  : " + str(timeMapCount))
    outputTextFile.write("\nPath Maps  : " + str(pathMapCount))

    outputTextFile.write("\n" + ODNodes.toString())
outputTextFile.close()



# end of file
