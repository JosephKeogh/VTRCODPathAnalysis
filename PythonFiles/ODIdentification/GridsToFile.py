import math
from Objects import Coordinate

# main --------------------------------------------------------------------

# create a list of OD's, maybe a hashtable
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


# end of file
