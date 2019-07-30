from Objects import Coordinate, TimeNode, ODNode, PathNode, HashTable, Region
from datetime import datetime, timedelta
import sys
import csv
from pykml import parser

sys.argv.pop(0)                                 # ignore this program's name
inputFileName = sys.argv.pop(0)
outputFileName = sys.argv.pop(0)
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

def percentAnalysis():

    s = "\n\n--- Percent Analysis ---"
    s = s + "\nTrips of Interest % : " + str(interestTripCount / totalTripCount)[:5]
    s = s + "\nInt Trips Map to OD : " + str(odMapCount / interestTripCount)[:5]
    s = s + "\nOD Trips Map to Time: " + str(timeMapCount / odMapCount)[:5]
    s = s + "\nTime Mapped to Path : " + str(pathMapCount / timeMapCount)[:5]
    s = s + "\nEnd Amount Mapped   : " + str(pathMapCount / totalTripCount)[:5]

    return s

def pathCountAnalysis(cutOff: int):
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

    with open("PathCounts.csv", 'w', newline='') as csvfile:
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


def regionAnalysis(nodes: list):

    matched = []

    with open("ActualGridToRegion.csv", 'r', newline='') as f:
        reader = csv.reader(f)

        for line in reader:
            c = Coordinate.Coordinate(line[0], line[1])
            c.setDistrict(line[2])
            matched.append(c)
    f.close()

    regions = []

    for a in matched:

        for b in matched:

            aD = a.getDistrict()
            bD = b.getDistrict()

            if aD.__contains__("NOVA") is True and bD.__contains__("Nova") is False:

                region = Region.Region(aD, bD)

            if aD.__contains__("DC") is True and bD.__contains__("DC") is False:
                region = "From: " + aD + " To: " + bD
                if regions.__contains__(region) is False:
                    regions[region] = 0

    for node in nodes:
        origin = node.origin
        dest = node.destination
        inBound = node.getInbound()

        if inBound is True:
            for m in matched:


        if inBound is False:



    s = ""

    return s


# -----------------------------------------------------------analysis----------------------------

with open(outputFileName, 'w') as file:

    basic = basicInfo()

    percent = percentAnalysis()

    pathAnalysis = pathCountAnalysis(0)

    props = NodeProportionAnalysis(0, 0, 0)

    region = regionAnalysis()

    # string = basic + percent + pathAnalysis + props
    string = region

    file.write(string)

file.close()

# end of file
