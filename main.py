import subprocess
import sys
import os
import atexit
import signal

# Variables globales para los procesos
proceso_api = None
proceso_front = None

def cerrar_procesos():
    """Función para cerrar ambos procesos al finalizar el script."""
    global proceso_api, proceso_front

    if proceso_api:
        print("Cerrando la API...")
        proceso_api.terminate()  # Intenta cerrar el proceso suavemente
        proceso_api.wait()  # Espera a que el proceso termine

    if proceso_front:
        print("Cerrando el frontend...")
        proceso_front.terminate()
        proceso_front.wait()

def iniciar_aplicacion():
    global proceso_api, proceso_front

    # Definir las rutas a los archivos frontend y API
    ruta_front = os.path.join("Front", "pc_front.py")
    ruta_api = os.path.join("Back", "Api.py")

    # Verificar si los archivos existen
    if not os.path.exists(ruta_front):
        print(f"Error: No se pudo encontrar el archivo {ruta_front}")
        sys.exit(1)

    if not os.path.exists(ruta_api):
        print(f"Error: No se pudo encontrar el archivo {ruta_api}")
        sys.exit(1)

    try:
        print("Iniciando la API...")
        proceso_api = subprocess.Popen([sys.executable, ruta_api])
        print(f"API iniciada con PID: {proceso_api.pid}")

        print("Iniciando la aplicación frontend...")
        proceso_front = subprocess.Popen([sys.executable, ruta_front])
        print(f"Frontend iniciado con PID: {proceso_front.pid}")

        # Esperar a que el frontend termine
        proceso_front.wait()

        # Cuando el frontend termina, también cerramos la API
        if proceso_front.returncode == 0:
            print("La aplicación frontend se cerró correctamente.")
        else:
            print(f"La aplicación frontend se cerró con código de error: {proceso_front.returncode}")

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar la aplicación: {e}")
    except KeyboardInterrupt:
        print("\nEjecución interrumpida por el usuario.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        cerrar_procesos()

# Configurar la salida para ejecutar el cierre de procesos
atexit.register(cerrar_procesos)

# Punto de entrada principal del script
if __name__ == "__main__":
    iniciar_aplicacion()
