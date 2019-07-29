import csv


def repeat(string: str):

    roads = []

    while string.__contains__("---"):

        index = string.index("---")

        before = string[:index]
        after = string[index:]

        roads.append(before)

        string = after[3:]


for i in range(7, 9):

    fileName = "PathCounts201" + str(i) + ".csv"

    with open(fileName, 'r', newline='') as file:

        reader = csv.reader(file)

        for line in reader:

            path = str(line[0])

            if path.__contains__("---"):

                repeat(path)

    file.close()


# end of file

