# Скрипт для запуска сервера PriceForecastingSystem

Write-Host "🔍 Проверка запущенных процессов сервера..." -ForegroundColor Yellow

# Проверяем запущенные процессы
$runningProcesses = Get-Process | Where-Object { $_.ProcessName -like "*PriceForecasting*" } 2>$null

if ($runningProcesses) {
    Write-Host "⚠️ Найдены запущенные процессы сервера. Завершаю..." -ForegroundColor Red
    foreach ($process in $runningProcesses) {
        Stop-Process -Id $process.Id -Force
        Write-Host "✅ Завершен процесс $($process.Id)" -ForegroundColor Green
    }
    Start-Sleep -Seconds 2
}

# Проверяем порт 5229
$portInUse = netstat -ano | findstr ":5229" 2>$null
if ($portInUse) {
    $processId = ($portInUse -split '\s+')[-1]
    if ($processId -and $processId -ne "0") {
        Write-Host "⚠️ Порт 5229 занят процессом $processId. Завершаю..." -ForegroundColor Red
        Stop-Process -Id $processId -Force 2>$null
        Write-Host "✅ Процесс $processId завершен" -ForegroundColor Green
    }
    Start-Sleep -Seconds 1
}

Write-Host "🚀 Запуск сервера PriceForecastingSystem..." -ForegroundColor Green

# Переходим в директорию API
$apiPath = Join-Path $PSScriptRoot "PriceForecasting.API\PriceForecasting.API"
Set-Location $apiPath

# Запускаем сервер
dotnet run

Write-Host "🎯 Сервер запущен! Доступные адреса:" -ForegroundColor Green
Write-Host "  📊 Swagger UI: http://localhost:5229/swagger" -ForegroundColor Cyan
Write-Host "  🎨 Docs демо: file://$PSScriptRoot/docs/index.html" -ForegroundColor Cyan
Write-Host "  💼 Frontend: file://$PSScriptRoot/PriceForecasting.Frontend/index.html" -ForegroundColor Cyan
