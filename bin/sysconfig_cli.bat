@echo off
rem
rem Run the SysConfig command line tool
rem
set DIR=%~dp0

rem try to use standalone node, then CCS node, finally any node version available on the path
if exist "%DIR%nodejs\node.exe" (
    set NODE=%DIR%nodejs\node.exe
) else if exist "%DIR%..\..\tools\node\node.exe" (
    set NODE=%DIR%..\..\tools\node\node.exe
) else (
    set NODE=node
)

"%NODE%" "%DIR%dist\cli.js" %*
