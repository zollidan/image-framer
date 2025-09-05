$backendEnv = "./backend/.env"
$frontendEnv = "./frontend/.env"
$dockerEnv   = "./.env"

$envFiles = @($backendEnv, $frontendEnv, $dockerEnv)

Write-Host "🔍 Проверка .env файлов..."

$missing = @()
foreach ($file in $envFiles) {
    if (-Not (Test-Path -Path $file)) {
        $missing += $file
    }
}

if ($missing.Count -gt 0) {
    Write-Host "⚠️ Отсутствуют следующие файлы:"
    $missing | ForEach-Object { Write-Host "   - $_" }
    exit 1
} else {
    Write-Host "✅ Все необходимые .env файлы найдены."
}

$composeFile = "docker-compose.build-images.yml"
$composeCmd  = "docker-compose -f $composeFile build"

param(
    [switch]$Clean
)

if ($Clean) {
    $composeCmd += " --push --no-cache"
} else {
    $composeCmd += " --push"
}

Write-Host "🚀 Запуск сборки: $composeCmd"
Invoke-Expression $composeCmd -ErrorAction Stop

if ($LASTEXITCODE -eq 0) {
    Write-Host "🎉 Сборка успешно завершена!"
} else {
    Write-Host "❌ Ошибка при сборке. Код: $LASTEXITCODE"
    exit $LASTEXITCODE
}
