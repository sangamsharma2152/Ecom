# E-Commerce Application Launcher
# Location: deployment\run.ps1

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "Starting E-Commerce Application..."
Write-Host ""

java -jar ecommerce.jar

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Error: Application failed to start"
    Write-Host "Please ensure Java JDK 11+ is installed"
    Read-Host "Press Enter to exit"
}
