import csv
import sys


sys.argv.pop(0)
inputFileName = sys.argv.pop(0)

'''short months'''
shortMonths = [4, 6, 9, 11]
'''long months'''
longMonths = [1, 3, 5, 7, 8, 10, 12]
'''2017 datetimes'''
dates2017 = []

with open(inputFileName, 'r', newline='') as file17:
    reader = csv.reader(file17)

    for line in reader:

        newStartDateTime = ""
        newEndDateTime = ""

        if line[0].__contains__("10:30"):

            '''start info'''
            newStartDateTime = line[0][:11] + "05:00"

            '''end info'''
            '''old'''
            oldEndMonthInt = int(line[1][5:7])
            oldEndDayInt = int(line[1][8:10])

            '''update end date'''
            newEndDayInt = oldEndDayInt + 1
            newEndMonthInt = oldEndMonthInt

            '''update end month'''
            if newEndDayInt >= 31:

                '''if we are in a long month'''
                if longMonths.__contains__(oldEndMonthInt):
                    if newEndDayInt == 32:
                        newEndDayInt = 1
                        newEndMonthInt += 1

                '''if we are in a short month'''
                if shortMonths.__contains__(oldEndMonthInt):
                    if newEndDayInt == 31:
                        newEndDayInt = 1
                        newEndMonthInt += 1

            newEndDateTime = line[1][:4] + "-" + str(newEndMonthInt) + "-" + str(newEndDayInt) + "T" + "04:59"

        if line[0].__contains__("09:30"):
            '''start info'''
            newStartDateTime = line[0][:11] + "04:00"

            '''end info'''
            '''old'''
            oldEndMonthInt = int(line[1][5:7])
            oldEndDayInt = int(line[1][8:10])

            '''update end time'''
            newEndTime = line[1][7:11] + "03:59"

            '''update end date'''
            newEndDayInt = oldEndDayInt + 1
            newEndMonthInt = oldEndMonthInt

            '''update end month'''
            if newEndDayInt >= 31:

                '''if we are in a long month'''
                if longMonths.__contains__(oldEndMonthInt):
                    if newEndDayInt == 32:
                        newEndDayInt = 1
                        newEndMonthInt += 1

                '''if we are in a short month'''
                if shortMonths.__contains__(oldEndMonthInt):
                    if newEndDayInt == 31:
                        newEndDayInt = 1
                        newEndMonthInt += 1

            newEndDateTime = line[1][:4] + "-" + str(newEndMonthInt) + "-" + str(newEndDayInt) + "T" + "03:59"

        combo = []

        if newStartDateTime != '' and newEndDateTime != '':
            combo.append(newStartDateTime)
            combo.append(newEndDateTime)
            dates2017.append(combo)

file17.close()

newFileName = inputFileName[:7] + "AllDay.csv"
with open(newFileName, 'w', newline='') as output:
    writer = csv.writer(output)
    writer.writerow(["Start datetime utc", "End datetime utc"])
    writer.writerows(dates2017)
output.close()


# end of file
