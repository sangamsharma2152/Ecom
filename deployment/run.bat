@echo off
REM E-Commerce Application Launcher
REM Location: deployment\run.bat

cd /d "%~dp0"
echo Starting E-Commerce Application...
echo.

java -jar ecommerce.jar

if errorlevel 1 (
    echo.
    echo Error: Application failed to start
    echo Please ensure Java JDK 11+ is installed
    pause
)
