import math
from Objects import Coordinate
import csv

# main --------------------------------------------------------------------

# create a list of OD's, maybe a hashtable
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
TLDcLat = 39.03431
TLDcLong = -77.221
TLDcCoor = Coordinate.Coordinate(TLDcLat, TLDcLong)
dcSize = 32.1869
dcNum = int(dcSize / 4.82)
dcGrid = TLDcCoor.createGrid(dcSize, dcNum)

with open("ODNodes.txt", 'w') as file:
    # writer = csv.writer(file)
    # writer.writerow(["ID", "Type", "CenterLat", "CenterLong", "Radius"])
    file.write("ID, Type, CenterLat, CenterLong\n")
    # file.write("CenterLat, CenterLong" + "\n")

    IDCount = 0

    for o in novaGrid:
        # writer.writerow([IDCount, "O", o.lat, o.long, originClose])
        # writer.writerow([o.lat, o.long])
        file.write(str(IDCount) + "," + "NOVA" + "," + str(o.lat) + "," + str(o.long) + "\n")
        # file.write(str(o.lat) + "," + str(o.long) + "\n")

        IDCount += 1

    for d in dcGrid:
        # writer.writerow([IDCount, "D", d.lat, d.long, destClose])
        # writer.writerow([d.lat, d.long])
        file.write(str(IDCount) + "," + "DC" + "," + str(d.lat) + "," + str(d.long) + "\n")
        # file.write(str(d.lat) + "," + str(d.long) + "\n")

        IDCount += 1

file.close()

with open("TableauInput.csv", 'w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(["Latitude", "Longitude", "Zone"])

    for anode in dcGrid:
        writer.writerow([anode.getLat(), anode.getLong(), "DC"])


file.close()


# end of file
