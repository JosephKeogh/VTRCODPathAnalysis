!#bin/bash

cd

cd git/V*/P*/OD*

# variables
17=/scratch/jgk7uf/*17
18=/scratch/jgk7uf/*18

# copy the slurm request
cp request.slurm 17
cp request.slurm 18

# copy the super main shell program
cp SuperMain.sh 17
cp SuperMain.sh 18

# copy the date time file
cp utc2017AllDay.csv 17
cp utc2018AllDay.csv 18

# copy the trips files
cp tripsDetected.csv 17
cp tripsDetected.csv 18
cp 'tripsDetected (1).csv' 17
cp 'tripsDetected (1).csv' 18

# copy Main.py
cp Main.py 17
cp Main.py 18

# copy the appropriate output files
cp totalOutput2017-*.txt 17
cp totalOutput2018-*.txt 18

# copy the combine program
cp Combine.py 17
cp Combine.py 18

# copy the combined output file
cp finalOutput2017.txt 17
cp finalOutput2018.txt 18

# copy the analyzer
cp AnalyzeOutput.py 17
cp AnalyzeOutput.py 18

# copy the analysis file
cp analysis2017.txt 17
cp analysis2018.txt 18



