import subprocess
import os
import socket

if __name__ == "__main__":
    try:
        subprocess.Popen(["python", "pc_front.py"])
        subprocess.Popen(["python", "Back/Api.py"])
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        print(f"Tu IP es {ip}")
    except Exception as e:
        print(f"Error al iniciar los procesos: {e}")
