import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def test_abrir_mesa(mesa_id):
    response = requests.post(f"{BASE_URL}/mesas/{mesa_id}/abrir")
    print("Test abrir mesa:", response.json())


def test_ver_mesas():
    response = requests.get(f"{BASE_URL}/mesas")
    print("Test ver mesas:", response.json())


def test_editar_mesa(mesa_id, categoria, valor):
    payload = {"categoria": categoria, "valor": valor}
    response = requests.put(f"{BASE_URL}/mesas/{mesa_id}", json=payload)
    print("Test editar mesa:", response.json())


def test_cerrar_mesa(mesa_id):
    response = requests.post(f"{BASE_URL}/mesas/{mesa_id}/cerrar")
    print("Test cerrar mesa:", response.json())


if __name__ == "__main__":
    mesa_id = 1

    # Test abrir mesa
    test_abrir_mesa(mesa_id)

    # Test ver mesas
    test_ver_mesas()

    # Test editar mesa
    test_editar_mesa(mesa_id, "productos", ["Pizza", "Refresco"])

    # Test ver mesas
    test_ver_mesas()

    # Test cerrar mesa
    test_cerrar_mesa(mesa_id)

    # Test ver mesas
    test_ver_mesas()
