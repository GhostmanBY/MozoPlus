import subprocess
import os
if __name__ == "__main__":
    if not os.listdir("tmp"):
        subprocess.Popen(["python", "Front/crear_mesa.py"])
    subprocess.Popen(["python", "pc_front.py"])
    subprocess.Popen(["python", "Api.py"])

