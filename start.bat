@echo off
REM One-click start for Windows
cd %~dp0

where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
	echo Docker is not installed.
	echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop/
	pause
	exit /b 1
)

where docker-compose >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
	echo Docker Compose is not installed or not in PATH.
	echo Please install Docker Desktop (includes Compose) from https://www.docker.com/products/docker-desktop/
	pause
	exit /b 1
)

start http://localhost:8080
call docker-compose up --build
pause
