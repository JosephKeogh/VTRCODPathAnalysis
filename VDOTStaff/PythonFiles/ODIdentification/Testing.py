import csv
from Objects import Coordinate

coords = []



with open("ActualGridToRegion.csv", 'r', newline='') as file:
    reader = csv.reader(file)

    for line in reader:

        c = Coordinate.Coordinate(line[0], line[1])
        coords.append(c)
file.close()

over = 0
for a in coords:
    count = 0
    for b in coords:
        if a.equals(b):
            count += 1
    if count >= 2:
        over += 1

        with open("ActualGridToRegion.csv", 'r', newline='') as file:
            reader = csv.reader(file)

            lineCounter = 0

            for line in reader:
                lineCounter += 1
                c = Coordinate.Coordinate(line[0], line[1])
                coords.append(c)

                if c.equals(a):
                    print(lineCounter)
                    print(a.toString())
                    print(c.toString())
        file.close()

print(coords.__len__())
print(over)



# end of file
