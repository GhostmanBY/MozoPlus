param (
    [string]$RutaBase
)

# Variable para activar el modo de depuración
$debugMode = $true

# Función para imprimir mensajes de depuración
function Debug-Print {
    param (
        [string]$message
    )
    if ($debugMode) {
        Write-Host "DEBUG: $message"
    }
}

# Cambia el directorio de trabajo al directorio del script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir
Debug-Print "Directorio de trabajo cambiado a $scriptDir"

# Usar la ruta base proporcionada como argumento
if (-Not $RutaBase) {
    $documentsFolder = [System.IO.Path]::Combine($env:USERPROFILE, 'Documents')
    $RutaBase = [System.IO.Path]::Combine($documentsFolder, "mi_app_temp")
}

Debug-Print "Ruta base establecida en $RutaBase"

$rutaFront = [System.IO.Path]::Combine($RutaBase, "Front", "pc_front.py")
$rutaApi = [System.IO.Path]::Combine($RutaBase, "Back", "Api.py")

Debug-Print "Ruta del frontend: $rutaFront"
Debug-Print "Ruta de la API: $rutaApi"

# Verificar si los archivos existen
if (-Not (Test-Path $rutaFront)) {
    Write-Host "Error: No se pudo encontrar el archivo $rutaFront. Verifica que el archivo esté en la ubicación correcta."
    exit 1
}

if (-Not (Test-Path $rutaApi)) {
    Write-Host "Error: No se pudo encontrar el archivo $rutaApi. Verifica que el archivo esté en la ubicación correcta."
    exit 1
}

# Iniciar la API
Write-Host "Iniciando la API..."
try {
    $apiProcess = Start-Process -FilePath "python" -ArgumentList $rutaApi -PassThru -WindowStyle Hidden
    Debug-Print "API iniciada con PID: $($apiProcess.Id)"
} catch {
    Write-Host "Error al iniciar la API: $_"
    exit 1
}

# Iniciar el frontend
Write-Host "Iniciando la aplicación frontend..."
try {
    $frontProcess = Start-Process -FilePath "python" -ArgumentList $rutaFront -PassThru -WindowStyle Hidden
    Debug-Print "Frontend iniciado con PID: $($frontProcess.Id)"
} catch {
    Write-Host "Error al iniciar el frontend: $_"
    exit 1
}

# Esperar a que el frontend termine
try {
    $frontProcess.WaitForExit()
    Debug-Print "Frontend ha terminado con código de salida: $($frontProcess.ExitCode)"
} catch {
    Write-Host "Error al esperar el cierre del frontend: $_"
}

# Cuando el frontend termina, también cerramos la API
if ($frontProcess.ExitCode -eq 0) {
    Write-Host "La aplicación frontend se cerró correctamente."
} else {
    Write-Host "Error: La aplicación frontend se cerró con código de error $($frontProcess.ExitCode)."
}

# Cerrar la API
Write-Host "Cerrando la API..."
try {
    Stop-Process -Id $apiProcess.Id
    Debug-Print "API cerrada"
} catch {
    Write-Host "Error al cerrar la API: $_"
}

# Asegurarse de que el puerto 8000 esté cerrado
Write-Host "Asegurándose de que el puerto 8000 esté cerrado..."
try {
    $portProcess = netstat -ano | Select-String ":8000" | ForEach-Object { $_ -replace '\s+', ' ' } | ForEach-Object { $_.Split(' ')[-1] }
    if ($portProcess) {
        Stop-Process -Id $portProcess -Force
        Debug-Print "Proceso en el puerto 8000 cerrado"
    } else {
        Debug-Print "No se encontró ningún proceso en el puerto 8000"
    }
} catch {
    Write-Host "Error al cerrar el proceso en el puerto 8000: $_"
}

# Restablecer la configuración de IP
Write-Host "Restableciendo la configuración de IP..."
try {
    netsh int ip reset
    Debug-Print "Configuración de IP restablecida"
} catch {
    Write-Host "Error al restablecer la configuración de IP: $_"
}