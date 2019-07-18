import csv

'''clear all the output files'''
for i in range(0, 6):

    i = str(i)

    fileName = "totalOutput2017" + i + ".txt"

    with open(fileName, 'w') as file:
        file.write("Total Trips: " + str(0))
        file.write("\nInt Trips  : " + str(0))
        file.write("\nOD Maps    : " + str(0))
        file.write("\nTime Maps  : " + str(0))
        file.write("\nPath Maps  : " + str(0))
    file.close()

    fileName = "totalOutput2018" + i + ".txt"
    with open(fileName, 'w') as file:
        file.write("Total Trips: " + str(0))
        file.write("\nInt Trips  : " + str(0))
        file.write("\nOD Maps    : " + str(0))
        file.write("\nTime Maps  : " + str(0))
        file.write("\nPath Maps  : " + str(0))
    file.close()

with open("totalOutputTest.txt", 'w') as file:
    '''write the header'''
    file.write("Total Trips: " + str(0))
    file.write("\nInt Trips  : " + str(0))
    file.write("\nOD Maps    : " + str(0))
    file.write("\nTime Maps  : " + str(0))
    file.write("\nPath Maps  : " + str(0))
file.close()

print('Done Clearing Files')





