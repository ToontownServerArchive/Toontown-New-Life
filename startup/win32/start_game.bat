@echo off

echo Pick a connectiom method
echo.
echo #1 - Localhost
echo #2 - Public Server
echo.

:selection

set INPUT=-1
set /P INPUT=Selection: 

if %INPUT%==1 (
    echo.
    set TT_GAMESERVER=72.230.96.74
) else if %INPUT%==2 (
  echo.
  set TT_GAMESERVER=gs2.toontownjourney.com
)

set /P TT_PLAYCOOKIE="Username: "

cd ../../

set /P PPYTHON_PATH=<PPYTHON_PATH
echo ===============================
echo Starting Toontown Project Altis...
echo ppython: %PPYTHON_PATH%
echo Username: %TT_PLAYCOOKIE%
echo Gameserver: %TT_GAMESERVER%
echo ===============================

:goto
%PPYTHON_PATH% -m toontown.toonbase.ClientStart
pause
goto :goto
