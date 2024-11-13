param (
    [string]$RutaBase
)

# Variable para activar el modo de depuración
$debugMode = $true

# Ruta del archivo de log
$logFilePath = [System.IO.Path]::Combine($env:USERPROFILE, 'Documents', 'script_log.txt')

# Función para imprimir mensajes de depuración
function Debug-Print {
    param (
        [string]$message
    )
    if ($debugMode) {
        Write-Host "DEBUG: $message"
        Add-Content -Path $logFilePath -Value "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') DEBUG: $message"
    }
}

# Función para imprimir mensajes de error
function Write-ErrorMessage {
    param (
        [string]$message
    )
    Write-Host "ERROR: $message"
    Add-Content -Path $logFilePath -Value "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ERROR: $message"
}

# Cambia el directorio de trabajo al directorio del script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir
Debug-Print "Directorio de trabajo cambiado a $scriptDir"

# Usar la ruta base proporcionada como argumento
if (-Not $RutaBase) {
    $documentsFolder = [System.IO.Path]::Combine($env:USERPROFILE, 'Documents')
    $appTempPath = [System.IO.Path]::Combine($documentsFolder, "mi_app_temp")

    # Buscar el último directorio que comienza con "_MEI"
    $meiDir = Get-ChildItem -Path $appTempPath -Directory | Where-Object { $_.Name -like '_MEI*' } | Sort-Object CreationTime -Descending | Select-Object -First 1

    if (-Not $meiDir) {
        Write-ErrorMessage "No se encontró ningún directorio que comience con '_MEI' en $appTempPath."
        exit 1
    }

    $RutaBase = $meiDir.FullName
}

Debug-Print "Ruta base establecida en $RutaBase"

$rutaFront = [System.IO.Path]::Combine($RutaBase, "Front", "pc_front.py")
$rutaApi = [System.IO.Path]::Combine($RutaBase, "Back", "Api.py")

Debug-Print "Ruta del frontend: $rutaFront"
Debug-Print "Ruta de la API: $rutaApi"

# Verificar si los archivos existen
if (-Not (Test-Path $rutaFront)) {
    Write-ErrorMessage "No se pudo encontrar el archivo $rutaFront. Verifica que el archivo esté en la ubicación correcta."
    exit 1
}

if (-Not (Test-Path $rutaApi)) {
    Write-ErrorMessage "No se pudo encontrar el archivo $rutaApi. Verifica que el archivo esté en la ubicación correcta."
    exit 1
}

# Función para verificar si una biblioteca está instalada
function Is-PackageInstalled {
    param (
        [string]$packageName
    )
    try {
        $result = & python -c "import $packageName" 2>&1
        return -not $result
    } catch {
        return $false
    }
}

# Instalar bibliotecas desde requirements.txt solo si no están instaladas
Write-Host "Verificando e instalando bibliotecas necesarias..."
try {
    $requirementsPath = [System.IO.Path]::Combine($RutaBase, "requirements.txt")
    if (Test-Path $requirementsPath) {
        $requirements = Get-Content $requirementsPath
        foreach ($requirement in $requirements) {
            $packageName = $requirement.Split('==')[0]  # Obtener el nombre del paquete
            if (-not (Is-PackageInstalled $packageName)) {
                Write-Host "Instalando $packageName..."
                & python -m pip install $requirement
                Debug-Print "Biblioteca $packageName instalada."
            } else {
                Debug-Print "Biblioteca $packageName ya está instalada."
            }
        }
    } else {
        Write-ErrorMessage "No se encontró el archivo requirements.txt en $RutaBase."
    }
} catch {
    Write-ErrorMessage "Error al instalar las bibliotecas: $_"
}

# Verificar si falta alguna biblioteca
Write-Host "Verificando bibliotecas instaladas..."
try {
    $missingPackages = & python -m pip check
    if ($missingPackages) {
        Write-ErrorMessage "Faltan algunas bibliotecas o hay conflictos: $missingPackages"
    } else {
        Debug-Print "Todas las bibliotecas están correctamente instaladas."
    }
} catch {
    Write-ErrorMessage "Error al verificar las bibliotecas: $_"
}

# Iniciar la API
Write-Host "Iniciando la API..."
try {
    $apiProcess = Start-Process -FilePath "python" -ArgumentList $rutaApi -PassThru -WindowStyle Hidden
    Debug-Print "API iniciada con PID: $($apiProcess.Id)"
} catch {
    Write-ErrorMessage "Error al iniciar la API: $_"
    exit 1
}

# Iniciar el frontend
Write-Host "Iniciando la aplicación frontend..."
try {
    $frontProcess = Start-Process -FilePath "python" -ArgumentList $rutaFront -PassThru -WindowStyle Hidden
    Debug-Print "Frontend iniciado con PID: $($frontProcess.Id)"
} catch {
    Write-ErrorMessage "Error al iniciar el frontend: $_"
    exit 1
}

# Esperar a que el frontend termine
try {
    $frontProcess.WaitForExit()
    Debug-Print "Frontend ha terminado con código de salida: $($frontProcess.ExitCode)"
} catch {
    Write-ErrorMessage "Error al esperar el cierre del frontend: $_"
}

# Cuando el frontend termina, también cerramos la API
if ($frontProcess.ExitCode -eq 0) {
    Write-Host "La aplicación frontend se cerró correctamente."
    Debug-Print "Frontend se cerró correctamente"
} else {
    Write-Host "Error: La aplicación frontend se cerró con código de error $($frontProcess.ExitCode)."
    Debug-Print "Frontend se cerró con código de error $($frontProcess.ExitCode)"
}

# Cerrar la API
Write-Host "Cerrando la API..."
try {
    Stop-Process -Id $apiProcess.Id
    Debug-Print "API cerrada"
} catch {
    Write-ErrorMessage "Error al cerrar la API: $_"
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
    Write-ErrorMessage "Error al cerrar el proceso en el puerto 8000: $_"
}

# Restablecer la configuración de IP
Write-Host "Restableciendo la configuración de IP..."
try {
    netsh int ip reset
    Debug-Print "Configuración de IP restablecida"
} catch {
    Write-ErrorMessage "Error al restablecer la configuración de IP: $_"
}

# Eliminar todas las carpetas _MEI
Write-Host "Eliminando todas las carpetas _MEI..."
try {
    $meiDirs = Get-ChildItem -Path $appTempPath -Directory | Where-Object { $_.Name -like '_MEI*' }
    foreach ($dir in $meiDirs) {
        Remove-Item -Path $dir.FullName -Recurse -Force
        Debug-Print "Carpeta eliminada: $($dir.FullName)"
    }
    Write-Host "Todas las carpetas _MEI han sido eliminadas."
} catch {
    Write-ErrorMessage "Error al eliminar las carpetas _MEI: $_"
}