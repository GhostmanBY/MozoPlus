import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Back.Menu import agregar_a_menu

lista_prueba = {}

agregar_a_menu(lista_prueba, "Coca", 8.50, "beverages")

print(lista_prueba)