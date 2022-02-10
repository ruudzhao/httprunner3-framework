@echo off
set yaml_dir=yaml
set testcases_dir=testcases
set empty_str=
set PACKAGE_DIR=%~dp0
echo %PACKAGE_DIR%
rem set REPORT_DIR=d:/temps
rem if NOT defined REPORT_DIR (set REPORT_DIR=d:/temps/reports)
if NOT defined REPORT_DIR (set REPORT_DIR=%cd%)
echo %REPORT_DIR%
rem pause
rem set pa=%cd%

if [%1] == [] goto BEGIN
if [%2] == [] goto ERROR
set yaml_dir=%1
set testcases_dir=%2

:BEGIN
python %PACKAGE_DIR%/httprunner3.py make -y=%yaml_dir% -t=%testcases_dir% -c -v
if [3%] NEQ [] goto END

if %ERRORLEVEL% == 0 ( pytest %testcases_dir% --html=%REPORT_DIR%/report.html --self-contained-html)

rem echo %ERRORLEVEL%

rem if %ERRORLEVEL% NEQ 0 goto END

:REPORT

set FLASK_APP=%PACKAGE_DIR%/httprunner3_report.py
set FLASK_ENV=development
set PATH=%PATH%;C:\"Program Files (x86)"\Google\Chrome\Application
rem set PATH=%PATH%;C:\"Program Files"\"internet explorer"
rem set PATH=%PATH%;C:\"Program Files (x86)""\"Internet Explorer"
start chrome.exe http://localhost:5000/
rem start iexplore.exe http://localhost:5000/
python -m flask run -p 5000

goto END

:ERROR
  echo *                                          *
  echo *                                          *
  echo *                                          *
  echo *   Usage:                                 *
  echo *       hrun3 yaml_dir testcases_dir       *
  echo *                                          *
  echo *                                          *
  echo *                                          *


:END
