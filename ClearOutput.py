import csv

with open("totalOutput2017.txt", 'w') as file:
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

with open("totalOutput2018.txt", 'w') as file:
    file.write("Total Trips: " + str(0))
    file.write("\nInt Trips  : " + str(0))
    file.write("\nOD Maps    : " + str(0))
    file.write("\nTime Maps  : " + str(0))
    file.write("\nPath Maps  : " + str(0))
file.close()

with open("OutputTest.csv", 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
csvFile.close()

with open("Output2017.csv", 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
csvFile.close()

with open("Output2018.csv", 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
csvFile.close()

print('Done Clearing Files')





