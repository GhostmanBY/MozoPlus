import unittest
import requests
import json

BASE_URL = "http://localhost:8000"  # Asegúrate de que esta es la URL correcta de tu API

class TestAPI(unittest.TestCase):
    def test_verificar_mozo(self):
        response = requests.post(f"{BASE_URL}/verificar/admin")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("verificado", data)

    def test_login_out(self):
        response = requests.post(f"{BASE_URL}/salir/Santiago Mono")
        self.assertEqual(response.status_code, 200)
        # Verifica si hay contenido en la respuesta antes de intentar acceder a él
        if response.content:
            self.assertIn("message", response.json())
        else:
            self.fail("La respuesta está vacía")

    def test_ver_mesas(self):
        response = requests.get(f"{BASE_URL}/mesas")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_cantidad_mesas(self):
        response = requests.get(f"{BASE_URL}/mesas/cantidad")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("tables", data)

    def test_guardar_mesa(self):
        # Primero, abre la mesa
        abrir_response = requests.post(f"{BASE_URL}/mesas/1/TestMozo/abrir")
        self.assertEqual(abrir_response.status_code, 200)

        # Luego, intenta guardar los datos
        data = {
            "categoria": "productos",
            "valor": ["vino", "sorrentino"]
        }
        response = requests.put(f"{BASE_URL}/mesas/1", json=data)
        self.assertEqual(response.status_code, 200)
        
        # Verifica el contenido de la respuesta
        self.assertIn("Mesa número 1 productos actualizada", response.json())

    def test_editar_mesa(self):
        response = requests.get(f"{BASE_URL}/mesas/1")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)

    def test_abrir_mesa(self):
        response = requests.post(f"{BASE_URL}/mesas/1/Juan Pérez/abrir")
        self.assertEqual(response.status_code, 200)

    def test_cerrar_mesa(self):
        response = requests.post(f"{BASE_URL}/mesas/1/cerrar")
        self.assertEqual(response.status_code, 200)

    def test_obtener_menu(self):
        response = requests.get(f"{BASE_URL}/menu")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)

if __name__ == '__main__':
    unittest.main()
