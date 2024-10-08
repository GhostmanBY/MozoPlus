from fpdf import FPDF
import json

# Lista de platos inicial vacía
lista_platos = {}

# Inicializa el PDF
pdf = FPDF()
pdf.set_font("Arial", size=15)


def agregar_a_menu(lista_platos, nombre_plato, precio, categoria):
    """Agrega un plato al menú en la lista de platos, en la categoría correspondiente."""
    if categoria not in lista_platos:
        lista_platos[categoria] = []
    lista_platos[categoria].append({"name": nombre_plato, "price": precio})

def obtener_menu_en_json():
    """Devuelve el contenido del menú en formato JSON, asegurando la codificación."""
    with open("menu.json", "r", encoding="utf-8") as file:
        return json.load(file)

def mostrar_menu(pdf, lista_platos):
    """Crea el archivo PDF con el menú."""
    pdf.add_page()
    pdf.cell(200, 10, txt="Menú del día", ln=True, align="C")
    pdf.ln(10)
    for categoria, productos in lista_platos.items():
        for producto in productos:
            agregar_a_pdf(pdf, producto["name"], producto["price"], categoria)
    pdf.output("menu.pdf", "F")


def agregar_a_pdf(pdf, nombre_plato, precio, categoria):
    """Agrega un plato al PDF en el formato correcto."""
    pdf.cell(200, 10, txt=f"{categoria} - {nombre_plato} - ${precio}", ln=True, align="L")


def crear_menu_json(lista_platos):
    """Crea el archivo JSON con el menú en el formato adecuado."""
    menu_formateado = {"menu": {}}
    for categoria, platos in lista_platos.items():
        menu_formateado["menu"][categoria] = platos

    with open("menu.json", "w", encoding="utf-8") as file:
        json.dump(menu_formateado, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # Ejemplo: agregar platos
    agregar_a_menu(lista_platos, "Coca Cola", 2.5, "bebidas")
    agregar_a_menu(lista_platos, "Sprite", 2.0, "bebidas")
    agregar_a_menu(lista_platos, "Fanta", 2.0, "bebidas")
    agregar_a_menu(lista_platos, "Agua mineral", 1.5, "bebidas")
    agregar_a_menu(lista_platos, "Jugo de naranja", 3.0, "bebidas")
    agregar_a_menu(lista_platos, "Ensalada", 5.0, "entradas")
    agregar_a_menu(lista_platos, "Pizza", 8.0, "platos principales")
    agregar_a_menu(lista_platos, "Helado", 3.0, "postres")
    agregar_a_menu(lista_platos, "Torta de zanahoria", 4.0, "postres")
    agregar_a_menu(lista_platos, "Tiramisú", 5.0, "postres")

    # Muestra el menú en el PDF
    mostrar_menu(pdf, lista_platos)
    
    # Crea el archivo JSON con el menú formateado
    crear_menu_json(lista_platos)
