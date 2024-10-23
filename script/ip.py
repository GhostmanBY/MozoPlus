import subprocess
import sys

def configurar_ip_estatica(ip, mascara, puerta_enlace, interfaz):
    try:
        # Comando para establecer la IP estática
        comando = f"netsh interface ip set address {interfaz} static {ip} {mascara} {puerta_enlace}"
        subprocess.run(comando, shell=True, check=True)

        print(f"IP {ip} configurada exitosamente en la interfaz {interfaz}.")
    except subprocess.CalledProcessError as e:
        print(f"Ocurrió un error al configurar la IP: {e}")

def obtener_interfaz_wifi():
    # Lista de interfaces de red WiFi comunes
    interfaces_wifi = ["Wi-Fi", "Ethernet", "Conexión de área local"]

    # Intentar cada interfaz de red WiFi
    for interfaz in interfaces_wifi:
        try:
            # Verificar si la interfaz existe
            comando = f"netsh interface ip show config {interfaz}"
            subprocess.run(comando, shell=True, check=True)
            return interfaz
        except subprocess.CalledProcessError:
            pass

    # Si no se encuentra ninguna interfaz WiFi, devolver None
    return None

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python script.py <ip_estatica> <mascara_de_subred> <puerta_de_enlace>")
        sys.exit(1)

    ip_estatica = sys.argv[1]
    mascara_de_subred = sys.argv[2]
    puerta_de_enlace = sys.argv[3]
    interfaz_wifi = obtener_interfaz_wifi()

    if interfaz_wifi is None:
        print("No se encontró ninguna interfaz de red WiFi.")
        sys.exit(1)

    configurar_ip_estatica(ip_estatica, mascara_de_subred, puerta_de_enlace, interfaz_wifi)