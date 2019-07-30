import csv

with open("DCGrid.csv", 'r') as file:

    reader = csv.reader(file)

    count = 0
    for line in reader:
        count += 1

    print(count)

file.close()

with open("NOVAGrid.csv", 'r') as file:
    reader = csv.reader(file)

    count = 0
    for line in reader:
        count += 1
    print(count)

file.close()

with open("GridToRegion.csv", 'r', newline='') as file:
    reader = csv.reader(file)

    count = 0
    for line in reader:
        count += 1
    print(count)

file.close()


# end of file

