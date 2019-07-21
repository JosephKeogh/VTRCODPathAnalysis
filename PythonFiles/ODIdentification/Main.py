import sys
import csv
from datetime import datetime, timedelta
import time
import math
from Objects import Coordinate, HashTable, ODNode, TimeNode, PathNode, LatLongMath

PYTHONHASHSEED = 0

# cd git/VTRC*/Python*/OD*


year1 = 2017
year2 = 2018

startOfYear1DSTStr = '2017-03-12'
endOfYear1DSTStr = '2017-11-05'
startOfYear2DSTStr = '2018-03-11'
endOfYear2DSTStr = '2018-11-04'

EDT_UTC = -4             # 4 hours difference between Eastern Daylight (Savings) Time and UTC, UTC ahead by 4 hours
EST_UTC = -5             # 5 hours difference between Eastern Standard Time and UTC, UTC ahead by 5 hours

startOfYear1DST = datetime.strptime(startOfYear1DSTStr, "%Y-%m-%d")
endOfYear1DST = datetime.strptime(endOfYear1DSTStr, "%Y-%m-%d")
startOfYear2DST = datetime.strptime(startOfYear2DSTStr, "%Y-%m-%d")
endOfYear2DST = datetime.strptime(endOfYear2DSTStr, "%Y-%m-%d")


def timeToInt(ttime: str):
    """

    :param ttime: the time in "00:00"
    :return: an int of how many minutes have passed that day
    """

    """the current hour and min"""
    hour = ttime[0:2]
    minute = ttime[3:]

    hourInt = int(hour) * 60
    minInt = int(minute)

    return hourInt + minInt

def datetimeOfInterest(dt):
    for per in utcDatetimes:
        if per[0] <= dt and dt <= per[1]:
            return True
    return False


def convertToLocal(dt):
    currYear = datetime.strftime(dt, "%Y")
    if currYear == str(year1):
        currMonth = datetime.strftime(dt, "%m")
        currDay = datetime.strftime(dt, "%d")
        currDate = datetime.strptime(currYear + '-' + currMonth + '-' + currDay, "%Y-%m-%d")
        if currDate >= startOfYear1DST and currDate <= endOfYear1DST:
            result = dt + timedelta(hours = EDT_UTC)
        else:
            result = dt + timedelta(hours = EST_UTC)
    elif currYear == str(year2):
        currMonth = datetime.strftime(dt, "%m")
        currDay = datetime.strftime(dt, "%d")
        currDate = datetime.strptime(currYear + '-' + currMonth + '-' + currDay, "%Y-%m-%d")
        if currDate >= startOfYear2DST and currDate <= endOfYear2DST:
            result = dt + timedelta(hours = EDT_UTC)
        else:
            result = dt + timedelta(hours = EST_UTC)
    else:
        result = -1
    return result


# will show if the time is in the AM or PM peak, returns blank if neither
def correctPeakPeriod(h, p):
    return p == '' or h in range(5, 10) and p == 'AM' or h in range(15, 19) and p == 'PM'




# main --------------------------------------------------------------------


'''get the arguments from the command line input'''
programName = sys.argv.pop(0)                                 # ignore this program's name
inputFileName = sys.argv.pop(0)                 # input data file containing the timestamped waypoints snapped to XDs
utcDatetimeFileName = sys.argv.pop(0)           # file containing the UTC datetime periods of interest
outputTextFileName = sys.argv.pop(0)
wantProgramProgression = sys.argv.pop(0)        # will be "true" if the user wants to see programs progress
testingPerformance = sys.argv.pop(0)            # will only print out the time to analyze input file
programIteration = sys.argv.pop(0)

'''set up the actual input and output file names'''
inputFileName = inputFileName + str(programIteration) + ".csv"
outputTextFileName = outputTextFileName + "-" + str(programIteration) + ".txt"

'''what we want the program to output'''
'''turn command line inputs into boolean'''
printProgramProgression = False
if wantProgramProgression == "true":
    printProgramProgression = True

testPerformance = False
if testingPerformance == "true":
    testPerformance = True

'''running counters'''
TripCounter = 0
TripsOfInterestCounter = 0
ODCounter = 0
TimeCounter = 0
PathCounter = 0

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
        inBoundNode.setInbound(True)

        # create outbound node
        outBoundNode = ODNode.ODNode(dc, nova, 0)
        outBoundNode.createTimeIntervals(startAM, endAM, timeInterval)
        outBoundNode.setInbound(False)

        # append to container
        ODNodes.insert(inBoundNode)
        ODNodes.insert(outBoundNode)

# print progression statement
if printProgramProgression:
    print("HashTable of OD Nodes created of size: " + str(ODNodes.table.__len__()))
    print("To hold: " + str(minSizeOfHashTable) + " nodes")

