@ECHO OFF


rem Variables
rem these are the files that contain the dates of interest
set utc2017="C:\Users\JK\Google Drive\Non Acedemics\Occupational\VTRC\Python Files\ODIdentification\utc2017AllDay.csv"
set utc2018="C:\Users\JK\Google Drive\Non Acedemics\Occupational\VTRC\Python Files\ODIdentification\utc2018AllDay.csv"

rem this is what you use to unzip the csv files
set Zipper="C:\Program Files\7-Zip\7z.exe"

rem this is the program that will analyze the trip data
set Analyzer="C:\Users\JK\Google Drive\Non Acedemics\Occupational\VTRC\Python Files\ODIdentification\Main.py"

rem this control the output of the file
set printProgress="true"
set testPerformance="false"

setlocal enableextensions enabledelayedexpansion
set counter17=0
set counter18=0

rem clear the output file
echo Clearing the Output files...
py "C:/Users/JK/Google Drive/Non Acedemics/Occupational/VTRC/Python Files/ODIdentification/ClearOutput.py"
echo Output Files Cleared.
echo.

rem Loop over every 2017 file
echo Looping over 2017 files...
rem the location is a folder that contains the zipped csv files
for %%i in (C:\Users\JK\Desktop\InrixData\Trips\2017\unzipped\*.gz) do (

    rem keep track of file progression
    set /a counter17+=1
    echo 2017: !counter17!

    rem unzip the data
    echo unzipping the data...
    %Zipper% e %%i > null
    del null
    echo Data Unzipped.

    rem rename the file
    ren trips.csv* data.csv
    echo Unzipped file renamed.

    rem execute the program
    echo Executing the Program...
    py %Analyzer% data.csv %utc2017% AllXDInfo-17.csv Output2017.csv totalOutput2017.txt %printProgress% %testPerformance%
    echo Program Executed.

    rem delete the unzipped file
    del data.csv
    echo Unzipped file deleted.
    echo.
)
echo Looping over 2017 files done.
echo.

rem Loop over every 2018 file
echo Looping over 2018 files...
rem the location is where all the zipped 2018 data files are
for %%i in (C:\Users\JK\Desktop\InrixData\Trips\2018\unzipped\*.gz) do (

    rem keep track of file progression
    set /a counter18+=1
    echo 2018: !counter18!

    rem unzip the data
    echo unzipping the data...
    %Zipper% e %%i > null
    del null
    echo Data Unzipped.

    rem rename the file
    ren trips.csv* data.csv
    echo Unzipped file renamed.

    rem execute the program
    echo Executing the Program...
    py %Analyzer% data.csv %utc2018% totalOutput2018.txt %printProgress% %testPerformance%
    echo Program Executed.

    rem delete the unzipped file
    del data.csv
    echo Unzipped file deleted.
    echo.
)
echo Looping over 2018 files done.
echo.

echo Doing Analysis...
Analyze.bat
echo Analysis Finished.
echo.

echo Program Complete, Good Job


