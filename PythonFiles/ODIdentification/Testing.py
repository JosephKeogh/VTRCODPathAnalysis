from Objects import Coordinate
import csv

noRegion = []

with open("DCGrid.csv", 'r') as file:

    reader = csv.reader(file)

    count = 0
    for line in reader:
        if str(line[0]).__contains__("a") is False:
            c = Coordinate.Coordinate(float(line[0]), float(line[1]))
            noRegion.append(c)


file.close()

with open("NOVAGrid.csv", 'r') as file:
    reader = csv.reader(file)

    count = 0
    for line in reader:
        if str(line[0]).__contains__("a") is False:
            c = Coordinate.Coordinate(float(line[0]), float(line[1]))
            noRegion.append(c)

file.close()


yesRegion = []
yesRegionCount = 0
with open("GridToRegion.csv", 'r', newline='') as file:
    reader = csv.reader(file)

    count = 0
    for line in reader:
        if str(line[0]).__contains__("a") is False:
            c = Coordinate.Coordinate(float(line[0]), float(line[1]))
            yesRegion.append(c)
            yesRegionCount += 1

file.close()

found = 0
for a in yesRegion:

    for b in noRegion:

        tol = 8

        alat = float(str(a.getLat())[:tol])
        along = float(str(a.getLong())[:tol])
        blat = float(str(b.getLat())[:tol])
        blong = float(str(b.getLong())[:tol])

        if alat == blat:

            if along == blong:
                found += 1
                break

print("with region: " + str(yesRegion.__len__()))
print("found: " + str(found))
print("not found: " + str(yesRegion.__len__() - found))


# end of file