'''update the virtual objects based on the output of other files'''
with open(outputTextFileName, 'r') as outputTextFile1:

    for line in outputTextFile1:
        line = line.strip()

        '''if we are looking at a new od node'''
        while line.__contains__("Index"):

            '''get the origin of the od node'''
            voriginLine = outputTextFile1.readline().strip()
            if voriginLine == '':
                break

            vorigin = voriginLine[8:]
            vcommaIndex = vorigin.index(",")
            voriginLat = vorigin[:vcommaIndex]
            voriginLong = vorigin[vcommaIndex + 1:]
            voriginC = Coordinate.Coordinate(float(voriginLat), float(voriginLong))

            '''get the destination of the od node'''
            vdestLine = outputTextFile1.readline().strip()
            vdestination = vdestLine[13:]
            vcommaIndex = vdestination.index(",")
            vdestlat = vdestination[:vcommaIndex]
            vdestlong = vdestination[vcommaIndex + 1:]
            vdestC = Coordinate.Coordinate(float(vdestlat), float(vdestlong))

            '''readout the direction'''
            direction = outputTextFile1.readline()

            '''get the count of the od node'''
            vcountLine = outputTextFile1.readline().strip()
            vcount = vcountLine[7:]

            print(vcountLine)

            '''get the am count of the od node'''
            vamCountLine = outputTextFile1.readline().strip()
            vamCount = vamCountLine[9:]

            '''get the pm count of the od node'''
            vpmCountLine = outputTextFile1.readline().strip()
            vpmCount = vpmCountLine[9:]

            '''create the od node'''
            vodnode = ODNode.ODNode(voriginC, vdestC, int(vcount))

            '''update the period counts of the od node'''
            vodnode.setAmCount(int(vamCount))
            vodnode.setPmCount(int(vpmCount))

            '''readout the "Times: "'''
            readOut = outputTextFile1.readline().strip()

            '''update the times of the od node'''
            vt = outputTextFile1.readline().strip()

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
                nl = outputTextFile1.readline().strip()

                # changed the output of the hashtable to be correct
                if nl.__contains__("Paths"):

                    nl = outputTextFile1.readline().strip()

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

                        nl = outputTextFile1.readline().strip()

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

outputTextFile1.close()


# print progression statement
if printProgramProgression:
    print("Output File read and OD Nodes Updated")

# load utcDatetimefile
# create an array of dateTimes of interest
utcDatetimes = []
with open(utcDatetimeFileName, newline='') as utcDatetimeFile:
    utcDatetimeData = csv.reader(utcDatetimeFile)
    next(utcDatetimeData, None)  # skip the headers
    for line in utcDatetimeData:
        utcDatetimes.append((datetime.strptime(line[0], "%Y-%m-%dT%H:%M"),
                             datetime.strptime(line[1], "%Y-%m-%dT%H:%M")))
utcDatetimeFile.close()

'''keep track of how long it takes the program to run'''
startTime = time.time()
lastTime = time.time()

# print progression statement
if printProgramProgression:
    print("Reading input file: ")

'''this will be used to map Waypoint trip IDs to ODNodes'''
tripIDandODNode = {}

tripPaths = {}
'''read in the file that contains TripIDs and paths'''
with open("tripsDetected.csv", 'r', newline='') as trips:
    reader = csv.reader(trips)

    '''create all the paths'''
    '''the file contains mulitple paths for one trip id, so must consolidate'''
    for line in reader:
        '''index 0 is the tripID, index 1 is the path it was identified on'''
        if line[0] != "tripID":
            if tripPaths.__contains__(line[0]):
                tripPaths[line[0]] = tripPaths[line[0]] + "---" + line[1]
            else:
                tripPaths[line[0]] = line[1]

trips.close()

'''read in the file that contains TripIDs and paths'''
with open("tripsDetected (1).csv", 'r', newline='') as trips:
    reader = csv.reader(trips)

    '''create all the paths'''
    '''the file contains mulitple paths for one trip id, so must consolidate'''
    for line in reader:
        '''index 0 is the tripID, index 1 is the path it was identified on'''
        if line[0] != "tripID":
            if tripPaths.__contains__(line[0]):
                tripPaths[line[0]] = tripPaths[line[0]] + "---" + line[1]
            else:
                tripPaths[line[0]] = line[1]

trips.close()

