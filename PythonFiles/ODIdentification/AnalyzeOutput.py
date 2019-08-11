from Objects import Coordinate, TimeNode, ODNode, PathNode, HashTable, ODRegion
from datetime import datetime, timedelta
import sys
import csv
import time
import matplotlib.pyplot as plt
from pykml import parser

programName = sys.argv.pop(0)                                 # ignore this program's name
inputFileName = sys.argv.pop(0)
outputFileName = sys.argv.pop(0)
sys.argv.append(programName)
'''functions'''

def timeToInt(now):
    """

    :param time: the time in "00:00"
    :return: an int of how many minutes have passed that day
    """

    """the current hour and min"""
    hour = now[0:2]
    min = now[3:]

    hourInt = int(hour) * 60
    minInt = int(min)

    return hourInt + minInt


'''the time intervals we are looking at'''
timeInterval = 30

"""the running counts"""
totalAM = 0
totalPM = 0
totalCountFromNodes = 0

"""the marker between morning and afternoon"""
noonTime = "12:00"
noon = timeToInt(noonTime)

'''list of od nodes'''
ODNodes = []


with open(inputFileName, 'r') as outputTextFile1:

    for line in outputTextFile1:
        line = line.strip()

        '''get the general attributes from the outputfile'''
        if line.__contains__("Total Trips"):
            totalTripCount = int(line[13:])
        if line.__contains__("Int Trips"):
            interestTripCount = int(line[13:])
        if line.__contains__("OD Maps"):
            odMapCount = int(line[13:])
        if line.__contains__("Time Maps"):
            timeMapCount = int(line[13:])
        if line.__contains__("Path Maps"):
            pathMapCount = int(line[13:])

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

            '''get the am count of the od node'''
            vamCountLine = outputTextFile1.readline().strip()
            vamCount = vamCountLine[9:]

            '''get the pm count of the od node'''
            vpmCountLine = outputTextFile1.readline().strip()
            vpmCount = vpmCountLine[9:]

            '''increment the global time period totals'''
            totalAM += int(vamCount)
            totalPM += int(vpmCount)

            '''create the od node'''
            vodnode = ODNode.ODNode(voriginC, vdestC, int(vcount))

            '''update the period counts of the od node'''
            vodnode.setAmCount(int(vamCount))
            vodnode.setPmCount(int(vpmCount))

            '''set the direction of the node'''
            if direction.__contains__("In-"):
                vodnode.setInbound(True)
            else:
                vodnode.setInbound(False)

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

            '''add the od node to the list of od nodes'''
            '''only if it is not an empty node'''
            e = Coordinate.Coordinate(0, 0)
            empty = ODNode.ODNode(e, e, 0)
            if vodnode.__eq__(empty) is False:
                ODNodes.append(vodnode)

outputTextFile1.close()

def basicInfo():

    s = ""
    s = s + "--- Basic Info ---"
    s = s + "\nNumber of ODNodes: " + str(ODNodes.__len__())

    s = s + "\n\n--- Raw Numbers ---"
    s = s + "\nTotal Trips: " + str(totalTripCount)
    s = s + "\nInt Trips  : " + str(interestTripCount)
    s = s + "\nOD Maps    : " + str(odMapCount)
    s = s + "\nTime Maps  : " + str(timeMapCount)
    s = s + "\nTotal AM   : " + str(totalAM)
    s = s + "\nTotal PM   : " + str(totalPM)
    s = s + "\nPath Maps  : " + str(pathMapCount)
    
    return s

def nodePercentAnalysis():

    s = "\n\n--- Node Percent Analysis ---"
    s = s + "\nTrips of Interest % : " + str(interestTripCount / totalTripCount)[:5]
    s = s + "\nInt Trips Map to OD : " + str(odMapCount / interestTripCount)[:5]
    s = s + "\nOD Trips Map to Time: " + str(timeMapCount / odMapCount)[:5]
    s = s + "\nTime Mapped to Path : " + str(pathMapCount / timeMapCount)[:5]
    s = s + "\nEnd Amount Mapped   : " + str(pathMapCount / totalTripCount)[:5]

    return s

