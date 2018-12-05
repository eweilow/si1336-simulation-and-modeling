@echo off

mkdir .\dist\

SET PGI_ACC_TIME=1
SET OUTPUT=".\dist\build.exe"
SET PGCC="pgcc"
SET BUILDCOMMAND=%PGCC% -o=%OUTPUT% -acc -ta=multicore -fast -Minfo=accel -Mprof=ccff main.c
echo.
echo Removing existing build
del %OUTPUT%
echo.
echo Building '%BUILDCOMMAND%'
%BUILDCOMMAND%
echo.
echo Starting...
%OUTPUT%