import os
import platform
import subprocess
import re
import sys


# Función para obtener el sistema operativo
def get_os():
    return platform.system()

# Función para detectar la interfaz de red automáticamente en Linux
def get_linux_interface():
    result = subprocess.run(['ip', 'link', 'show'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    interfaces = re.findall(r'\d+: (\w+): <BROADCAST,MULTICAST,UP', result)
    return interfaces[0] if interfaces else None

# Función para detectar la interfaz de red automáticamente en Windows
def get_windows_interface():
    result = subprocess.run(['netsh', 'interface', 'show', 'interface'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    interfaces = re.findall(r'([A-Za-z0-9\s]+)\s+Enabled', result)
    return interfaces[0].strip() if interfaces else None

# Función para detectar el gateway automáticamente en Linux
def get_linux_gateway():
    result = subprocess.run(['ip', 'route', 'show', 'default'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    match = re.search(r'default via (\S+)', result)
    return match.group(1) if match else None

# Función para detectar el gateway automáticamente en Windows
def get_windows_gateway():
    result = subprocess.run(['netsh', 'interface', 'ipv4', 'show', 'config'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    match = re.search(r'Default Gateway:\s+(\S+)', result)
    return match.group(1) if match else None

# Función para configurar IP estática en Linux
def set_static_ip_linux(interface, ip_address, gateway, dns):
    commands = [
        f"sudo ip addr flush dev {interface}",  # Eliminar todas las IPs actuales de la interfaz
        f"sudo ip addr add {ip_address}/24 dev {interface}",  # Añadir la nueva IP
        f"sudo ip route add default via {gateway}",  # Añadir la ruta por defecto (gateway)
        f"echo 'nameserver {dns}' | sudo tee /etc/resolv.conf > /dev/null"  # Configurar DNS
    ]
    for cmd in commands:
        os.system(cmd)

# Función para configurar IP estática en Windows
def set_static_ip_windows(interface, ip_address, gateway, dns):
    commands = [
        f"netsh interface ip set address name=\"{interface}\" static {ip_address} 255.255.255.0 {gateway}",
        f"netsh interface ip set dns name=\"{interface}\" static {dns}"
    ]
    for cmd in commands:
        subprocess.run(cmd, shell=True)

# Función principal para detectar y configurar IP automáticamente
def set_static_ip(ip_address, dns):
    current_os = get_os()
    if current_os == "Linux":
        interface = get_linux_interface()
        gateway = get_linux_gateway()
        if interface and gateway:
            set_static_ip_linux(interface, ip_address, gateway, dns)
        else:
            print("No se pudo detectar la interfaz de red o el gateway en Linux")
    elif current_os == "Windows":
        interface = get_windows_interface()
        gateway = get_windows_gateway()
        if interface and gateway:
            set_static_ip_windows(interface, ip_address, gateway, dns)
        else:
            print("No se pudo detectar la interfaz de red o el gateway en Windows")
    else:
        print("Sistema operativo no soportado")

# Comprobar que se ha pasado una IP como argumento
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, introduce una dirección IP como argumento.")
        sys.exit(1)

    ip_address = sys.argv[1]  # IP proporcionada por el usuario
    dns = "8.8.8.8"  # Servidor DNS

    # Establecer la IP estática
    set_static_ip(ip_address, dns)
