import subprocess
import sys
import os

def iniciar_aplicacion():
    ruta_front = os.path.join("Front", "pc_front.py")
    
    if not os.path.exists(ruta_front):
        print(f"Error: No se pudo encontrar el archivo {ruta_front}")
        sys.exit(1)

    try:
        print("Iniciando la aplicación...")
        proceso = subprocess.Popen([sys.executable, ruta_front])
        print(f"Aplicación iniciada con PID: {proceso.pid}")
        
        # Esperar a que el proceso termine
        proceso.wait()
        
        if proceso.returncode == 0:
            print("La aplicación se cerró correctamente.")
        else:
            print(f"La aplicación se cerró con código de error: {proceso.returncode}")
    
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar la aplicación: {e}")
    except KeyboardInterrupt:
        print("\nEjecución interrumpida por el usuario.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    iniciar_aplicacion()
