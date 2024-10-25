import subprocess
import sys
import os

def iniciar_aplicacion():
    # Definir la ruta al archivo frontend
    ruta_front = os.path.join("Front", "pc_front.py")
    
    # Verificar si el archivo frontend existe
    if not os.path.exists(ruta_front):
        print(f"Error: No se pudo encontrar el archivo {ruta_front}")
        sys.exit(1)

    try:
        print("Iniciando la aplicación...")
        # Iniciar el proceso de la aplicación frontend
        proceso = subprocess.Popen([sys.executable, ruta_front])
        print(f"Aplicación iniciada con PID: {proceso.pid}")
        
        # Esperar a que el proceso termine
        proceso.wait()
        
        # Verificar el código de salida del proceso
        if proceso.returncode == 0:
            print("La aplicación se cerró correctamente.")
        else:
            print(f"La aplicación se cerró con código de error: {proceso.returncode}")
    
    except subprocess.CalledProcessError as e:
        # Manejar errores específicos de la ejecución del subproceso
        print(f"Error al ejecutar la aplicación: {e}")
    except KeyboardInterrupt:
        # Manejar la interrupción por teclado (Ctrl+C)
        print("\nEjecución interrumpida por el usuario.")
    except Exception as e:
        # Capturar cualquier otra excepción no prevista
        print(f"Ocurrió un error inesperado: {e}")

# Punto de entrada principal del script
if __name__ == "__main__":
    iniciar_aplicacion()
