# Define la URL de descarga de Python 3.11
$pythonInstallerUrl = "https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe"
$installerPath = "$env:TEMP\python-3.11.0-amd64.exe"

# Descarga el instalador
Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $installerPath

# Instala Python sin necesidad de intervención del usuario
Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait

# Verifica la instalación
python --version

# Instala pip (normalmente se instala con Python, pero por si acaso)
python -m ensurepip

# Verifica la instalación de pip
pip --version

# Instala las dependencias
pip install -r requirements.txt

# Limpieza
Remove-Item $installerPath
