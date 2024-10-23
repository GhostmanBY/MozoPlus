import subprocess
import os
import sys
import socket
import threading

def handle_connection(conn):
    """Función que maneja las conexiones entrantes"""
    data = conn.recv(1024)  # Recibir datos
    if data == b"CLOSE":
        print("Recibido comando de cierre. Terminando procesos...")
        try:
            pc_process.terminate()
            api_process.terminate()
            panel_process.terminate()  # Asegúrate de cerrar todos los procesos
            print("Procesos terminados.")
        except Exception as e:
            print(f"Error al terminar los procesos: {e}")
    conn.close()

def server_thread():
    """Hilo del servidor que espera señales de cierre"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(("localhost", 9999))  # Escuchar en el puerto 9999
        server.listen(1)  # Solo necesitamos una conexión a la vez
        print("Servidor de cierre esperando conexiones...")
        while True:
            conn, _ = server.accept()
            handle_connection(conn)
    except OSError as e:
        print(f"Error al iniciar el servidor: {e}")
    finally:
        server.close()  # Asegúrate de cerrar el socket al finalizar

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    base_dir = os.path.dirname(os.path.abspath(__file__))
    dir_api = os.path.join(base_dir, "Back/Api.py")
    dir_pc = os.path.join(base_dir, "front/pc_front.py")
    dir_panel = os.path.join(base_dir, "Back/Panel_Admin_Back.py")

    try:
        # Iniciar los procesos y guardarlos como variables globales
        pc_process = subprocess.Popen(["python", f"{dir_pc}"])
        api_process = subprocess.Popen(["python", f"{dir_api}"])
        panel_process = subprocess.Popen(["python", f"{dir_panel}"])

        # Iniciar el servidor que escucha la señal de cierre en un hilo separado
        server = threading.Thread(target=server_thread)
        server.daemon = True  # Para que el servidor no bloquee la salida del programa
        server.start()

        # Mantener el programa en ejecución
        print("Procesos iniciados. Presiona Ctrl+C para salir manualmente.")
        server.join()

    except Exception as e:
        print(f"Error al iniciar los procesos: {e}")
    finally:
        print("Cerrando...")
