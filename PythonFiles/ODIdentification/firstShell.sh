#!/bin/bash

# clear the module, then load python
module purge
module load anaconda

# get into the correct directory
cd PythonFiles/ODIdentification/

# variables moving forward
printProgress=true
testPerformance=false

# clear the output files
python ClearOutput.py

# analyze the data
python Main.py ShortDataTrip.csv utc2017AllDay.csv AllXDInfo-17.csv OutputTest.csv totalOutputTest.txt $printProgress $testPerformance

# view the output of the analysis
# more totalOutputTest.txt
