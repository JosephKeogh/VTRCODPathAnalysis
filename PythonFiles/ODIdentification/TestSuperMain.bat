@ECHO OFF


rem Variables
set utc2017="C:\Users\JK\Google Drive\Non Acedemics\Occupational\VTRC\Python Files\ODIdentification\utc2017AllDay.csv"
set utc2018="C:\Users\JK\Google Drive\Non Acedemics\Occupational\VTRC\Python Files\ODIdentification\utc2018AllDay.csv"
set Zipper="C:\Program Files\7-Zip\7z.exe"
set Analyzer="C:\Users\JK\Google Drive\Non Acedemics\Occupational\VTRC\Python Files\ODIdentification\Main.py"
set DataOrigin=""
set printProgress="true"
set testPerformance="false"

py ClearOutput.py

py Main.py ShortDataTrip %utc2017% totalOutputTest %printProgress% %testPerformance% 0

notepad totaloutputtest-0.txt

py AnalyzeOutput.py totalOutputTest-0.txt analysistest.txt

notepad analysistest.txt

echo.



