import os
import sys
import subprocess
import atexit

# Variables globales para el proceso de PowerShell
proceso_powershell = None

def cerrar_procesos():
    """Función para cerrar el proceso de PowerShell al finalizar el script."""
    global proceso_powershell

    if proceso_powershell:
        print("Cerrando el script de PowerShell...")
        proceso_powershell.terminate()

def iniciar_aplicacion():
    global proceso_powershell
    print("Iniciando aplicación...")  # Imprimir al inicio

    # Cambiar el directorio de trabajo si se está ejecutando como un ejecutable
    if hasattr(sys, '_MEIPASS'):
        ruta_base = sys._MEIPASS
        print(f"Ejecutando desde un ejecutable, ruta base: {ruta_base}")
    else:
        documents_folder = os.path.join(os.getenv('USERPROFILE'), 'Documents')
        ruta_base = os.path.join(documents_folder, "mi_app_temp")
        print(f"Ruta base establecida en: {ruta_base}")

    ruta_powershell = os.path.join(ruta_base, "main.ps1")
    print(f"Ruta del script de PowerShell: {ruta_powershell}")

    # Verificar si el archivo de PowerShell existe en la ruta especificada
    if not os.path.exists(ruta_powershell):
        print(f"Error: No se pudo encontrar el archivo {ruta_powershell}. Verifica que el archivo esté en la ubicación correcta.")
        input("Presiona Enter para salir...")
        sys.exit(1)

    try:
        # Iniciar el script de PowerShell con la política de ejecución adecuada
        print("Iniciando el script de PowerShell...")  # Imprimir antes de iniciar
        proceso_powershell = subprocess.Popen(
            ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", ruta_powershell, "-RutaBase", ruta_base],
            shell=True
        )
        print(f"Script de PowerShell iniciado con PID: {proceso_powershell.pid}")

        # Esperar a que el script de PowerShell termine
        proceso_powershell.wait()
        print("Script de PowerShell ha terminado.")

        # Verificar el código de salida del script de PowerShell
        if proceso_powershell.returncode == 0:
            print("El script de PowerShell se cerró correctamente.")
        else:
            print(f"Error: El script de PowerShell se cerró con código de error {proceso_powershell.returncode}.")
    except Exception as e:
        print(f"Error inesperado al iniciar el script de PowerShell: {e}")
    finally:
        cerrar_procesos()
    print("Aplicación finalizada.")  # Imprimir al final

# Configurar la salida para ejecutar el cierre de procesos
atexit.register(cerrar_procesos)

# Punto de entrada principal del script
if __name__ == "__main__":
    try:
        iniciar_aplicacion()
    except Exception as e:
        print(f"Error general en la aplicación: {e}")