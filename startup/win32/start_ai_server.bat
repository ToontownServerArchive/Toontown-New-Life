@echo off
cd ../../

rem Define some constants for our AI server:
set MAX_CHANNELS=999999
set STATESERVER=4002
set ASTRON_IP=127.0.0.1:7199
set EVENTLOGGER_IP=127.0.0.1:7197

rem Get the user input:
echo Don't Change district name from Test Canvas or it will show up in invasion api!
set /P DISTRICT_NAME="District name (DEFAULT: Test Canvas): " || ^
set DISTRICT_NAME=Test Canvas
set /P BASE_CHANNEL="Base channel (DEFAULT: 401000000): " || ^
set BASE_CHANNEL=401000000

set /P START_TIME="START TIME(DEFAULT : 6): " || ^
set START_TIME=6
title %DISTRICT_NAME%

set /P PPYTHON_PATH=<PPYTHON_PATH

echo ===============================
echo Starting Toontown Project Altis AI server...
echo ppython: %PPYTHON_PATH%
echo District name: %DISTRICT_NAME%
echo Base channel: %BASE_CHANNEL%
echo Max channels: %MAX_CHANNELS%
echo State Server: %STATESERVER%
echo Astron IP: %ASTRON_IP%
echo Event Logger IP: %EVENTLOGGER_IP%
echo ===============================

:main
%PPYTHON_PATH% -m toontown.ai.ServiceStart --base-channel %BASE_CHANNEL% ^
               --max-channels %MAX_CHANNELS% --stateserver %STATESERVER% ^
               --astron-ip %ASTRON_IP% --eventlogger-ip %EVENTLOGGER_IP% ^
               --district-name "%DISTRICT_NAME%" --start-time "%START_TIME%"
goto main