def nodePathCountAnalysis(cutOff: int):
    '''to keep track of the counts per weekday'''
    weekdays = {}
    weekdayTotal = 0

    '''to keep track of the times'''
    justTimes = {}
    justTimeTotal = 0

    ''''to keep track of the paths'''
    justPaths = {}
    pathTotal = 0

    '''to keep track of the times per weekday'''
    weekdayTimes = {}
    weekdayTimeTotal = 0

    '''weekdays and paths'''
    weekdayPaths = {}
    weekdayPathTotal = 0

    '''time of day and paths'''
    timePaths = {}
    timePathTotal = 0

    '''all three'''
    weekdayHourPaths = {}
    weekdayHourPathTotal = 0

    '''list to hold all dicts'''
    l = []
    l.append(weekdays)
    l.append(justTimes)
    l.append(justPaths)
    l.append(weekdayTimes)
    l.append(weekdayPaths)
    l.append(timePaths)
    l.append(weekdayHourPaths)

    '''collect the counts for each path'''
    for node in ODNodes:

        times = node.getTimes()

        for t in times.values():

            wkdy = t.getWeekDay()
            hour = t.getTimeID()

            paths = t.getPaths()

            for p in paths.values():

                path = p.getPathID()
                count = p.getCount()

                '''path'''
                if justPaths.__contains__(path):
                    justPaths[path] = justPaths[path] + int(count)
                else:
                    justPaths[path] = int(count)

    with open("NodePathCounts.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for p in justPaths:
            a = [str(p), str(justPaths[p])]
            writer.writerow(a)
    csvfile.close()

    '''remove the paths that are not frequently used'''
    newPaths = justPaths.copy()
    for p in newPaths:
        if newPaths[p] < cutOff:
            del justPaths[p]

    '''update the other counts'''
    '''collect the counts for each path'''
    for node in ODNodes:

        times = node.getTimes()

        for t in times.values():

            wkdy = t.getWeekDay()
            hour = t.getTimeID()

            paths = t.getPaths()

            for p in paths.values():

                path = p.getPathID()
                count = p.getCount()

                '''if this path is one with a large enough count'''
                if path in justPaths.keys():

                    '''weekday'''
                    if weekdays.__contains__(wkdy):
                        weekdays[wkdy] = weekdays[wkdy] + int(count)
                    else:
                        weekdays[wkdy] = int(count)

                    '''hour'''
                    if justTimes.__contains__(hour):
                        justTimes[hour] = justTimes[hour] + int(count)
                    else:
                        justTimes[hour] = int(count)

                    '''weekday and hour'''
                    weekdayHour = str(wkdy) + " " + str(hour)
                    if weekdayTimes.__contains__(weekdayHour):
                        weekdayTimes[weekdayHour] = weekdayTimes[weekdayHour] + int(count)
                    else:
                        weekdayTimes[weekdayHour] = int(count)

                    '''weekday and path'''
                    weekdayPath = str(wkdy) + " " + str(path)
                    if weekdayPaths.__contains__(weekdayPath):
                        weekdayPaths[weekdayPath] = weekdayPaths[weekdayPath] + int(count)
                    else:
                        weekdayPaths[weekdayPath] = int(count)

                    '''hour and path'''
                    hourPath = str(hour) + " " + str(path)
                    if timePaths.__contains__(hourPath):
                        timePaths[hourPath] = timePaths[hourPath] + int(count)
                    else:
                        timePaths[hourPath] = int(count)

                    '''weekday and hour and path'''
                    weekdayHourPath = str(wkdy) + " " + str(hour) + " " + str(path)
                    if weekdayHourPaths.__contains__(weekdayHourPath):
                        weekdayHourPaths[weekdayHourPath] = weekdayHourPaths[weekdayHourPath] + int(count)
                    else:
                        weekdayHourPaths[weekdayHourPath] = int(count)

    for aa in weekdays.values():
        weekdayTotal += aa
    for aaa in timePaths.values():
        timePathTotal += aaa
    for aaaa in weekdayPaths.values():
        weekdayPathTotal += aaaa
    for aaaaa in weekdayTimes.values():
        weekdayTimeTotal += aaaaa
    for aaaaaa in justTimes.values():
        justTimeTotal += aaaaaa
    for aaaaaaa in justPaths.values():
        pathTotal += aaaaaaa
    for aaaaaaaa in weekdayHourPaths.values():
        weekdayHourPathTotal += aaaaaaaa

    '''list to hold all totals'''
    ll = []
    llNames = []
    llexamples = []
    ll.append(weekdayTotal)
    llNames.append("Average Weekday Total Path Count: ")
    llexamples.append("Example: Wednesday had 100 trips with map-able paths")
    ll.append(justTimeTotal)
    llNames.append("Average Time Segment Path Count: ")
    llexamples.append("Example: 08:00 had 100 trips with map-able paths")
    ll.append(pathTotal)
    llNames.append("Average Distinct Path Count: ")
    llexamples.append("Example: I-66 had 100 trips with map-able paths")
    ll.append(weekdayTimeTotal)
    llNames.append("Average Weekday Time Segment Path Count: ")
    llexamples.append("Example: Wednesday at 08:00 had 100 trips with map-able paths")
    ll.append(weekdayPathTotal)
    llNames.append("Average Weekday Distinct Path Count: ")
    llexamples.append("Example: I-66 on Wednesday had 100 trips with map-able paths")
    ll.append(timePathTotal)
    llNames.append("Average Time Segment on Distinct Path Path Count: ")
    llexamples.append("Example: I-66 on Wednesdays had 100 trips with map-able paths")
    ll.append(weekdayHourPathTotal)
    llNames.append("Average Distinct Path during Time Segment on Weekday Path Count: ")
    llexamples.append("Example: I-66 taken at 08:30 on Wednesdays had 100 trips with map-able paths")

    '''header'''
    s = "\n\n--- Path Count Analysis ---"
    s = s + "\nOnly looking at paths with a count more than: " + str(cutOff)
    count = 0
    for a in l:
        average = ll[count] / int(a.__len__())
        average = round(average, 1)
        s = s + "\n" + llNames[count] + str(average)
        s = s + "\n\t" + llexamples[count]
        count += 1

    return s

def regionPathCountAnalysis(cutOff: int, regions: list):
    '''to keep track of the counts per weekday'''
    weekdays = {}
    weekdayTotal = 0

    '''to keep track of the times'''
    justTimes = {}
    justTimeTotal = 0

    ''''to keep track of the paths'''
    justPaths = {}
    pathTotal = 0

    '''to keep track of the times per weekday'''
    weekdayTimes = {}
    weekdayTimeTotal = 0

    '''weekdays and paths'''
    weekdayPaths = {}
    weekdayPathTotal = 0

    '''time of day and paths'''
    timePaths = {}
    timePathTotal = 0

    '''all three'''
    weekdayHourPaths = {}
    weekdayHourPathTotal = 0

    '''list to hold all dicts'''
    l = []
    l.append(weekdays)
    l.append(justTimes)
    l.append(justPaths)
    l.append(weekdayTimes)
    l.append(weekdayPaths)
    l.append(timePaths)
    l.append(weekdayHourPaths)

    '''collect the counts for each path'''
    for region in regions:

        times = region.getTimes()

        for t in times.values():

            wkdy = t.getWeekDay()
            hour = t.getTimeID()

            paths = t.getPaths()

            for p in paths.values():

                path = p.getPathID()
                count = p.getCount()

                '''path'''
                if justPaths.__contains__(path):
                    justPaths[path] = justPaths[path] + int(count)
                else:
                    justPaths[path] = int(count)

    with open("RegionPathCounts.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for p in justPaths:
            a = [str(p), str(justPaths[p])]
            writer.writerow(a)
    csvfile.close()

    '''remove the paths that are not frequently used'''
    newPaths = justPaths.copy()
    for p in newPaths:
        if newPaths[p] < cutOff:
            del justPaths[p]

    '''update the other counts'''
    '''collect the counts for each path'''
    for region in ODNodes:

        times = region.getTimes()

        for t in times.values():

            wkdy = t.getWeekDay()
            hour = t.getTimeID()

            paths = t.getPaths()

            for p in paths.values():

                path = p.getPathID()
                count = p.getCount()

                '''if this path is one with a large enough count'''
                if path in justPaths.keys():

                    '''weekday'''
                    if weekdays.__contains__(wkdy):
                        weekdays[wkdy] = weekdays[wkdy] + int(count)
                    else:
                        weekdays[wkdy] = int(count)

                    '''hour'''
                    if justTimes.__contains__(hour):
                        justTimes[hour] = justTimes[hour] + int(count)
                    else:
                        justTimes[hour] = int(count)

                    '''weekday and hour'''
                    weekdayHour = str(wkdy) + " " + str(hour)
                    if weekdayTimes.__contains__(weekdayHour):
                        weekdayTimes[weekdayHour] = weekdayTimes[weekdayHour] + int(count)
                    else:
                        weekdayTimes[weekdayHour] = int(count)

                    '''weekday and path'''
                    weekdayPath = str(wkdy) + " " + str(path)
                    if weekdayPaths.__contains__(weekdayPath):
                        weekdayPaths[weekdayPath] = weekdayPaths[weekdayPath] + int(count)
                    else:
                        weekdayPaths[weekdayPath] = int(count)

                    '''hour and path'''
                    hourPath = str(hour) + " " + str(path)
                    if timePaths.__contains__(hourPath):
                        timePaths[hourPath] = timePaths[hourPath] + int(count)
                    else:
                        timePaths[hourPath] = int(count)

                    '''weekday and hour and path'''
                    weekdayHourPath = str(wkdy) + " " + str(hour) + " " + str(path)
                    if weekdayHourPaths.__contains__(weekdayHourPath):
                        weekdayHourPaths[weekdayHourPath] = weekdayHourPaths[weekdayHourPath] + int(count)
                    else:
                        weekdayHourPaths[weekdayHourPath] = int(count)

    for aa in weekdays.values():
        weekdayTotal += aa
    for aaa in timePaths.values():
        timePathTotal += aaa
    for aaaa in weekdayPaths.values():
        weekdayPathTotal += aaaa
    for aaaaa in weekdayTimes.values():
        weekdayTimeTotal += aaaaa
    for aaaaaa in justTimes.values():
        justTimeTotal += aaaaaa
    for aaaaaaa in justPaths.values():
        pathTotal += aaaaaaa
    for aaaaaaaa in weekdayHourPaths.values():
        weekdayHourPathTotal += aaaaaaaa

    '''list to hold all totals'''
    ll = []
    llNames = []
    llexamples = []
    ll.append(weekdayTotal)
    llNames.append("Average Weekday Total Path Count: ")
    llexamples.append("Example: Wednesday had 100 trips with map-able paths")
    ll.append(justTimeTotal)
    llNames.append("Average Time Segment Path Count: ")
    llexamples.append("Example: 08:00 had 100 trips with map-able paths")
    ll.append(pathTotal)
    llNames.append("Average Distinct Path Count: ")
    llexamples.append("Example: I-66 had 100 trips with map-able paths")
    ll.append(weekdayTimeTotal)
    llNames.append("Average Weekday Time Segment Path Count: ")
    llexamples.append("Example: Wednesday at 08:00 had 100 trips with map-able paths")
    ll.append(weekdayPathTotal)
    llNames.append("Average Weekday Distinct Path Count: ")
    llexamples.append("Example: I-66 on Wednesday had 100 trips with map-able paths")
    ll.append(timePathTotal)
    llNames.append("Average Time Segment on Distinct Path Path Count: ")
    llexamples.append("Example: I-66 on Wednesdays had 100 trips with map-able paths")
    ll.append(weekdayHourPathTotal)
    llNames.append("Average Distinct Path during Time Segment on Weekday Path Count: ")
    llexamples.append("Example: I-66 taken at 08:30 on Wednesdays had 100 trips with map-able paths")

    '''header'''
    s = "\n\n--- Path Count Analysis ---"
    s = s + "\nOnly looking at paths with a count more than: " + str(cutOff)
    count = 0
    for a in l:
        average = ll[count] / int(a.__len__())
        average = round(average, 1)
        s = s + "\n" + llNames[count] + str(average)
        s = s + "\n\t" + llexamples[count]
        count += 1

    return s

def NodeProportionAnalysis(total: int, AM: int, PM: int):
    '''total traffic analysis'''
    significantFactor = total
    expectedProportion = 1 / ODNodes.__len__()
    significantProportion = expectedProportion * significantFactor

    string = "\n\n--- ODNodes Holding " + str(significantFactor) + "x more of Expected Total Traffic---"
    string = string + "\n--- If 'Percent total interested trips' >= " + str(significantProportion)[:5] + " ---"

    counter = 0
    nodeString = ""
    totalProportion = 0

    for i in ODNodes:

        if (i.getCount() / odMapCount) >= significantProportion:
            totalProportion += (i.getCount() / odMapCount)

            nodeString = nodeString + "\n\n[" + str(counter) + "]"

            '''node information'''
            nodeString = nodeString + "\nOrigin     : " + i.origin.toString() + \
                         "\nDestination: " + i.destination.toString() + \
                         "\nODMapCount % (total): " + str(i.getCount() / odMapCount)[:5]

            counter += 1

    string = string + "\n---" + str(counter) + " OD Nodes Encompass " + str(totalProportion)[:5] + \
             " of all Interested Trips ---"
    # string = string + nodeString

    '''AM traffic analysis'''
    significantFactor = AM
    expectedProportion = 1 / ODNodes.__len__()
    significantProportion = expectedProportion * significantFactor

    string = string + "\n\n--- ODNodes Holding " + str(significantFactor) + "x more of Expected AM Traffic---"
    string = string + "\n--- If 'Percent AM trips' >= " + str(significantProportion)[:5] + " ---"

    counter = 0
    nodeString = ""
    totalProportion = 0

    for i in ODNodes:

        if (i.getAmCount() / totalAM) >= significantProportion:
            totalProportion += (i.getAmCount() / totalAM)

            nodeString = nodeString + "\n\n[" + str(counter) + "]"

            '''node information'''
            nodeString = nodeString + \
                         "\nOrigin     : " + i.origin.toString() + \
                         "\nDestination: " + i.destination.toString() + \
                         "\nInt Trips % (total): " + str(i.getCount() / interestTripCount)[:5] + \
                         "\nAM % (total)       : " + str(i.getAmCount() / totalAM)[:5]

            counter += 1

    string = string + "\n---" + str(counter) + " OD Nodes Encompass " + str(totalProportion)[:5] + \
             " of all AM Trips ---"
    # string = string + nodeString

    '''PM traffic analysis'''
    significantFactor = PM
    expectedProportion = 1 / ODNodes.__len__()
    significantProportion = expectedProportion * significantFactor

    string = string + "\n\n--- ODNodes Holding " + str(significantFactor) + "x more of Expected PM Traffic---"
    string = string + "\n--- If 'Percent PM trips' >= " + str(significantProportion)[:5] + " ---"

    counter = 0
    nodeString = ""
    totalProportion = 0

    for i in ODNodes:

        if (i.getPmCount() / totalPM) >= significantProportion:
            totalProportion += (i.getPmCount() / totalPM)

            nodeString = nodeString + "\n\n[" + str(counter) + "]"

            '''node information'''
            nodeString = nodeString + \
                         "\nOrigin     : " + i.origin.toString() + \
                         "\nDestination: " + i.destination.toString() + \
                         "\nInt Trips % (total): " + str(i.getCount() / interestTripCount)[:5] + \
                         "\nPM % (total)       : " + str(i.getPmCount() / totalPM)[:5]

            counter += 1

    string = string + "\n---" + str(counter) + " OD Nodes Encompass " + str(totalProportion)[:5] + \
             " of all PM Trips ---"

    return string

def createRegions(fileName: str):
    """

    :param fileName: name of the file that contains coordinates mapped to regions
    :return: a list of all possible regions
    """

    regions = []

    nova = {}
    dc = {}

    with open(fileName, 'r', newline='') as f:
        reader = csv.reader(f)

        for line in reader:

            district = str(line[2])

            if district.__contains__("NOVA"):
                nova[district] = 0
            if district.__contains__("DC"):
                dc[district] = 0
    f.close()

    for n in nova:
        for d in dc:
            inbound = ODRegion.ODRegion(n, d, True)
            regions.append(inbound)
    for d in dc:
        for n in nova:
            outbound = ODRegion.ODRegion(d, n, False)
            regions.append(outbound)

    for r in regions:
        r.createTimeIntervals("00:00", "23:59", 30)

    return regions

def matchCoordinates(fileName: str):

    matchedCoordinates = []

    try:
        with open(fileName, 'r', newline='') as file:
            reader = csv.reader(file)

            for l in reader:
                c = Coordinate.Coordinate(l[0], l[1])
                c.setDistrict(l[2])
                matchedCoordinates.append(c)

        file.close()

    except:
        print("Error opening file in matchCoordinates()")

    return matchedCoordinates

def attachRegions(nodes: list, coords: list):
    """

    :param nodes: a list of all the od nodes with all the data
    :return:
    """

    '''loop through all passed nodes'''
    for node in nodes:
        '''loop though all coordinates that are matched to regions'''
        for coor in coords:
            '''snap the region to the coordinates of the od node'''
            d = coor.getDistrict()
            if node.origin.equals(coor):
                node.origin.setDistrict(d)
            if node.destination.equals(coor):
                node.destination.setDistrict(d)


    nodesWithRegions = []

    for node in nodes:
        if node.origin.getDistrict() != "blank" and node.destination.getDistrict() != "blank":
            nodesWithRegions.append(node)

    return nodesWithRegions


def updateRegions(regions: list, nodes: list):

    for node in nodes:
        for r in regions:

            regionTimes = r.getTimes()

            if node.origin.getDistrict() == r.getOrigin():
                if node.destination.getDistrict() == r.getDestination():
                    '''update region'''
                    '''update the counts'''
                    r.setCount(r.getCount() + node.getCount())
                    r.setAMCount(r.getAmCount() + node.getAmCount())
                    r.setPMCount(r.getPmCount() + node.getPmCount())

                    '''update the time counts'''
                    nodeTimes = node.getTimes()
                    for t in nodeTimes:
                        nodeTimeNode = nodeTimes[t]
                        if regionTimes.__contains__(t):
                            regionTimeNode = regionTimes[t]

                            '''update the time count'''
                            regionTimeNode.setCount(regionTimeNode.getCount() + nodeTimeNode.getCount())

                            '''update the paths'''
                            nodeTimeNodePaths = nodeTimeNode.getPaths()
                            regionTimeNodePaths = regionTimeNode.getPaths()
                            for p in nodeTimeNodePaths:
                                nodeTimeNodePath = nodeTimeNodePaths[p]

                                if regionTimeNodePaths.__contains__(p):
                                    regionTimeNodePath = regionTimeNodePaths[p]

                                    regionTimeNodePath.setCount(regionTimeNodePath.getCount() + nodeTimeNodePath.getCount())

                                    regionTimeNodePaths[p] = regionTimeNodePath

                            regionTimes[t] = regionTimeNode

    return regions

def regionProportionAnalysis(regions: list, total: int, AM: int, PM: int):
    """

    :param regions: list of the regions
    :param total: the cut off for being interesting for the total count, if the region contains totalx times the
        expected count it is considered interesting
    :param AM: the cut off for being interesting for the am count, if the region contains totalx times the
        expected am count it is considered interesting
    :param PM: the cut off for being interesting for the pm count, if the region contains totalx times the
        expected pm count it is considered interesting
    :return: a string that describes the proportion deistribution
    """

    '''total traffic analysis'''
    significantFactor = total
    expectedProportion = 1 / regions.__len__()
    significantProportion = expectedProportion * significantFactor

    string = "\n\n--- Regions Holding " + str(significantFactor) + "x more of Expected Total Traffic---"
    string = string + "\n--- If 'Percent total interested trips' >= " + str(significantProportion)[:5] + " ---"

    counter = 0
    nodeString = ""
    totalProportion = 0

    for i in regions:

        if (i.getCount() / odMapCount) >= significantProportion:
            totalProportion += (i.getCount() / odMapCount)

            nodeString = nodeString + "\n\n[" + str(counter) + "]"

            '''node information'''
            nodeString = nodeString + "\nOrigin     : " + i.origin + \
                         "\nDestination: " + i.destination + \
                         "\nODMapCount % (total): " + str(i.getCount() / odMapCount)[:5]

            counter += 1

    string = string + "\n---" + str(counter) + " Regions Encompass " + str(totalProportion)[:5] + \
             " of all Interested Trips ---"
    # string = string + nodeString

    '''AM traffic analysis'''
    significantFactor = AM
    expectedProportion = 1 / regions.__len__()
    significantProportion = expectedProportion * significantFactor

    string = string + "\n\n--- Regions Holding " + str(significantFactor) + "x more of Expected AM Traffic---"
    string = string + "\n--- If 'Percent AM trips' >= " + str(significantProportion)[:5] + " ---"

    counter = 0
    nodeString = ""
    totalProportion = 0

    for i in regions:

        if (i.getAmCount() / totalAM) >= significantProportion:
            totalProportion += (i.getAmCount() / totalAM)

            nodeString = nodeString + "\n\n[" + str(counter) + "]"

            '''node information'''
            nodeString = nodeString + \
                         "\nOrigin     : " + i.origin + \
                         "\nDestination: " + i.destination + \
                         "\nInt Trips % (total): " + str(i.getCount() / interestTripCount)[:5] + \
                         "\nAM % (total)       : " + str(i.getAmCount() / totalAM)[:5]

            counter += 1

    string = string + "\n---" + str(counter) + " Regions Encompass " + str(totalProportion)[:5] + \
             " of all AM Trips ---"
    # string = string + nodeString

    '''PM traffic analysis'''
    significantFactor = PM
    expectedProportion = 1 / regions.__len__()
    significantProportion = expectedProportion * significantFactor

    string = string + "\n\n--- Regions Holding " + str(significantFactor) + "x more of Expected PM Traffic---"
    string = string + "\n--- If 'Percent PM trips' >= " + str(significantProportion)[:5] + " ---"

    counter = 0
    nodeString = ""
    totalProportion = 0

    for i in regions:

        if (i.getPmCount() / totalPM) >= significantProportion:
            totalProportion += (i.getPmCount() / totalPM)

            nodeString = nodeString + "\n\n[" + str(counter) + "]"

            '''node information'''
            nodeString = nodeString + \
                         "\nOrigin     : " + i.origin + \
                         "\nDestination: " + i.destination + \
                         "\nInt Trips % (total): " + str(i.getCount() / interestTripCount)[:5] + \
                         "\nPM % (total)       : " + str(i.getPmCount() / totalPM)[:5]

            counter += 1

    string = string + "\n---" + str(counter) + " Regions Encompass " + str(totalProportion)[:5] + \
             " of all PM Trips ---"


    return string

def regionPercentAnalysis(regions: list):
    regionMapCount = 0
    regionTimeMapCount = 0
    regionPathMapCount = 0

    for r in regions:
        regionMapCount += r.getCount()

        times = r.getTimes()
        for t in times:
            t = times[t]
            regionTimeMapCount += t.getCount()

            paths = t.getPaths()

            for p in paths:
                pathNode = paths[p]

                regionPathMapCount += pathNode.getCount()

    s = "\n\n--- Region Percent Analysis ---"
    s = s + "\nOD Trips Map to Region : " + str(regionMapCount / odMapCount)[:5]
    s = s + "\nRegion Trips Map to Time: " + str(regionTimeMapCount / regionMapCount)[:5]
    s = s + "\nTime Mapped to Path : " + str(regionPathMapCount / regionTimeMapCount)[:5]
    s = s + "\nEnd Amount Mapped   : " + str(regionPathMapCount / totalTripCount)[:5]

    return s



def graphRegionCounts(regions: list):

    # the regions sorted based on counts, highest count first
    totalCountSorted = sorted(regions, key=lambda x: x.count, reverse=True)
    amCountSorted = sorted(regions, key=lambda x: x.amCount, reverse=True)
    pmCountSorted = sorted(regions, key=lambda x: x.pmCount, reverse=True)

    count = 0
    x1 = []
    y1 = []
    for i in totalCountSorted:
        count += 1
        x1.append(count)
        y1.append(i.getCount())
    # plotting the points
    plt.plot(x1, y1, label="Total Count")

    count = 0
    x2 = []
    y2 = []
    for i in amCountSorted:
        count += 1
        x2.append(count)
        y2.append(i.getAmCount())
    # plotting the points
    plt.plot(x2, y2, label="AM Count")

    count = 0
    x3 = []
    y3 = []
    for i in pmCountSorted:
        count += 1
        x3.append(count)
        y3.append(i.getPmCount())
    # plotting the points
    plt.plot(x3, y3, label="PM Count")

    # naming the x axis
    plt.xlabel('rank')
    # naming the y axis
    plt.ylabel('count')
    # give the graph a  legend
    plt.legend()
    # giving a title to my graph
    plt.title('Regions By Count')

    # function to show the plot
    plt.show()
    plt.savefig("RegionsByCount.png")

def graphEncompassed(regions: list):
    # the regions sorted based on counts, highest count first
    totalCountSorted = sorted(regions, key=lambda x: x.count, reverse=True)
    amCountSorted = sorted(regions, key=lambda x: x.amCount, reverse=True)
    pmCountSorted = sorted(regions, key=lambda x: x.pmCount, reverse=True)

    count = 0
    sumSeen = 0
    x1 = []
    y1 = []
    for i in totalCountSorted:
        count += 1
        x1.append(count)

        sumSeen += i.getCount()
        y1.append(sumSeen / interestTripCount)

    # plotting the points
    plt.plot(x1, y1, label="Percentage Seen")

    # naming the x axis
    plt.xlabel('rank')
    # naming the y axis
    plt.ylabel('count')
    # give the graph a  legend
    plt.legend()
    # giving a title to my graph
    plt.title('Regions By Count')

    # function to show the plot
    plt.show()
    plt.savefig("RegionsByCount.png")


def setUpRegons(nodes: list):
    """

    :param nodes: list of od nodes that contain all the data
    :return: the counts for each region
    """

    matchedCoordinates = matchCoordinates("ActualGridToRegion.csv")
    end = time.time()

    # what regions are we working with
    regions = createRegions("ActualGridToRegion.csv")

    # attach regions to the coordinates of the od nodes
    nodesWithRegions = attachRegions(nodes, matchedCoordinates)

    # go through all the od nodes, and add its counts to the correct regions counts
    updatedRegions = updateRegions(regions, nodesWithRegions)

    return updatedRegions



# -----------------------------------------------------------analysis----------------------------

with open(outputFileName, 'w') as file:

    # the regions
    updatedRegions = setUpRegons(ODNodes)

    basic = basicInfo()

    nodePercent = nodePercentAnalysis()

    pathAnalysis = nodePathCountAnalysis(0)

    props = NodeProportionAnalysis(0, 0, 0)

    # proportion analysis on regions
    regionProportion = regionProportionAnalysis(updatedRegions, 3, 3, 3)

    # percent capture analysis
    regionPercent = regionPercentAnalysis(updatedRegions)

    # graphRegionCounts(updatedRegions)
    # graphEncompassed(updatedRegions)

    string = basic + nodePercent + regionPercent

    file.write(string)



file.close()

# end of file
