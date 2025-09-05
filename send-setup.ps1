param(
    [Parameter(Mandatory=$true)]
    [string]$RemoteHost,
    
    [Parameter(Mandatory=$true)]
    [string]$Username,
    
    [Parameter(Mandatory=$false)]
    [string]$SshKeyPath = "$env:USERPROFILE\.ssh\id_ed25519"
)

# Проверка существования файлов установки
$setupFiles = @(
    "setup.sh",
    "setup-app.sh"
)

foreach ($file in $setupFiles) {
    if (-not (Test-Path $file)) {
        Write-Error "Файл $file не найден!"
        exit 1
    }
}

# Создание временной директории для файлов
$tempDir = "setup-files"
if (Test-Path $tempDir) {
    Remove-Item -Path $tempDir -Recurse -Force
}
New-Item -ItemType Directory -Path $tempDir | Out-Null

# Копирование файлов во временную директорию
foreach ($file in $setupFiles) {
    Copy-Item $file $tempDir
}

# Отправка файлов на удаленный сервер
Write-Host "Отправка файлов на $RemoteHost..."
$sshArgs = "-i", $SshKeyPath

# Отправка файлов
scp @sshArgs -r $tempDir/* "$($Username)@$($RemoteHost):~/"

# Установка прав на выполнение для скриптов
ssh @sshArgs "$($Username)@$($RemoteHost)" "chmod +x ~/*.sh"

Write-Host "Файлы успешно отправлены в ~/"
Write-Host "Для установки Docker и зависимостей выполните:"
Write-Host "./setup.sh"
Write-Host ""
Write-Host "Выполните установку приложения:"
Write-Host "export MY_DOMAIN=your-domain.com"
Write-Host "export REGISTER_ID=your-register-id"
Write-Host "export OAUTHTOKEN=token"
Write-Host "./setup-app.sh"

# Очистка временной директории
Remove-Item -Path $tempDir -Recurse -Force
