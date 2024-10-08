import subprocess
import os
if __name__ == "__main__":
    subprocess.Popen(["python", "pc_front.py"])
    subprocess.Popen(["python", "Back/Api.py"])
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    print(f"Tu IP es {ip}")
