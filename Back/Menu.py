from fpdf import FPDF
import json

# Inicializa el PDF
pdf = FPDF()
pdf.set_font("Arial", size=15)

def agregar_a_menu(lista_platos, nombre_plato, precio, categoria):
    """Agrega un plato al menú en la lista de platos, en la categoría correspondiente."""
    if categoria not in lista_platos:
        lista_platos[categoria] = []
    lista_platos[categoria].append({"name": nombre_plato, "price": precio})

def mostrar_menu(pdf, lista_platos):
    """Crea el archivo PDF con el menú."""
    pdf.add_page()
    pdf.cell(200, 10, txt="Menu del día", ln=True, align='C')
    pdf.ln(10)
    for categoria, productos in lista_platos.items():
        for producto in productos:
            agregar_a_pdf(pdf, producto['name'], producto['price'], categoria)
    pdf.output("menu.pdf")

def agregar_a_pdf(pdf, nombre_plato, precio, categoria):
    """Agrega un plato al PDF en el formato correcto."""
    pdf.cell(200, 10, txt=f"{categoria} - {nombre_plato} - ${precio}", ln=True, align='L')

def obtener_menu_en_json(lista_platos):
    """Devuelve el contenido del menú en formato JSON."""
    return json.dumps({"menu": lista_platos}, indent=4)

if __name__ == "__main__":
    # Lista de platos inicial vacía
    lista_platos = {}

    # Ejemplo: agregar platos
    agregar_a_menu(lista_platos, "Coca Cola", 2.5, "beverages")
    agregar_a_menu(lista_platos, "Sprite", 2.0, "beverages")
    agregar_a_menu(lista_platos, "Ensalada", 5.0, "starters")
    agregar_a_menu(lista_platos, "Pizza", 8.0, "main_courses")
    agregar_a_menu(lista_platos, "Helado", 3.0, "desserts")

    # Muestra el menú en el PDF
    mostrar_menu(pdf, lista_platos)

    # Muestra el menú en formato JSON
    print(obtener_menu_en_json(lista_platos))
