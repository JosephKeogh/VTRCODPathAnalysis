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

with open("NovaGrid.csv", 'w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(["Latitude", "Longitude", "Zone"])

    for bnode in novaGrid:
        writer.writerow([bnode.getLat(), bnode.getLong(), "NOVA"])

file.close()

with open("DCGrid.csv", 'w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(["Latitude", "Longitude", "Zone"])

    for anode in dcGrid:
        writer.writerow([anode.getLat(), anode.getLong(), "DC"])


file.close()


# end of file