# load input file and process it line by line
# count the OD
'''analyze the input file'''
with open(inputFileName, 'r') as inputFile:

    # read the file
    reader = csv.reader(inputFile)

    # loop through the data lines
    for inputLine in reader:

        TripCounter += 1

        # print progression statement
        if printProgramProgression:
            if TripCounter % 100000 == 0:
                thisTime = time.time()
                print("Line: " + str(TripCounter) + " - In " + str(int(thisTime - lastTime)) + " sec - Total Time: " +
                      str(int(thisTime - startTime)))
                lastTime = thisTime

        # the start and end date of this capture
        startDate = inputLine[4][:16]
        captureUTCDateStartTime = datetime.strptime(startDate, "%Y-%m-%dT%H:%M")
        endDate = inputLine[4][:16]
        captureUTCDateEndTime = datetime.strptime(endDate, "%Y-%m-%dT%H:%M")

        # if we should be looking at this date
        if datetimeOfInterest(captureUTCDateStartTime):

            startDateLocal = convertToLocal(captureUTCDateStartTime)

            # if the convert to local time was successful
            # do the actual counting
            if startDateLocal != -1:

                '''increment that this trip was during the period of interest'''
                TripsOfInterestCounter += 1

                # assign data values to variables
                tripID = inputLine[0]
                StartLat = inputLine[8]
                StartLong = inputLine[9]
                EndLat = inputLine[10]
                EndLong = inputLine[11]
                weekDay = int(inputLine[5])

                # snap to origin and desination sections
                # snap to OD node

                # update the count on that OD node
                # create a place holder OD
                origin = Coordinate.Coordinate(StartLat, StartLong)
                destination = Coordinate.Coordinate(EndLat, EndLong)
                tempNode = ODNode.ODNode(origin, destination, 0)

                # find if the origin and destination are of interst
                # if they are of interest, incremement the appropriate ODNode
                if ODNodes.__contains__(tempNode, novaClose, dcClose):
                    '''find the correct od node'''
                    n = ODNodes.find(tempNode, novaClose, dcClose)
                    '''find the index of the correct od node'''
                    getindex = ODNodes.getIndex(tempNode, novaClose, dcClose)

                    '''add the trip id to the dict of trip id mapped to od node index'''
                    tripIDandODNode[tripID] = getindex

                    '''increment the correct od node'''
                    n.inc()
                    '''make note that this was mapped'''
                    ODCounter += 1

                    '''if this trip was at a time that can be mapped'''
                    tempTimeNode = TimeNode.TimeNode(startDateLocal, weekDay, timeInterval)
                    if n.__contains__(tempTimeNode):

                        '''find the correct timenode'''
                        t = n.findTime(tempTimeNode)

                        '''add the tripID to the list of trip ids'''
                        t.addTripID(tripID)

                        '''increment the correct time node'''
                        t.inc()

                        '''increment the global count of time maps'''
                        TimeCounter += 1

                        '''incremement the correct period in od node'''
                        if timeToInt(t.getTimeID()) < timeToInt("12:00"):
                            n.incAmCount()
                        else:
                            n.incPmCount()

                        '''the path that was taken'''
                        a = False
                        b = False
                        '''if this trip id can be mapped to a path'''
                        if tripPaths.__contains__(tripID):
                            path = tripPaths[tripID]
                            a = True
                            PathCounter += 1
                            '''if this path is already a part of the time nodes path'''
                            if t.getPaths().__contains__(path):
                                b = True

                        if a:
                            if b:
                                '''increment the count'''
                                oldPaths = t.getPaths()
                                newPaths = oldPaths
                                newPaths[path].inc()
                                t.setPaths(newPaths)

                            elif b is False:
                                '''if this path has not been seen yet'''
                                oldPaths = t.getPaths()
                                newPaths = oldPaths
                                newPaths[path] = PathNode.PathNode(path)
                                newPaths[path].inc()
                                t.setPaths(newPaths)

inputFile.close()

# end the timer
endTime = time.time()
totalTime = float(endTime - startTime)

# print progression statement
if printProgramProgression:
    print(str(totalTime)[:5] + " seconds to analyze input file")

# for performance testing purposes only
if testPerformance is True:
    print(str(totalTime))

'''read the basic info from the output file'''
with open(outputTextFileName, 'r') as outputTextFile:
    line = outputTextFile.readline().strip()
    TripCounter = TripCounter + int(line[13:])

    line = outputTextFile.readline().strip()
    TripsOfInterestCounter = TripsOfInterestCounter + int(line[13:])

    line = outputTextFile.readline().strip()
    ODCounter = ODCounter + int(line[13:])

    line = outputTextFile.readline().strip()
    TimeCounter = TimeCounter + int(line[13:])

    line = outputTextFile.readline().strip()
    PathCounter = PathCounter + int(line[13:])
outputTextFile.close()

with open(outputTextFileName, 'w') as outputTextFile:
    '''write the header'''
    outputTextFile.write("Total Trips: " + str(TripCounter))
    outputTextFile.write("\nInt Trips  : " + str(TripsOfInterestCounter))
    outputTextFile.write("\nOD Maps    : " + str(ODCounter))
    outputTextFile.write("\nTime Maps  : " + str(TimeCounter))
    outputTextFile.write("\nPath Maps  : " + str(PathCounter))
    outputTextFile.write("\n" + ODNodes.toString())
outputTextFile.close()

# print progression statement
if printProgramProgression:
    print(str(programName) + " Complete")

# end of file
