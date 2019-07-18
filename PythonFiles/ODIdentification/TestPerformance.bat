@ECHO OFF


rem Variables
set utc2017="C:\Users\JK\Google Drive\Non Acedemics\Occupational\VTRC\Python Files\ODIdentification\utc2017AllDay.csv"
set utc2018="C:\Users\JK\Google Drive\Non Acedemics\Occupational\VTRC\Python Files\ODIdentification\utc2018AllDay.csv"
set Zipper="C:\Program Files\7-Zip\7z.exe"
set Analyzer="C:\Users\JK\Google Drive\Non Acedemics\Occupational\VTRC\Python Files\ODIdentification\Main.py"
set DataOrigin=""
set printProgress="false"
set testPerformance="true"

py ClearOutput.py > output.txt
    del output.txt

for /L %%i in (1,1,50) do (

    rem execute the program
    rem echo Executing the Program...
    py %Analyzer% ShortDataTrip.csv %utc2017% AllXDInfo-17.csv OutputTest.csv totalOutputTest.txt %printProgress% %testPerformance% >> runs.txt
    rem echo Program Executed.
    )

rem write the performance to file
echo July 11 - 1110 >> performance.txt
echo Notes: Changed findTimeNode method in ODNode >> performance.txt
py averageRunTime.py >> performance.txt
echo. >> performance.txt

rem delete the file that stored the run times
del runs.txt

rem view the performance file
cat performance.txt


