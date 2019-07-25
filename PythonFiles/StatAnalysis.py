import sys
import csv
from datetime import datetime
from Objects import Coordinate, ODNode, PathNode, TimeNode

'''global'''
timeInterval = 30


'''for 2017'''
total17AM = 0
total17PM = 0
ODNodes17 = []
with open("finalOutput2017.txt", 'r') as outputTextFile1:

    print("reading 17...")

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
            total17AM += int(vamCount)
            total17PM += int(vpmCount)

            '''create the od node'''
            vodnode = ODNode.ODNode(voriginC, vdestC, int(vcount))
            vodnode.createTimeIntervals("00:00", "24:00", timeInterval)

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
                ODNodes17.append(vodnode)

outputTextFile1.close()

'''for 2018'''
total18AM = 0
total18PM = 0
ODNodes18 = []
with open("finalOutput2018.txt", 'r') as outputTextFile1:

    print("reading 18...")

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
            total18AM += int(vamCount)
            total18PM += int(vpmCount)

            '''create the od node'''
            vodnode = ODNode.ODNode(voriginC, vdestC, int(vcount))
            vodnode.createTimeIntervals("00:00", "24:00", timeInterval)

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
                ODNodes18.append(vodnode)

outputTextFile1.close()

statOutput = []
short = []
statOutput.append(["Origin Lat", "Origin Long",
                   "Destination Lat", "Destination Long",
                   "DateTime" "Path",
                   "2017 Count", "2018 Count"])

print("working...")
for i in range(0, ODNodes17.__len__()):
    node17 = ODNodes17[i]
    node18 = ODNodes18[i]

    originEqual = node17.origin.__eq__(node18.origin)
    destEqual = node18.destination.__eq__(node18.destination)

    if originEqual is False and destEqual is False:
        print("od node problem")

    else:

        '''time nodes'''
        times17 = node17.getTimes()
        times18 = node18.getTimes()

        if times17.__len__() != times18.__len__():
            print("time node problem")

        else:

            for key in times17:

                '''the time nodes'''
                timeNode17 = times17[key]
                timeNode18 = times18[key]

                paths17 = timeNode17.getPaths()
                paths18 = timeNode18.getPaths()

                for p in paths17:
                    if paths18.__contains__(p) is False:
                        paths18[p] = PathNode.PathNode(p)
                for p in paths18:
                    if paths17.__contains__(p) is False:
                        paths17[p] = PathNode.PathNode(p)

                for p in paths17:

                    pathNode17 = paths17[p]
                    pathNode18 = paths18[p]

                    add = [
                            node17.origin.getLat(), node17.origin.getLong(),
                            node17.destination.getLat(), node17.destination.getLong(),
                            timeNode17.getTimeID() + str(timeNode17.getWeekDay()), pathNode17.getPathID(),
                            pathNode17.getCount(), pathNode18.getCount()
                           ]
                    statOutput.append(add)

                    if timeNode18.getCount() > 0 and timeNode17.getCount() > 0:

                        p1 = pathNode17.getCount() / timeNode17.getCount()
                        p2 = pathNode18.getCount() / timeNode18.getCount()

                        diff = p1 - p1
                        short.append([p1, p2])

for i in statOutput:
    print(i)

with open("stat.csv", 'w', newline='') as stat:

    writer = csv.writer(stat)

    writer.writerows(short)


stat.close()
# end of file
