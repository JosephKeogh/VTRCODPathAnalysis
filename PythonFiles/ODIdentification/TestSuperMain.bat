@ECHO OFF


rem Variables
set utc2017="C:\Users\JK\Google Drive\Non Acedemics\Occupational\VTRC\Python Files\ODIdentification\utc2017AllDay.csv"
set utc2018="C:\Users\JK\Google Drive\Non Acedemics\Occupational\VTRC\Python Files\ODIdentification\utc2018AllDay.csv"
set Zipper="C:\Program Files\7-Zip\7z.exe"
set Analyzer="C:\Users\JK\Google Drive\Non Acedemics\Occupational\VTRC\Python Files\ODIdentification\Main.py"
set DataOrigin=""
set printProgress="false"
set testPerformance="false"

py ClearOutput.py

rem execute the program
rem echo Executing the Program...
py %Analyzer% ShortDataTrip.csv %utc2017% AllXDInfo-17.csv OutputTest.csv totalOutputTest.txt %printProgress% %testPerformance%

rem totaloutputtest.txt

rem py %Analyzer% ShortDataTrip.csv %utc2017% AllXDInfo-17.csv OutputTest.csv totalOutputTest.txt %printProgress% %testPerformance%

rem totaloutputtest.txt

rem echo Program Executed.

rem py Testing.py

rem py AnalyzeOutput.py totalOutputTest.txt analysis.txt

rem totalOutputTest.txt

rem analysis.txt

echo.



